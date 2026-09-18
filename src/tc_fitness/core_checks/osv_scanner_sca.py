"""CORE check: execute a pinned OSV scan and reject every vulnerability.

The consumer owns the exact scanner version and lockfile list.  This check
owns verdict semantics: only a completed, parseable, clean scan can pass.
Missing tooling, a version mismatch, an absent lockfile, an execution error,
or malformed output is incomplete evidence and therefore cannot become green.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from tc_fitness.lib import REPO_ROOT

DEFAULT_TIMEOUT = 180


class ScanStatus(StrEnum):
    """Terminal evidence states for one scanner invocation."""

    EXECUTED = "executed"
    MISSING_TOOL = "missing-tool"
    INCOMPLETE = "incomplete"


@dataclass(frozen=True)
class ScanExecution:
    """Scanner evidence kept separate from the vulnerability verdict."""

    status: ScanStatus
    report: dict[str, Any] | None = None
    detail: str = ""


Runner = Callable[[Path, tuple[str, ...], str], ScanExecution]


def _reported_version(binary: str, *, timeout: int) -> ScanExecution | str:
    try:
        process = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"version probe failed: {exc}")
    output = f"{process.stdout}\n{process.stderr}".strip()
    match = re.search(r"(?<!\d)(\d+\.\d+\.\d+)(?!\d)", output)
    if process.returncode != 0 or match is None:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"version probe returned {process.returncode}: {output[:240]}",
        )
    return match.group(1)


def execute_scan(
    repo_root: Path,
    lockfiles: tuple[str, ...],
    scanner_version: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
) -> ScanExecution:
    """Execute the real scanner and retain why evidence is incomplete."""
    binary = shutil.which("osv-scanner")
    if binary is None:
        return ScanExecution(ScanStatus.MISSING_TOOL, detail="osv-scanner is not on PATH")

    reported = _reported_version(binary, timeout=timeout)
    if isinstance(reported, ScanExecution):
        return reported
    if reported != scanner_version:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"expected osv-scanner {scanner_version}, found {reported}",
        )

    paths = tuple(repo_root / lockfile for lockfile in lockfiles)
    missing = [lockfile for lockfile, path in zip(lockfiles, paths, strict=True) if not path.is_file()]
    if missing:
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"declared lockfile(s) missing: {', '.join(missing)}",
        )

    command = [binary, "scan", "source", "--format", "json"]
    for path in paths:
        command.extend(("--lockfile", str(path)))
    try:
        process = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan failed: {exc}")
    if process.returncode not in (0, 1) or not process.stdout.strip():
        return ScanExecution(
            ScanStatus.INCOMPLETE,
            detail=f"scan returned {process.returncode}: {process.stderr.strip()[:240]}",
        )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan output was not JSON: {exc}")
    report_error = _report_error(report)
    if report_error is not None:
        return ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}")
    return ScanExecution(ScanStatus.EXECUTED, report=report)


def _report_error(report: object) -> str | None:
    if not isinstance(report, dict) or "results" not in report or not isinstance(report["results"], list):
        return "results must be present as a list"
    for result in report["results"]:
        if not isinstance(result, Mapping) or not isinstance(result.get("packages"), list):
            return "every result must contain a packages list"
        for package in result["packages"]:
            if not isinstance(package, Mapping) or not isinstance(package.get("vulnerabilities"), list):
                return "every package must contain a vulnerabilities list"
            for vulnerability in package["vulnerabilities"]:
                if not isinstance(vulnerability, Mapping) or not str(vulnerability.get("id", "")).strip():
                    return "every vulnerability must contain a non-empty id"
    return None


def vulnerability_ids(report: Mapping[str, Any]) -> list[str]:
    """Return every reported advisory id without a suppression/baseline path."""
    found: list[str] = []
    for result in report.get("results", []) or []:
        for package in result.get("packages", []) or []:
            for vulnerability in package.get("vulnerabilities", []) or []:
                vulnerability_id = str(vulnerability.get("id", "")).strip()
                if vulnerability_id:
                    found.append(vulnerability_id)
    return sorted(set(found))


class OsvScannerSca:
    """Pinned, no-grandfathering SCA contract for consumer lockfiles."""

    name = "osv-scanner-sca"

    def __init__(
        self,
        repo_root: Path | None = None,
        *,
        scanner_version: str,
        lockfiles: Sequence[str] = (),
        required: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        runner: Runner | None = None,
    ) -> None:
        if not re.fullmatch(r"\d+\.\d+\.\d+", scanner_version):
            raise ValueError("scanner_version must be an exact x.y.z pin")
        if required and not lockfiles:
            raise ValueError("required OSV scanning must declare at least one lockfile")
        self.repo_root = (repo_root or REPO_ROOT).resolve()
        self.scanner_version = scanner_version
        self.lockfiles = tuple(lockfiles)
        self.required = required
        self.timeout = timeout
        self._runner = runner

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> OsvScannerSca:
        return cls(
            repo_root,
            scanner_version=str(config.get("scanner_version", "")),
            lockfiles=tuple(str(value) for value in config.get("lockfiles", ())),
            required=bool(config.get("required", True)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    def _execute(self) -> ScanExecution:
        if self._runner is not None:
            return self._runner(self.repo_root, self.lockfiles, self.scanner_version)
        return execute_scan(
            self.repo_root,
            self.lockfiles,
            self.scanner_version,
            timeout=self.timeout,
        )

    def evaluate(self) -> tuple[bool, list[str], ScanExecution]:
        execution = self._execute()
        if execution.status is not ScanStatus.EXECUTED or execution.report is None:
            return False, [], execution
        report_error = _report_error(execution.report)
        if report_error is not None:
            return (
                False,
                [],
                ScanExecution(ScanStatus.INCOMPLETE, detail=f"scan report is incomplete: {report_error}"),
            )
        findings = vulnerability_ids(execution.report)
        return not findings, findings, execution

    def run(self) -> int:
        passed, findings, execution = self.evaluate()
        if execution.status is not ScanStatus.EXECUTED:
            print(
                f"INCOMPLETE osv_scanner_sca ({execution.status.value}): {execution.detail}. "
                f"fix: install osv-scanner {self.scanner_version} and ensure every declared lockfile exists; "
                "next: re-run the full fitness gate; run: osv-scanner --version"
            )
            return 1
        if not passed:
            print(
                f"FAIL osv_scanner_sca ({len(findings)} vulnerable advisory id(s)): "
                f"{', '.join(findings)}. fix: update affected dependencies; "
                "next: refresh lockfiles and re-run the full fitness gate; "
                f"run: osv-scanner scan source {' '.join(f'--lockfile {path}' for path in self.lockfiles)}"
            )
            return 1
        print(
            f"PASS osv_scanner_sca (executed osv-scanner {self.scanner_version}; "
            f"{len(self.lockfiles)} lockfile(s); 0 vulnerabilities)"
        )
        return 0

    def establish_baseline(self) -> Path:
        raise RuntimeError("osv_scanner_sca has no baseline: every finding must be remediated")


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> OsvScannerSca:
    return OsvScannerSca.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=OsvScannerSca.name)
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--scanner-version", required=True)
    parser.add_argument("--lockfile", action="append", default=[])
    args = parser.parse_args(argv)
    return OsvScannerSca(
        args.repo_root,
        scanner_version=args.scanner_version,
        lockfiles=args.lockfile,
    ).run()


if __name__ == "__main__":
    raise SystemExit(main())
