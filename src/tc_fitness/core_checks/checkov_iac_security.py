"""CORE check: require a clean Checkov scan of the configured IaC directory.

Every Checkov finding blocks. Parsing failures, malformed reports, unavailable
executables, and scanner execution errors also block because the scan has not
proved that the IaC tree is clean.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path, PurePosixPath
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.lib import REPO_ROOT
from tc_fitness.lib import remediation as _remediation

DEFAULT_SCAN_DIR = "."
DEFAULT_FRAMEWORK = "bicep"
DEFAULT_TIMEOUT = 180
_PARSING_ERRORS_KEY = "parsing_errors"

REMEDIATION = _remediation(
    fix="remediate every Checkov finding and correct every IaC parsing error before merging.",
    nxt="re-run this check and confirm Checkov reports zero findings and zero parsing errors.",
    run="python -m tc_fitness.core_checks.checkov_iac_security",
    passing="Checkov completes successfully with zero policy findings and zero parsing errors",
    forbidden="IaC is admitted when Checkov reports a policy finding, parsing error, or execution failure",
)


class CheckovScanError(RuntimeError):
    """The scanner did not produce a complete, trustworthy report."""


def _diff_paths(repo_root: Path, base_ref: str) -> list[str]:
    """Resolve one merge base and its changed paths; refuse an ambiguous diff."""
    if not base_ref or base_ref.startswith("-") or any(c.isspace() for c in base_ref):
        raise CheckovScanError("diff base is invalid")
    git = shutil.which("git")
    if git is None:
        raise CheckovScanError("diff cannot be computed: git is unavailable")
    try:
        base = subprocess.run(
            [git, "rev-parse", "--verify", f"{base_ref}^{{commit}}"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if base.returncode != 0:
            raise CheckovScanError(f"diff base {base_ref!r} cannot be resolved")
        merge_base = subprocess.run(
            [git, "merge-base", "--all", base.stdout.strip(), "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        bases = merge_base.stdout.splitlines()
        if merge_base.returncode != 0 or len(bases) != 1:
            raise CheckovScanError("diff base is missing or ambiguous")
        diff = subprocess.run(
            [git, "diff", "--name-only", "-z", "--no-renames", f"{bases[0]}...HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise CheckovScanError(f"diff cannot be computed: {exc}") from exc
    if diff.returncode != 0:
        raise CheckovScanError("diff cannot be computed")
    return [path for path in diff.stdout.split("\0") if path]


def _local_modules(path: Path) -> list[str]:
    """Read local module references with Checkov's Bicep parser dependency."""
    try:
        from pycep import BicepParser

        parsed = BicepParser().parse(file_path=path)
    except Exception as exc:
        raise CheckovScanError(f"Bicep dependency parsing failed for {path}: {exc}") from exc
    modules = parsed.get("modules", {})
    paths: list[str] = []
    for module in modules.values():
        if module["type"] != "local":
            continue
        detail = module["detail"]
        local_path = detail.get("path")
        if not isinstance(local_path, str):
            raise CheckovScanError(f"local Bicep module path is invalid in {path}")
        paths.append(local_path)
    return paths


def checkov_binary() -> str | None:
    """Return the installed Checkov executable, or ``None`` when it is absent."""
    return shutil.which("checkov")


def _validated_report(report: Any) -> tuple[list[dict[str, Any]], int]:
    """Return one report's failed checks and parse-error count, or refuse it."""
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return failed, parsing_errors


def _parse_report(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON into one validated report of the whole scan.

    Checkov emits a single report object, or — when the scan spans more than one
    framework — a list of them. A list is aggregated into the same shape, so a
    finding raised under any framework still blocks. An empty list carries no
    report at all, so it cannot evidence a clean tree and is refused.
    """
    try:
        payloads = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if isinstance(payloads, list) and not payloads:
        raise CheckovScanError("Checkov JSON report list is empty")
    reports = payloads if isinstance(payloads, list) else [payloads]
    failed: list[dict[str, Any]] = []
    parsing_errors = 0
    for report in reports:
        report_failed, report_parsing_errors = _validated_report(report)
        failed.extend(report_failed)
        parsing_errors += report_parsing_errors
    return {"results": {"failed_checks": failed}, "summary": {_PARSING_ERRORS_KEY: parsing_errors}}


def run_checkov(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
    files: Sequence[Path] | None = None,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None

    return _run_checkov(binary, scan_dir, framework=framework, timeout=timeout, files=files)


def _run_checkov(
    binary: str,
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
    files: Sequence[Path] | None = None,
) -> tuple[int, dict[str, Any]]:
    """Run a previously resolved Checkov executable."""
    target = ["-f", *(str(path) for path in files)] if files is not None else ["-d", str(scan_dir)]
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", encoding="utf-8") as config_file:
            config_file.write("{}\n")
            config_file.flush()
            clean_env = {
                key: value
                for key, value in os.environ.items()
                if not key.startswith(("CKV_", "CHECKOV_", "BC_", "PRISMA_"))
            }
            process = subprocess.run(
                [
                    binary,
                    *target,
                    "--framework",
                    framework,
                    "--output",
                    "json",
                    "--quiet",
                    "--compact",
                    "--skip-check",
                    "",
                    "--baseline",
                    "",
                    "--config-file",
                    config_file.name,
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout,
                env=clean_env,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def _finding_line(failed_check: Mapping[str, Any], *, file_path: str | None = None) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = file_path if file_path is not None else str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def _finding_path(
    failed_check: Mapping[str, Any],
    *,
    scan_path: Path,
    scan_dir: str,
    repo_root: Path | None = None,
) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        if repo_root is not None:
            try:
                return Path(absolute).resolve().relative_to(repo_root).as_posix()
            except ValueError:
                pass
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


class CheckovIacSecurity:
    """Absolute IaC-security gate: all findings and parse errors fail."""

    name = "checkov_iac_security"

    def __init__(
        self,
        repo_root: Path | None = None,
        *,
        scan_dir: str = DEFAULT_SCAN_DIR,
        framework: str = DEFAULT_FRAMEWORK,
        timeout: int = DEFAULT_TIMEOUT,
        changed_files: Sequence[str] | None = None,
        base_ref: str | None = None,
    ) -> None:
        self._repo_root = (repo_root if repo_root is not None else REPO_ROOT).resolve()
        self._scan_dir = scan_dir
        self._framework = framework
        self._timeout = timeout
        self._changed_files = changed_files
        self._base_ref = base_ref

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
        changed_files: Sequence[str] | None = None,
    ) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
            changed_files=changed_files if changed_files is not None else config.get("changed_files"),
            base_ref=config.get("base_ref") if changed_files is None else None,
        )

    @property
    def scan_path(self) -> Path:
        """The configured IaC path resolved from the repository root."""
        return (self._repo_root / self._scan_dir).resolve()

    def _scan_files(self) -> tuple[Path, ...] | None:
        """Return affected Bicep files and local modules, or None for full mode."""
        if self._changed_files is not None and self._base_ref is not None:
            raise CheckovScanError("changed files and diff base cannot both be set")
        if self._changed_files is None and self._base_ref is None:
            return None
        changed = (
            _diff_paths(self._repo_root, self._base_ref)
            if self._base_ref is not None
            else self._changed_files
        )
        if not isinstance(changed, Sequence) or isinstance(changed, (str, bytes)):
            raise CheckovScanError("changed files must be a list of repo-relative paths")
        try:
            self.scan_path.relative_to(self._repo_root)
        except ValueError as exc:
            raise CheckovScanError("scan directory escapes the repository") from exc
        if not self.scan_path.is_dir():
            raise CheckovScanError("scan directory does not exist")
        changed_paths: set[Path] = set()
        for rel in changed:
            if not isinstance(rel, str) or not rel or "\0" in rel or Path(rel).is_absolute():
                raise CheckovScanError("changed file path is invalid")
            path = (self._repo_root / rel).resolve()
            try:
                path.relative_to(self._repo_root)
            except ValueError as exc:
                raise CheckovScanError(f"changed file escapes the repository: {rel}") from exc
            if path.suffix == ".bicep":
                changed_paths.add(path)
        if not changed_paths:
            return ()

        # Index the in-scope templates and every local module they can reach.
        # The reverse edges make a changed module affect its unchanged callers;
        # missing targets stay in the graph so deletion is detected below.
        dependencies: dict[Path, tuple[Path, ...]] = {}
        importers: dict[Path, set[Path]] = {}
        to_index = list(self.scan_path.rglob("*.bicep"))
        while to_index:
            path = to_index.pop().resolve()
            if path in dependencies:
                continue
            if not path.is_relative_to(self._repo_root):
                raise CheckovScanError(f"Bicep module escapes the repository: {path}")
            if not path.exists():
                continue
            if not path.is_file():
                raise CheckovScanError(f"Bicep path is not a file: {path}")
            targets = tuple((path.parent / module).resolve() for module in _local_modules(path))
            dependencies[path] = targets
            for target in targets:
                if not target.is_relative_to(self._repo_root):
                    raise CheckovScanError(f"local Bicep module escapes the repository: {target}")
                importers.setdefault(target, set()).add(path)
                to_index.append(target)

        affected_importers: set[Path] = set()
        to_visit = list(changed_paths)
        while to_visit:
            for importer in importers.get(to_visit.pop(), ()):
                if importer not in affected_importers:
                    affected_importers.add(importer)
                    to_visit.append(importer)

        pending = [
            path
            for path in changed_paths | affected_importers
            if path.is_relative_to(self.scan_path) and path.exists()
        ]
        selected: set[Path] = set()
        while pending:
            path = pending.pop()
            if path in selected:
                continue
            selected.add(path)
            for dependency in dependencies.get(path, ()):
                if dependency.suffix != ".bicep" or not dependency.is_file():
                    raise CheckovScanError(f"local Bicep module is missing or invalid: {dependency}")
                pending.append(dependency)
        return tuple(sorted(selected))

    def evaluate(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            files = self._scan_files()
            binary = checkov_binary()
            if binary is None:
                return (
                    False,
                    [],
                    {
                        "unavailable": True,
                        "execution_error": False,
                        "exit_code": None,
                        "failed": 0,
                        _PARSING_ERRORS_KEY: 0,
                        "findings": [],
                    },
                )
            if files == ():
                return (
                    True,
                    [],
                    {
                        "unavailable": False,
                        "execution_error": False,
                        "exit_code": 0,
                        "failed": 0,
                        _PARSING_ERRORS_KEY: 0,
                        "findings": [],
                    },
                )
            result = _run_checkov(
                binary,
                self.scan_path,
                framework=self._framework,
                timeout=self._timeout,
                files=files,
            )
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [
            _finding_line(
                item,
                file_path=f"/{_finding_path(item, scan_path=self.scan_path, scan_dir=self._scan_dir, repo_root=self._repo_root)}",
            )
            for item in failed
        ]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def run(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            finding_path = _finding_path(
                finding, scan_path=self.scan_path, scan_dir=self._scan_dir, repo_root=self._repo_root
            )
            report_finding(
                "checkov-policy",
                finding_path,
                _finding_line(finding, file_path=f"/{finding_path}"),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    changed_files: Sequence[str] | None = None,
) -> CheckovIacSecurity:
    """Factory used by the CORE check catalogue."""
    return CheckovIacSecurity.from_config(config, repo_root=repo_root, changed_files=changed_files)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, help="repository root to scan")
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--changed-files-from", type=Path, help="repo-relative changed paths, one per line")
    scope.add_argument("--base-ref", help="git ref to compare with HEAD through its merge base")
    args = parser.parse_args(argv)
    changed_files = None
    if args.changed_files_from is not None:
        try:
            changed_files = args.changed_files_from.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            print(f"ERROR checkov_iac_security: changed-file input cannot be read: {exc}")
            return 2
    return CheckovIacSecurity(
        repo_root=args.repo_root, changed_files=changed_files, base_ref=args.base_ref
    ).run()


if __name__ == "__main__":
    import sys

    sys.exit(main())
