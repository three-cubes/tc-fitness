"""CORE check: keep Python dependency and interpreter surfaces on the project lock.

The rule is deliberately a policy surface, not a package-manager migration:
consumers choose the roots they own, then ratchet existing legacy findings down
until those paths use the canonical project environment. No consumer paths or
package names are embedded here.
"""

from __future__ import annotations

import ast
import re
import shlex
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule, enumerate_repo_files
from tc_fitness.lib import remediation as _remediation

RULE_RAW_PIP_INSTALL = "raw-pip-install"
RULE_VENV_BOOTSTRAP = "python-m-venv"
RULE_PRIVATE_INTERPRETER = "private-interpreter"
RULE_ALTERNATIVE_MANIFEST = "alternative-dependency-manifest"

DEFAULT_EXTENSIONS = (".py", ".pyi", ".sh", ".bash")
DEFAULT_MANIFEST_PATTERNS = (
    "pyproject.toml",
    "uv.lock",
    "requirements*.txt",
    "requirements/*.txt",
    "*/requirements/*.txt",
    "Pipfile",
    "Pipfile.lock",
    "poetry.lock",
    "setup.py",
    "setup.cfg",
)
DEFAULT_CANONICAL_MANIFESTS = ("pyproject.toml", "uv.lock")
_PRIVATE_INTERPRETER_RE = re.compile(
    r"""(?<![\w.-])(?:[^"'\s/]+/)*(?:\.venv|venv)/bin/(?:python|python\d+(?:\.\d+)?|pip|pip\d+)(?![\w.-])"""
)
_PROCESS_MODULE_APIS = {
    "subprocess": {"Popen", "call", "check_call", "check_output", "run"},
}
_PYTHON_INTERPRETER_RE = re.compile(r"python(?:3(?:\.\d+)?)?")
_PIP_OPTIONS_WITH_VALUES = frozenset(
    {
        "--abi",
        "--build-constraint",
        "--cache-dir",
        "--cert",
        "--client-cert",
        "--config-settings",
        "--constraint",
        "--exists-action",
        "--extra-index-url",
        "--find-links",
        "--implementation",
        "--index-url",
        "--log",
        "--log-file",
        "--platform",
        "--prefix",
        "--progress-bar",
        "--proxy",
        "--python",
        "--report",
        "--retries",
        "--root",
        "--root-user-action",
        "--src",
        "--target",
        "--timeout",
        "--trusted-host",
        "--use-deprecated",
        "--use-feature",
    }
)
_PIP_SHORT_OPTIONS_WITH_VALUES = frozenset({"-c", "-f", "-i", "-r", "-t"})

REMEDIATION = _remediation(
    fix=(
        "use the repository's declared project dependency group and invoke tools "
        "through `uv run` or the configured project interpreter; remove raw "
        "`pip install`, `python -m venv`, and private `.venv/bin` bootstrap paths. "
        "For an existing exception, add one exact ratchet entry with a bounded "
        "count and stable content, then shrink it in a follow-up."
    ),
    nxt="re-run `uv run tc-fitness run` and reduce the ratchet until the finding is gone.",
    run="uv run tc-fitness run",
    passing="uv run --locked python -m package.module",
    forbidden='subprocess.run([sys.executable, "-m", "pip", "install", "package"])',
)


@dataclass(frozen=True)
class Finding:
    """One stable dependency-surface finding."""

    path: str
    rule: str
    content: str
    line: int = 0


@dataclass(frozen=True)
class Ratchet:
    """A shrink-only allowance for one path/rule pair."""

    path: str
    rule: str
    max_count: int
    contents: tuple[str, ...] = ()


def _relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _string_sequence(node: ast.AST) -> tuple[str | None, ...] | None:
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    values: list[str | None] = []
    for item in node.elts:
        values.append(item.value if isinstance(item, ast.Constant) and isinstance(item.value, str) else None)
    return tuple(values)


def _argv_content(sequence: tuple[str | None, ...]) -> str:
    return " ".join(item if item is not None else "<dynamic>" for item in sequence)


def _split_shell_commands(line: str) -> tuple[str, ...]:
    commands: list[str] = []
    start = 0
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif quote:
            if char == quote:
                quote = None
        elif char in {"'", '"'}:
            quote = char
        elif char in ";|&" or line[index : index + 2] in {"&&", "||"}:
            commands.append(line[start:index].strip())
            index += 2 if line[index : index + 2] in {"&&", "||"} else 1
            start = index
            continue
        index += 1
    commands.append(line[start:].strip())
    return tuple(command for command in commands if command)


def _launch_call(node: ast.Call, module_aliases: dict[str, str], function_aliases: set[str]) -> bool:
    function = node.func
    if isinstance(function, ast.Attribute):
        return isinstance(function.value, ast.Name) and function.attr in _PROCESS_MODULE_APIS.get(
            module_aliases.get(function.value.id, ""), set()
        )
    return isinstance(function, ast.Name) and function.id in function_aliases


def _process_aliases(tree: ast.Module) -> tuple[dict[str, str], set[str]]:
    module_aliases: dict[str, str] = {}
    function_aliases: set[str] = set()
    rebound: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in _PROCESS_MODULE_APIS:
                    module_aliases[alias.asname or alias.name] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module in _PROCESS_MODULE_APIS:
            for alias in node.names:
                if alias.name in _PROCESS_MODULE_APIS[node.module]:
                    function_aliases.add(alias.asname or alias.name)
    for descendant in ast.walk(tree):
        if isinstance(descendant, ast.Name) and isinstance(descendant.ctx, ast.Store):
            rebound.add(descendant.id)
        if isinstance(descendant, ast.arg):
            rebound.add(descendant.arg)
    return {name: module for name, module in module_aliases.items() if name not in rebound}, {
        name for name in function_aliases if name not in rebound
    }


def _pip_install_index(sequence: tuple[str | None, ...]) -> int | None:
    if not sequence or sequence[0] == "uv":
        return None
    executable = sequence[0]
    pip_start: int | None = None
    if executable is not None and re.fullmatch(r"pip(?:3(?:\.\d+)?)?", Path(executable).name):
        pip_start = 1
    elif len(sequence) >= 3 and sequence[1:3] == ("-m", "pip"):
        interpreter = Path(executable).name if executable is not None else ""
        if executable is None or re.fullmatch(r"python(?:3(?:\.\d+)?)?", interpreter):
            pip_start = 3
    elif len(sequence) >= 3 and sequence[:2] == ("-m", "pip"):
        pip_start = 2
    if pip_start is None:
        return None
    index = pip_start
    while index < len(sequence):
        if sequence[index] == "install":
            return index
        argument = sequence[index]
        if argument is not None and (
            argument in _PIP_OPTIONS_WITH_VALUES or argument in _PIP_SHORT_OPTIONS_WITH_VALUES
        ):
            index += 2
            continue
        if argument is not None and argument.startswith("--") and "=" in argument:
            index += 1
            continue
        if argument is not None and not argument.startswith("-"):
            break
        index += 1
    return None


def _argv_findings(text: str, relative: str) -> list[Finding]:
    try:
        tree = ast.parse(text, filename=relative)
    except (SyntaxError, UnicodeDecodeError):
        return []
    findings: list[Finding] = []
    module_aliases, function_aliases = _process_aliases(tree)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not _launch_call(node, module_aliases, function_aliases):
            continue
        argv_nodes = list(node.args[:1])
        argv_nodes.extend(keyword.value for keyword in node.keywords if keyword.arg == "args")
        sequences = (_string_sequence(candidate) for candidate in argv_nodes)
        for sequence in sequences:
            if sequence is None:
                continue
            if any(item is not None and _PRIVATE_INTERPRETER_RE.search(item) for item in sequence):
                findings.append(
                    Finding(relative, RULE_PRIVATE_INTERPRETER, _argv_content(sequence), node.lineno)
                )
            for index in range(len(sequence) - 1):
                pair = sequence[index : index + 2]
                if pair == ("-m", "venv"):
                    findings.append(
                        Finding(relative, RULE_VENV_BOOTSTRAP, _argv_content(sequence), node.lineno)
                    )
            if _pip_install_index(sequence) is not None:
                findings.append(Finding(relative, RULE_RAW_PIP_INSTALL, _argv_content(sequence), node.lineno))
    return findings


def _text_findings(path: Path, relative: str) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    first_line = text.splitlines()[:1]
    python_source = path.suffix in {".py", ".pyi"} or (
        first_line and first_line[0].startswith("#!") and "python" in first_line[0]
    )
    findings = _argv_findings(text, relative) if python_source else []
    # Python source is analysed structurally above.  Applying shell text rules
    # to the same lines would duplicate one semantic argv finding and make
    # ratchet counts unstable; dynamic string construction remains outside the
    # detector's static guarantee.
    if python_source:
        return findings
    logical_lines: list[tuple[int, str]] = []
    pending = ""
    start_line = 1
    for number, raw_line in enumerate(text.splitlines(), 1):
        stripped = raw_line.rstrip()
        if not pending:
            start_line = number
        if stripped.endswith("\\"):
            pending += stripped[:-1] + " "
            continue
        logical_lines.append((start_line, pending + stripped))
        pending = ""
    if pending:
        logical_lines.append((start_line, pending))
    for number, raw_line in logical_lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        for command in _split_shell_commands(line):
            try:
                tokens = tuple(shlex.split(command))
            except ValueError:
                tokens = ()
            if (
                len(tokens) >= 3
                and _PYTHON_INTERPRETER_RE.fullmatch(Path(tokens[0]).name)
                and tokens[1:3] == ("-m", "venv")
            ):
                findings.append(Finding(relative, RULE_VENV_BOOTSTRAP, command, number))
            if (
                tokens
                and _pip_install_index(tokens) is not None
                and not (tokens[0] == "uv" and "pip" in tokens[:3])
            ):
                findings.append(Finding(relative, RULE_RAW_PIP_INSTALL, command, number))
            if tokens and _PRIVATE_INTERPRETER_RE.search(tokens[0]):
                findings.append(Finding(relative, RULE_PRIVATE_INTERPRETER, command, number))
    return findings


def _iter_files(
    root: Path,
    roots: tuple[str, ...],
    extensions: tuple[str, ...],
    manifest_patterns: tuple[str, ...],
) -> Iterable[Path]:
    import fnmatch

    for path in enumerate_repo_files(root, roots):
        relative = path.relative_to(root.resolve()).as_posix()
        if (
            path.suffix in extensions
            or bool(path.stat().st_mode & 0o111)
            or any(
                fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(path.name, pattern)
                for pattern in manifest_patterns
            )
        ):
            yield path


def scan_findings(
    root: Path,
    *,
    roots: tuple[str, ...],
    extensions: tuple[str, ...] = DEFAULT_EXTENSIONS,
    manifest_patterns: tuple[str, ...] = DEFAULT_MANIFEST_PATTERNS,
    canonical_manifests: tuple[str, ...] = DEFAULT_CANONICAL_MANIFESTS,
) -> tuple[Finding, ...]:
    """Return deterministic raw findings before applying ratchet allowances."""
    import fnmatch

    findings: list[Finding] = []
    seen: set[tuple[str, str, str, int]] = set()
    for path in _iter_files(root, roots, extensions, manifest_patterns):
        relative = _relative(path, root)
        for finding in _text_findings(path, relative):
            key = (finding.path, finding.rule, finding.content, finding.line)
            if key not in seen:
                findings.append(finding)
                seen.add(key)
        if any(
            fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(path.name, pattern)
            for pattern in manifest_patterns
        ):
            if relative not in canonical_manifests:
                finding = Finding(relative, RULE_ALTERNATIVE_MANIFEST, path.name)
                findings.append(finding)
    return tuple(sorted(findings, key=lambda item: (item.path, item.rule, item.line, item.content)))


class PythonDependencySurface(FitnessRule):
    """Flags legacy Python dependency bootstrap and alternative manifest surfaces."""

    name = "python-dependency-surface"
    remediation = REMEDIATION
    extensions = DEFAULT_EXTENSIONS
    manifest_patterns: tuple[str, ...] = DEFAULT_MANIFEST_PATTERNS
    canonical_manifests: tuple[str, ...] = DEFAULT_CANONICAL_MANIFESTS
    ratchets: tuple[Ratchet, ...] = ()

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PythonDependencySurface:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PythonDependencySurface)  # noqa: S101
        if "exempt_paths" in config:
            raise ValueError("exempt_paths is not supported: findings cannot be suppressed")
        rule.manifest_patterns = tuple(
            str(item) for item in config.get("manifest_patterns", DEFAULT_MANIFEST_PATTERNS)
        )
        rule.canonical_manifests = tuple(
            str(item) for item in config.get("canonical_manifests", DEFAULT_CANONICAL_MANIFESTS)
        )
        raw_ratchets = config.get("ratchets", ())
        if not isinstance(raw_ratchets, (list, tuple)):
            raise ValueError("ratchets must be an array of tables")
        ratchets: list[Ratchet] = []
        for item in raw_ratchets:
            if not isinstance(item, Mapping):
                raise ValueError("each ratchet must be a table")
            maximum = int(item.get("max_count", 0))
            if maximum < 0:
                raise ValueError("ratchet max_count must be non-negative")
            raw_contents = item.get("contents", ())
            if maximum > 0 and not raw_contents:
                raise ValueError("positive ratchets must declare non-empty contents")
            ratchets.append(
                Ratchet(
                    path=str(item["path"]),
                    rule=str(item["rule"]),
                    max_count=maximum,
                    contents=tuple(str(content) for content in raw_contents),
                )
            )
        rule.ratchets = tuple(ratchets)
        return rule

    def _raw_findings(self) -> tuple[Finding, ...]:
        return scan_findings(
            self._repo_root,
            roots=self._roots,
            extensions=self._extensions,
            manifest_patterns=self.manifest_patterns,
            canonical_manifests=self.canonical_manifests,
        )

    def _allowed(self, finding: Finding, counts: Counter[tuple[str, str]]) -> bool:
        ratchet = next(
            (item for item in self.ratchets if item.path == finding.path and item.rule == finding.rule),
            None,
        )
        if ratchet is None or counts[(finding.path, finding.rule)] != ratchet.max_count:
            return False
        return not ratchet.contents or finding.content in ratchet.contents

    def _violating_findings(self) -> tuple[tuple[Finding, ...], tuple[Ratchet, ...]]:
        findings = self._raw_findings()
        counts: Counter[tuple[str, str]] = Counter((item.path, item.rule) for item in findings)
        violations = tuple(item for item in findings if not self._allowed(item, counts))
        observed = {(item.path, item.rule) for item in findings}
        stale = tuple(
            ratchet
            for ratchet in self.ratchets
            if ratchet.max_count > 0 and (ratchet.path, ratchet.rule) not in observed
        )
        return violations, stale

    def collect_violations(self) -> set[Path]:
        violations, stale = self._violating_findings()
        return {Path(item.path) for item in violations} | {Path(item.path) for item in stale}

    def file_has_violation(self, path: Path) -> bool:
        relative = _relative(path, self._repo_root)
        violations, stale = self._violating_findings()
        return relative in {item.path for item in violations} | {item.path for item in stale}

    def run(self) -> int:
        """Emit each raw policy rule as a contract-visible structured finding."""
        violations, stale = self._violating_findings()
        for finding in violations:
            report_finding(finding.rule, finding.path, finding.content)
            print(f"FAIL [{self.name}] {finding.path}: {finding.content}")
        for ratchet in stale:
            message = "ratchet has no matching current finding; remove stale migration debt"
            report_finding(ratchet.rule, ratchet.path, message)
            print(f"FAIL [{self.name}] {ratchet.path}: {message}")
        if violations or stale:
            print(self.remediation)
        return int(bool(violations or stale))


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> PythonDependencySurface:
    """Factory the engine calls to bind this CORE check to consumer config."""
    return PythonDependencySurface.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry for the standalone invocation."""
    return run_core_check(PythonDependencySurface, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
