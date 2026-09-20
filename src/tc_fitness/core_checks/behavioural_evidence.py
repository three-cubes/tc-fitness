"""CORE check: critical surfaces have executable, observed test evidence.

Static policy tests are useful for source-shape invariants, but they cannot
prove that a build, command, deployment adapter, or runtime works.  Consumers
declare critical surfaces and the real executable each surface depends on.
This hard gate then requires a marked test to invoke that executable, check
process success, and observe a produced artefact passed through the command.

The check is deliberately opt-in and repo-neutral.  An empty configuration is
a vacuous pass; once configured, findings cannot be baselined.
"""

from __future__ import annotations

import ast
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, cast

from tc_fitness.check_evidence import report_finding
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

REMEDIATION = _remediation(
    fix=(
        "map every critical surface to a marked behavioural test that invokes the declared "
        "executable and asserts its result or a produced artefact"
    ),
    nxt="run the declared behavioural test, then re-run this check",
    run="python -m tc_fitness.core_checks.behavioural_evidence",
    passing="a real executable invocation followed by process and produced-output assertions",
    forbidden="source-text or configuration-shape assertions presented as behavioural evidence",
)

_SUBPROCESS_CALLS = frozenset(
    {
        "subprocess.run",
        "subprocess.Popen",
        "subprocess.call",
        "subprocess.check_call",
        "subprocess.check_output",
    }
)
_RESULT_ATTRIBUTES = frozenset({"returncode", "stdout", "stderr"})
_OUTPUT_OBSERVATIONS = frozenset(
    {"exists", "is_file", "is_dir", "read_text", "read_bytes", "stat", "iterdir"}
)


@dataclass(frozen=True, order=True)
class BehaviouralEvidenceFinding:
    """One deterministic evidence-integrity defect."""

    source: Path
    pointer: str
    code: str
    message: str
    fix: str


def _finding(
    source: str | Path, pointer: str, code: str, message: str, fix: str
) -> BehaviouralEvidenceFinding:
    return BehaviouralEvidenceFinding(Path(source), pointer, code, message, fix)


def _safe_relative_path(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        return None
    return path.as_posix()


def _sequence(value: object) -> tuple[object, ...] | None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return None
    return tuple(value)


def _dotted_name(value: ast.expr) -> str | None:
    if isinstance(value, ast.Name):
        return value.id
    if isinstance(value, ast.Attribute):
        parent = _dotted_name(value.value)
        return f"{parent}.{value.attr}" if parent else None
    return None


def _import_aliases(tree: ast.Module) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name != "*":
                    aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def _resolved_name(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    return ".".join((aliases.get(root, root), *suffix))


def _marker_names(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(item, aliases) for item in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def _module_markers(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets
        ):
            return _marker_names(node.value, aliases)
    return set()


def _function_markers(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> set[str]:
    return set().union(*(_marker_names(decorator, aliases) for decorator in node.decorator_list))


def _path_fragment(value: ast.expr, constants: Mapping[str, str]) -> str | None:
    """Resolve literal/path-join syntax to a stable relative suffix."""
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return value.value
    if isinstance(value, ast.Name):
        return constants.get(value.id)
    if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id in {"str", "Path"}:
        if value.args:
            return _path_fragment(value.args[0], constants)
    if isinstance(value, ast.BinOp) and isinstance(value.op, ast.Div):
        left = _path_fragment(value.left, constants)
        right = _path_fragment(value.right, constants)
        if right is None:
            return None
        return f"{left.rstrip('/')}/{right.lstrip('/')}" if left else right
    return None


def _path_constants(tree: ast.Module) -> dict[str, str]:
    constants: dict[str, str] = {}
    assignments = [node for node in tree.body if isinstance(node, ast.Assign)]
    for _ in range(len(assignments) + 1):
        changed = False
        for node in assignments:
            fragment = _path_fragment(node.value, constants)
            if fragment is None:
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and constants.get(target.id) != fragment:
                    constants[target.id] = fragment
                    changed = True
        if not changed:
            break
    return constants


def _command_expression(call: ast.Call) -> ast.expr | None:
    if not call.args:
        return None
    argv = call.args[0]
    if isinstance(argv, ast.List | ast.Tuple) and argv.elts:
        return argv.elts[0]
    return argv


def _normalise_suffix(value: str) -> str:
    return PurePosixPath(value).as_posix().lstrip("./")


def _call_executes(
    call: ast.Call,
    *,
    executable: str,
    aliases: Mapping[str, str],
    constants: Mapping[str, str],
) -> bool:
    if _resolved_name(call.func, aliases) not in _SUBPROCESS_CALLS:
        return False
    command = _command_expression(call)
    fragment = _path_fragment(command, constants) if command is not None else None
    if fragment is None:
        return False
    return _normalise_suffix(fragment).endswith(_normalise_suffix(executable))


def _names_and_attributes(node: ast.AST) -> tuple[set[str], set[tuple[str, str]]]:
    names: set[str] = set()
    attributes: set[tuple[str, str]] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            names.add(child.id)
        elif isinstance(child, ast.Attribute) and isinstance(child.value, ast.Name):
            attributes.add((child.value.id, child.attr))
    return names, attributes


def _assert_observes_process(assertion: ast.Assert, result_names: set[str]) -> bool:
    _, attributes = _names_and_attributes(assertion.test)
    return any(name in result_names and attribute in _RESULT_ATTRIBUTES for name, attribute in attributes)


def _assert_observes_output(assertion: ast.Assert, command_names: set[str]) -> bool:
    for child in ast.walk(assertion.test):
        if not (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr in _OUTPUT_OBSERVATIONS
        ):
            continue
        names, _ = _names_and_attributes(child.func.value)
        if names & command_names:
            return True
    return False


@dataclass(frozen=True)
class _TestEvidence:
    has_marker: bool
    executes: bool
    observes_process: bool
    observes_output: bool


def _test_file_evidence(path: Path, *, executable: str, markers: frozenset[str]) -> _TestEvidence:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return _TestEvidence(False, False, False, False)
    aliases = _import_aliases(tree)
    module_markers = _module_markers(tree, aliases)
    constants = _path_constants(tree)
    has_marker = False
    executes = False
    observes_process = False
    observes_output = False
    for test in ast.walk(tree):
        if not isinstance(test, ast.FunctionDef | ast.AsyncFunctionDef) or not test.name.startswith("test_"):
            continue
        if not ((module_markers | _function_markers(test, aliases)) & markers):
            continue
        has_marker = True
        result_names: set[str] = set()
        command_names: set[str] = set()
        check_enforced = False
        execution_lines: list[int] = []
        for node in ast.walk(test):
            call: ast.Call | None = None
            result_name: str | None = None
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                call = node.value
                if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    result_name = node.targets[0].id
            elif isinstance(node, ast.AnnAssign) and isinstance(node.value, ast.Call):
                call = node.value
                if isinstance(node.target, ast.Name):
                    result_name = node.target.id
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                call = node.value
            if call is None or not _call_executes(
                call, executable=executable, aliases=aliases, constants=constants
            ):
                continue
            executes = True
            execution_lines.append(call.lineno)
            command_names.update(child.id for child in ast.walk(call) if isinstance(child, ast.Name))
            check_enforced = check_enforced or any(
                keyword.arg == "check"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in call.keywords
            )
            if result_name:
                result_names.add(result_name)
        if not execution_lines:
            continue
        first_execution = min(execution_lines)
        if check_enforced or any(
            isinstance(node, ast.Assert)
            and node.lineno > first_execution
            and _assert_observes_process(node, result_names)
            for node in ast.walk(test)
        ):
            observes_process = True
        if any(
            isinstance(node, ast.Assert)
            and node.lineno > first_execution
            and _assert_observes_output(node, command_names)
            for node in ast.walk(test)
        ):
            observes_output = True
    return _TestEvidence(has_marker, executes, observes_process, observes_output)


class BehaviouralEvidence(FitnessRule):
    """Hard gate for declared critical-surface behavioural evidence."""

    name = "behavioural-evidence"
    remediation = REMEDIATION

    def __init__(self, config: Mapping[str, object], *, repo_root: Path | None = None) -> None:
        super().__init__(repo_root=repo_root)
        self.config = dict(config)
        self.active = bool(config)

    @classmethod
    def from_config(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> BehaviouralEvidence:
        return cls(cast(Mapping[str, object], config), repo_root=repo_root)

    def file_has_violation(self, path: Path) -> bool:
        return False

    def collect_findings(self) -> tuple[BehaviouralEvidenceFinding, ...]:
        if not self.active:
            return ()
        findings: list[BehaviouralEvidenceFinding] = []
        marker_values = _sequence(self.config.get("behaviour_markers"))
        markers = frozenset(value for value in marker_values or () if isinstance(value, str) and value)
        if not markers:
            findings.append(
                _finding(
                    "pyproject.toml",
                    "/behaviour_markers",
                    "invalid-behaviour-markers",
                    "behaviour_markers must contain at least one non-empty pytest marker",
                    "declare the integration, e2e, journey or equivalent markers that carry real evidence",
                )
            )

        matched_surfaces: set[str] = set()
        glob_values = _sequence(self.config.get("surface_globs"))
        for index, raw_glob in enumerate(glob_values or ()):
            pattern = _safe_relative_path(raw_glob)
            if pattern is None:
                findings.append(
                    _finding(
                        "pyproject.toml",
                        f"/surface_globs/{index}",
                        "invalid-surface-glob",
                        "surface glob must be a non-empty repo-relative POSIX path",
                        "use a repo-relative glob without '..' or a leading slash",
                    )
                )
                continue
            matches = {path.relative_to(self._repo_root).as_posix() for path in self._repo_root.glob(pattern)}
            if not matches:
                findings.append(
                    _finding(
                        pattern,
                        f"/surface_globs/{index}",
                        "unmatched-surface-glob",
                        f"critical surface glob {pattern!r} matches no files",
                        "correct the glob or restore the required critical surface",
                    )
                )
            matched_surfaces.update(matches)

        claims_raw = _sequence(self.config.get("claims"))
        claimed_surfaces: set[str] = set()
        seen_ids: set[str] = set()
        if claims_raw is None or not claims_raw:
            findings.append(
                _finding(
                    "pyproject.toml",
                    "/claims",
                    "missing-evidence-claims",
                    "active behavioural evidence configuration requires at least one claim",
                    "map each critical surface to its executable and behavioural tests",
                )
            )
            claims_raw = ()

        for index, raw_claim in enumerate(claims_raw):
            pointer = f"/claims/{index}"
            if not isinstance(raw_claim, Mapping):
                findings.append(
                    _finding(
                        "pyproject.toml",
                        pointer,
                        "invalid-evidence-claim",
                        "each claim must be a mapping",
                        "declare id, surfaces, tests and executables for the claim",
                    )
                )
                continue
            claim = cast(Mapping[str, object], raw_claim)
            claim_id = claim.get("id")
            if not isinstance(claim_id, str) or not claim_id.strip() or claim_id in seen_ids:
                findings.append(
                    _finding(
                        "pyproject.toml",
                        f"{pointer}/id",
                        "invalid-evidence-claim-id",
                        "claim id must be a unique non-empty string",
                        "give each behavioural claim one stable unique id",
                    )
                )
                claim_id = f"claim-{index}"
            seen_ids.add(claim_id)

            surface_values = _sequence(claim.get("surfaces"))
            if not surface_values:
                findings.append(
                    _finding(
                        "pyproject.toml",
                        f"{pointer}/surfaces",
                        "missing-claim-surfaces",
                        f"claim {claim_id!r} has no critical surfaces",
                        "name every exact critical surface proved by this claim",
                    )
                )
            for surface_index, raw_surface in enumerate(surface_values or ()):
                surface = _safe_relative_path(raw_surface)
                if surface is None:
                    findings.append(
                        _finding(
                            "pyproject.toml",
                            f"{pointer}/surfaces/{surface_index}",
                            "invalid-claimed-surface",
                            "claimed surface must be a repo-relative POSIX path",
                            "declare the exact repository path of the critical surface",
                        )
                    )
                    continue
                claimed_surfaces.add(surface)
                if not (self._repo_root / surface).is_file():
                    findings.append(
                        _finding(
                            surface,
                            f"{pointer}/surfaces/{surface_index}",
                            "missing-claimed-surface",
                            f"claim {claim_id!r} names a surface that does not exist",
                            "restore the surface or remove the stale claim",
                        )
                    )

            test_values = _sequence(claim.get("tests"))
            if not test_values:
                findings.append(
                    _finding(
                        "pyproject.toml",
                        f"{pointer}/tests",
                        "missing-claim-tests",
                        f"claim {claim_id!r} has no behavioural tests",
                        "name the integration or E2E tests that execute this claim",
                    )
                )
            test_paths: list[Path] = []
            for test_index, raw_test in enumerate(test_values or ()):
                test_rel = _safe_relative_path(raw_test)
                if test_rel is None:
                    findings.append(
                        _finding(
                            "pyproject.toml",
                            f"{pointer}/tests/{test_index}",
                            "invalid-evidence-test",
                            "evidence test must be a repo-relative POSIX path",
                            "declare an exact Python test path",
                        )
                    )
                    continue
                test_path = self._repo_root / test_rel
                if not test_path.is_file():
                    findings.append(
                        _finding(
                            test_rel,
                            f"{pointer}/tests/{test_index}",
                            "missing-evidence-test",
                            f"claim {claim_id!r} names a test that does not exist",
                            "add the behavioural test or remove the stale claim",
                        )
                    )
                    continue
                test_paths.append(test_path)

            executable_values = _sequence(claim.get("executables"))
            if not executable_values:
                findings.append(
                    _finding(
                        "pyproject.toml",
                        f"{pointer}/executables",
                        "missing-claim-executables",
                        f"claim {claim_id!r} has no executable boundary",
                        "name the real executable the behavioural test must invoke",
                    )
                )
            for executable_index, raw_executable in enumerate(executable_values or ()):
                executable = _safe_relative_path(raw_executable)
                if executable is None:
                    findings.append(
                        _finding(
                            "pyproject.toml",
                            f"{pointer}/executables/{executable_index}",
                            "invalid-evidence-executable",
                            "evidence executable must be a repo-relative POSIX path",
                            "declare the exact executable path used by the critical surface",
                        )
                    )
                    continue
                if not test_paths:
                    continue
                evidence = [
                    _test_file_evidence(path, executable=executable, markers=markers) for path in test_paths
                ]
                if not any(item.has_marker for item in evidence):
                    findings.append(
                        _finding(
                            test_paths[0].relative_to(self._repo_root) if test_paths else "pyproject.toml",
                            f"{pointer}/tests",
                            "missing-behaviour-marker",
                            f"claim {claim_id!r} has no test using a configured behavioural marker",
                            "mark the real behavioural test as integration, e2e, journey or the configured equivalent",
                        )
                    )
                elif not any(item.executes for item in evidence):
                    findings.append(
                        _finding(
                            executable,
                            f"{pointer}/executables/{executable_index}",
                            "missing-executable-evidence",
                            f"claim {claim_id!r} never executes {executable}",
                            "invoke the declared executable through subprocess in a configured behavioural test",
                        )
                    )
                else:
                    if not any(item.executes and item.observes_process for item in evidence):
                        findings.append(
                            _finding(
                                executable,
                                f"{pointer}/executables/{executable_index}",
                                "missing-process-observation",
                                f"claim {claim_id!r} executes {executable} without checking process success",
                                "assert returncode/stdout/stderr or invoke subprocess with check=True",
                            )
                        )
                    if any(item.executes and item.observes_output for item in evidence):
                        continue
                    findings.append(
                        _finding(
                            executable,
                            f"{pointer}/executables/{executable_index}",
                            "missing-output-observation",
                            f"claim {claim_id!r} executes {executable} without asserting a passed output",
                            "assert a produced file, response or retained receipt passed to the executable",
                        )
                    )

        for surface in sorted(matched_surfaces - claimed_surfaces):
            findings.append(
                _finding(
                    surface,
                    "/surface_globs",
                    "unclaimed-critical-surface",
                    "critical surface has no behavioural evidence claim",
                    "map the surface to the executable and test that prove its behaviour",
                )
            )
        return tuple(sorted(set(findings)))

    def run(self) -> int:
        findings = self.collect_findings()
        if not findings:
            return 0
        for finding in findings:
            report_finding(
                self.name,
                finding.source.as_posix(),
                f"{finding.pointer}: {finding.code}: {finding.message}; fix: {finding.fix}",
            )
            print(f"{finding.source}:{finding.pointer}: {finding.code}: {finding.message}", file=sys.stderr)
            print(f"fix: {finding.fix}", file=sys.stderr)
            print("next: run the declared behavioural test, then re-run this check", file=sys.stderr)
            print("run: python -m tc_fitness.core_checks.behavioural_evidence", file=sys.stderr)
        return 1

    def establish_baseline(self) -> Path:
        findings = self.collect_findings()
        if findings:
            self.run()
            raise RuntimeError("behavioural evidence findings cannot establish a baseline")
        return super().establish_baseline()


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> BehaviouralEvidence:
    """Bind the hard behavioural-evidence rule to a consumer configuration."""
    return BehaviouralEvidence.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """Standalone probe; consumers normally invoke the configured catalogue."""
    del argv
    return build({}).run()


if __name__ == "__main__":
    sys.exit(main())
