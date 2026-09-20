"""CORE check: require a clean Checkov scan of the configured IaC directory.

Every Checkov finding blocks. Parsing failures, malformed reports, unavailable
executables, and scanner execution errors also block because the scan has not
proved that the IaC tree is clean.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from collections.abc import Mapping
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
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def _finding_line(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def _finding_path(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
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
    ) -> None:
        self._repo_root = (repo_root if repo_root is not None else REPO_ROOT).resolve()
        self._scan_dir = scan_dir
        self._framework = framework
        self._timeout = timeout

    @classmethod
    def from_config(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @property
    def scan_path(self) -> Path:
        """The configured IaC path resolved from the repository root."""
        return (self._repo_root / self._scan_dir).resolve()

    def evaluate(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
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
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
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
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
    """Factory used by the CORE check catalogue."""
    return CheckovIacSecurity.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


if __name__ == "__main__":
    import sys

    sys.exit(main())
