"""CORE check: keep Python dependency and interpreter surfaces on the project lock.

The rule is deliberately a policy surface, not a package-manager migration:
consumers choose the roots they own, then ratchet existing legacy findings down
until those paths use the canonical project environment. No consumer paths or
package names are embedded here.
"""

from __future__ import annotations

import ast
import re
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
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
_SHELL_VENV_RE = re.compile(r"\bpython(?:3(?:\.\d+)?)?\s+-m\s+venv\b")
_SHELL_PIP_RE = re.compile(
    r"(?<![\w-])(?:(?:python(?:3(?:\.\d+)?)?|/[^ \t]+/python(?:3(?:\.\d+)?))\s+-m\s+pip|(?:/[^ \t]+/)?pip3?)\s+install\b"
)

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


def _is_exempt(relative: str, exemptions: tuple[str, ...]) -> bool:
    return any(
        relative == item.rstrip("/") or relative.startswith(item.rstrip("/") + "/") for item in exemptions
    )


def _string_sequence(node: ast.AST) -> tuple[str | None, ...] | None:
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    values: list[str | None] = []
    for item in node.elts:
        values.append(item.value if isinstance(item, ast.Constant) and isinstance(item.value, str) else None)
    return tuple(values)


def _argv_findings(text: str, relative: str) -> list[Finding]:
    try:
        tree = ast.parse(text, filename=relative)
    except (SyntaxError, UnicodeDecodeError):
        return []
    findings: list[Finding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        sequences = (
            _string_sequence(candidate)
            for candidate in ast.walk(node)
            if isinstance(candidate, (ast.List, ast.Tuple))
        )
        for sequence in sequences:
            if sequence is None:
                continue
            for index in range(len(sequence) - 1):
                pair = sequence[index : index + 2]
                if pair == ("-m", "venv"):
                    findings.append(Finding(relative, RULE_VENV_BOOTSTRAP, "-m venv", node.lineno))
                if pair == ("-m", "pip") and index + 2 < len(sequence) and sequence[index + 2] == "install":
                    findings.append(Finding(relative, RULE_RAW_PIP_INSTALL, "-m pip install", node.lineno))
            if len(sequence) >= 2 and sequence[:2] == ("pip", "install"):
                findings.append(Finding(relative, RULE_RAW_PIP_INSTALL, "pip install", node.lineno))
    return findings


def _text_findings(path: Path, relative: str) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    findings = _argv_findings(text, relative) if path.suffix in {".py", ".pyi"} else []
    for number, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if _SHELL_VENV_RE.search(line):
            findings.append(Finding(relative, RULE_VENV_BOOTSTRAP, line, number))
        if _SHELL_PIP_RE.search(line) and not re.search(r"\buv\s+pip\s+install\b", line):
            findings.append(Finding(relative, RULE_RAW_PIP_INSTALL, line, number))
        if _PRIVATE_INTERPRETER_RE.search(line):
            findings.append(Finding(relative, RULE_PRIVATE_INTERPRETER, line, number))
    return findings


def _iter_files(
    root: Path,
    roots: tuple[str, ...],
    extensions: tuple[str, ...],
    manifest_patterns: tuple[str, ...],
) -> Iterable[Path]:
    import fnmatch

    for configured in roots:
        base = (root / configured).resolve()
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            relative_parts = path.relative_to(root).parts
            if any(
                part in {".git", ".venv", "venv", "__pycache__", "node_modules"} for part in relative_parts
            ):
                continue
            if (
                path.suffix in extensions
                or bool(path.stat().st_mode & 0o111)
                or any(fnmatch.fnmatch(path.name, pattern) for pattern in manifest_patterns)
            ):
                yield path


def scan_findings(
    root: Path,
    *,
    roots: tuple[str, ...],
    extensions: tuple[str, ...] = DEFAULT_EXTENSIONS,
    exempt_paths: tuple[str, ...] = (),
    manifest_patterns: tuple[str, ...] = DEFAULT_MANIFEST_PATTERNS,
    canonical_manifests: tuple[str, ...] = DEFAULT_CANONICAL_MANIFESTS,
) -> tuple[Finding, ...]:
    """Return deterministic raw findings before applying ratchet allowances."""
    import fnmatch

    findings: list[Finding] = []
    seen: set[tuple[str, str, str, int]] = set()
    for path in _iter_files(root, roots, extensions, manifest_patterns):
        relative = _relative(path, root)
        if _is_exempt(relative, exempt_paths):
            continue
        for finding in _text_findings(path, relative):
            key = (finding.path, finding.rule, finding.content, finding.line)
            if key not in seen:
                findings.append(finding)
                seen.add(key)
        if any(fnmatch.fnmatch(path.name, pattern) for pattern in manifest_patterns):
            if relative not in canonical_manifests:
                finding = Finding(relative, RULE_ALTERNATIVE_MANIFEST, path.name)
                key = (finding.path, finding.rule, finding.content, finding.line)
                if key not in seen:
                    findings.append(finding)
                    seen.add(key)
    return tuple(sorted(findings, key=lambda item: (item.path, item.rule, item.line, item.content)))


class PythonDependencySurface(FitnessRule):
    """Flags legacy Python dependency bootstrap and alternative manifest surfaces."""

    name = "python-dependency-surface"
    remediation = REMEDIATION
    extensions = DEFAULT_EXTENSIONS
    exempt_paths: tuple[str, ...] = ()
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
        rule.exempt_paths = tuple(str(item) for item in config.get("exempt_paths", ()))
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
            ratchets.append(
                Ratchet(
                    path=str(item["path"]),
                    rule=str(item["rule"]),
                    max_count=maximum,
                    contents=tuple(str(content) for content in item.get("contents", ())),
                )
            )
        rule.ratchets = tuple(ratchets)
        return rule

    def _raw_findings(self) -> tuple[Finding, ...]:
        return scan_findings(
            self._repo_root,
            roots=self._roots,
            extensions=self._extensions,
            exempt_paths=self.exempt_paths,
            manifest_patterns=self.manifest_patterns,
            canonical_manifests=self.canonical_manifests,
        )

    def _allowed(self, finding: Finding, counts: Counter[tuple[str, str]]) -> bool:
        ratchet = next(
            (item for item in self.ratchets if item.path == finding.path and item.rule == finding.rule),
            None,
        )
        if ratchet is None or counts[(finding.path, finding.rule)] > ratchet.max_count:
            return False
        return not ratchet.contents or finding.content in ratchet.contents

    def collect_violations(self) -> set[Path]:
        findings = self._raw_findings()
        counts: Counter[tuple[str, str]] = Counter((item.path, item.rule) for item in findings)
        return {Path(item.path) for item in findings if not self._allowed(item, counts)}

    def file_has_violation(self, path: Path) -> bool:
        relative = _relative(path, self._repo_root)
        findings = [item for item in self._raw_findings() if item.path == relative]
        counts: Counter[tuple[str, str]] = Counter((item.path, item.rule) for item in findings)
        return any(not self._allowed(item, counts) for item in findings)


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> PythonDependencySurface:
    """Factory the engine calls to bind this CORE check to consumer config."""
    return PythonDependencySurface.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry for the standalone invocation."""
    return run_core_check(PythonDependencySurface, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
