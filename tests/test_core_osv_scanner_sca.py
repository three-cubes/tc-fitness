"""Behavioural tests for the OSV software-composition-analysis contract."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from tc_fitness.core_checks.osv_scanner_sca import (
    OsvScannerSca,
    ScanExecution,
    ScanStatus,
    build,
)


def _report(*vulnerability_ids: str) -> dict[str, object]:
    return {
        "results": [
            {
                "packages": [
                    {"vulnerabilities": [{"id": vulnerability_id} for vulnerability_id in vulnerability_ids]}
                ]
            }
        ]
    }


def test_missing_required_scanner_is_incomplete_and_cannot_pass(tmp_path: Path) -> None:
    rule = OsvScannerSca(
        tmp_path,
        scanner_version="2.2.4",
        lockfiles=("uv.lock",),
        required=True,
        runner=lambda _root, _lockfiles, _version: ScanExecution(
            status=ScanStatus.MISSING_TOOL,
            detail="osv-scanner is not on PATH",
        ),
    )

    passed, findings, execution = rule.evaluate()

    assert passed is False
    assert findings == []
    assert execution.status is ScanStatus.MISSING_TOOL
    assert rule.run() == 1


@pytest.mark.parametrize("status", [ScanStatus.MISSING_TOOL, ScanStatus.INCOMPLETE])
def test_only_an_executed_clean_scan_can_return_green(tmp_path: Path, status: ScanStatus) -> None:
    rule = OsvScannerSca(
        tmp_path,
        scanner_version="2.2.4",
        lockfiles=("uv.lock",),
        runner=lambda _root, _lockfiles, _version: ScanExecution(status=status, detail="not executed"),
    )

    assert rule.run() != 0


def test_executed_clean_scan_passes(tmp_path: Path) -> None:
    rule = OsvScannerSca(
        tmp_path,
        scanner_version="2.2.4",
        lockfiles=("uv.lock",),
        runner=lambda _root, _lockfiles, _version: ScanExecution(
            status=ScanStatus.EXECUTED,
            report=_report(),
        ),
    )

    assert rule.run() == 0


def test_executed_scan_with_any_finding_fails_without_grandfathering(tmp_path: Path) -> None:
    rule = OsvScannerSca(
        tmp_path,
        scanner_version="2.2.4",
        lockfiles=("uv.lock",),
        runner=lambda _root, _lockfiles, _version: ScanExecution(
            status=ScanStatus.EXECUTED,
            report=_report("GHSA-example"),
        ),
    )

    passed, findings, execution = rule.evaluate()

    assert execution.status is ScanStatus.EXECUTED
    assert passed is False
    assert findings == ["GHSA-example"]
    assert rule.run() == 1


def test_config_requires_an_exact_scanner_pin(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="scanner_version"):
        build({"required": True, "lockfiles": ["uv.lock"]}, repo_root=tmp_path)

    rule = build(
        {"required": True, "scanner_version": "2.2.4", "lockfiles": ["uv.lock", "pnpm-lock.yaml"]},
        repo_root=tmp_path,
    )
    assert rule.scanner_version == "2.2.4"
    assert rule.required is True
    assert rule.lockfiles == ("uv.lock", "pnpm-lock.yaml")


def _scanner_script(path: Path, *, version: str = "2.2.4", report: str = '{"results": []}') -> Path:
    scanner = path / "osv-scanner"
    scanner.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = "--version" ]; then\n'
        f"  printf '%s\\n' 'osv-scanner version: {version}'\n"
        "  exit 0\n"
        "fi\n"
        f"printf '%s\\n' '{report}'\n",
        encoding="utf-8",
    )
    scanner.chmod(0o755)
    return scanner


def test_real_executable_boundary_accepts_exact_version_and_clean_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _scanner_script(tmp_path)
    (tmp_path / "uv.lock").write_text("fixture\n", encoding="utf-8")
    monkeypatch.setenv("PATH", os.fspath(tmp_path))

    rule = OsvScannerSca(tmp_path, scanner_version="2.2.4", lockfiles=("uv.lock",))

    assert rule.run() == 0


def test_real_executable_boundary_rejects_wrong_scanner_version(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _scanner_script(tmp_path, version="2.2.3")
    (tmp_path / "uv.lock").write_text("fixture\n", encoding="utf-8")
    monkeypatch.setenv("PATH", os.fspath(tmp_path))

    rule = OsvScannerSca(tmp_path, scanner_version="2.2.4", lockfiles=("uv.lock",))

    passed, findings, execution = rule.evaluate()
    assert passed is False
    assert findings == []
    assert execution.status is ScanStatus.INCOMPLETE
    assert "expected osv-scanner 2.2.4, found 2.2.3" in execution.detail


def test_real_executable_boundary_rejects_missing_declared_lockfile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _scanner_script(tmp_path)
    monkeypatch.setenv("PATH", os.fspath(tmp_path))

    rule = OsvScannerSca(tmp_path, scanner_version="2.2.4", lockfiles=("uv.lock",))

    passed, _, execution = rule.evaluate()
    assert passed is False
    assert execution.status is ScanStatus.INCOMPLETE
    assert execution.detail == "declared lockfile(s) missing: uv.lock"


@pytest.mark.parametrize(
    "report",
    [
        "{}",
        '{"results": null}',
        '{"results": [{}]}',
        '{"results": [{"packages": {}}]}',
        '{"results": [{"packages": [{"vulnerabilities": {}}]}]}',
        '{"results": [{"packages": [{"vulnerabilities": [{}]}]}]}',
    ],
)
def test_real_executable_boundary_rejects_malformed_or_partial_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    report: str,
) -> None:
    _scanner_script(tmp_path, report=report)
    (tmp_path / "uv.lock").write_text("fixture\n", encoding="utf-8")
    monkeypatch.setenv("PATH", os.fspath(tmp_path))

    rule = OsvScannerSca(tmp_path, scanner_version="2.2.4", lockfiles=("uv.lock",))

    passed, findings, execution = rule.evaluate()
    assert passed is False
    assert findings == []
    assert execution.status is ScanStatus.INCOMPLETE
    assert "report" in execution.detail
