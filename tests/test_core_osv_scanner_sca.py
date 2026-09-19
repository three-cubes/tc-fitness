"""Behavioural tests for the OSV software-composition-analysis contract."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness.catalogue import RuleEntry
from tc_fitness.core_checks.osv_scanner_sca import (
    OsvScannerSca,
    ScanExecution,
    ScanStatus,
    _reported_version,
    build,
    execute_scan,
    vulnerability_ids,
)
from tc_fitness.runner import RunnerConfig, _load_core_check

pytestmark = pytest.mark.integration


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


def test_required_scan_requires_at_least_one_lockfile(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="at least one lockfile"):
        OsvScannerSca(tmp_path, scanner_version="2.2.4", required=True)


def test_vulnerability_ids_are_deduplicated_and_blank_ids_are_ignored() -> None:
    report = {
        "results": [
            {"packages": [{"vulnerabilities": [{"id": "GHSA-2"}, {"id": " "}, {"id": "GHSA-1"}]}]},
            {"packages": [{"vulnerabilities": [{"id": "GHSA-1"}]}]},
        ]
    }

    assert vulnerability_ids(report) == ["GHSA-1", "GHSA-2"]


def test_real_osv_scanner_executes_against_the_repository_lockfile() -> None:
    scanner = shutil.which("osv-scanner")
    if scanner is None:
        pytest.skip("real OSV scanner is installed by the SCA development/CI toolchain")
    repo_root = Path(__file__).parents[1]
    probe = subprocess.run([scanner, "--version"], capture_output=True, text=True, check=True, timeout=10)
    version = probe.stdout + probe.stderr
    expected_version = version.split("version:", 1)[1].splitlines()[0].strip()

    execution = execute_scan(repo_root, ("uv.lock",), expected_version, timeout=60)

    assert execution.status is ScanStatus.EXECUTED
    assert execution.report is not None
    assert isinstance(execution.report.get("results"), list)


def test_real_scanner_rejects_version_mismatch_and_missing_lockfiles() -> None:
    scanner = shutil.which("osv-scanner")
    if scanner is None:
        pytest.skip("real OSV scanner is installed by the SCA development/CI toolchain")
    repo_root = Path(__file__).parents[1]
    probe = subprocess.run([scanner, "--version"], capture_output=True, text=True, check=True, timeout=10)
    actual_version = probe.stdout + probe.stderr
    actual_version = actual_version.split("version:", 1)[1].splitlines()[0].strip()

    mismatch = execute_scan(repo_root, ("uv.lock",), "0.0.0")
    missing = execute_scan(repo_root, ("missing.lock",), actual_version)

    assert mismatch.status is ScanStatus.INCOMPLETE
    assert "expected osv-scanner 0.0.0" in mismatch.detail
    assert missing.status is ScanStatus.INCOMPLETE
    assert "missing.lock" in missing.detail


def test_scanner_is_reported_missing_in_an_isolated_path(tmp_path: Path) -> None:
    source_root = Path(__file__).parents[1] / "src"
    command = (
        "from pathlib import Path; "
        "from tc_fitness.core_checks.osv_scanner_sca import execute_scan; "
        "result = execute_scan(Path.cwd(), (), '2.2.4'); print(result.status.value)"
    )
    result = subprocess.run(
        [sys.executable, "-c", command],
        cwd=tmp_path,
        env={**os.environ, "PATH": str(tmp_path), "PYTHONPATH": str(source_root)},
        capture_output=True,
        check=True,
        text=True,
    )

    assert result.stdout.strip() == ScanStatus.MISSING_TOOL.value


def test_zero_timeout_is_captured_as_incomplete_probe() -> None:
    if shutil.which("osv-scanner") is None:
        pytest.skip("real OSV scanner is installed by the SCA development/CI toolchain")

    result = execute_scan(Path(__file__).parents[1], (), "2.2.4", timeout=0)

    assert result.status is ScanStatus.INCOMPLETE
    assert "version probe failed" in result.detail


def test_real_process_boundary_reports_nonzero_version_probe() -> None:
    false_binary = shutil.which("false")
    if false_binary is None:
        pytest.skip("the host has no standard false utility")

    result = _reported_version(false_binary, timeout=10)

    assert isinstance(result, ScanExecution)
    assert result.status is ScanStatus.INCOMPLETE
    assert "version probe returned 1" in result.detail


def test_real_osv_scanner_rejects_a_lockfile_without_package_sources() -> None:
    scanner = shutil.which("osv-scanner")
    if scanner is None:
        pytest.skip("real OSV scanner is installed by the SCA development/CI toolchain")
    repo_root = Path(__file__).parents[1]
    probe = subprocess.run([scanner, "--version"], capture_output=True, text=True, check=True, timeout=10)
    output = probe.stdout + probe.stderr
    version = output.split("version:", 1)[1].splitlines()[0].strip()
    lockfile = "tests/check_contracts/osv_scanner_sca/unavailable/uv.lock"

    result = execute_scan(repo_root, (lockfile,), version, timeout=60)

    assert result.status is ScanStatus.INCOMPLETE
    assert result.detail.startswith("scan returned ")


def test_evaluate_rejects_an_incomplete_report_from_runner(tmp_path: Path) -> None:
    rule = OsvScannerSca(
        tmp_path,
        scanner_version="2.2.4",
        lockfiles=("uv.lock",),
        runner=lambda *_args: ScanExecution(ScanStatus.EXECUTED, report={"results": {}}),
    )

    passed, findings, execution = rule.evaluate()

    assert passed is False
    assert findings == []
    assert execution.status is ScanStatus.INCOMPLETE


def test_evaluate_without_configuration_is_a_pass(tmp_path: Path) -> None:
    passed, findings, execution = build({}, repo_root=tmp_path).evaluate()

    assert passed is True
    assert findings == []
    assert execution.status is ScanStatus.EXECUTED
    assert execution.report == {"results": []}


def test_osv_scan_has_no_baseline_operation(tmp_path: Path) -> None:
    rule = OsvScannerSca(tmp_path, scanner_version="2.2.4", lockfiles=("uv.lock",))

    with pytest.raises(RuntimeError, match="no baseline"):
        rule.establish_baseline()


def _scanner_script(
    path: Path,
    *,
    version: str = "2.2.4",
    report: str = '{"results": []}',
    exit_code: int = 0,
) -> Path:
    scanner = path / "osv-scanner"
    scanner.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = "--version" ]; then\n'
        f"  printf '%s\\n' 'osv-scanner version: {version}'\n"
        "  exit 0\n"
        "fi\n"
        f"printf '%s\\n' '{report}'\n"
        f"exit {exit_code}\n",
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


@pytest.mark.parametrize("version", ["2.2.4-rc.1", "2.2.4+dirty"])
def test_real_executable_boundary_rejects_scanner_version_suffixes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    version: str,
) -> None:
    _scanner_script(tmp_path, version=version)
    (tmp_path / "uv.lock").write_text("fixture\n", encoding="utf-8")
    monkeypatch.setenv("PATH", os.fspath(tmp_path))

    rule = OsvScannerSca(tmp_path, scanner_version="2.2.4", lockfiles=("uv.lock",))

    passed, findings, execution = rule.evaluate()

    assert passed is False
    assert findings == []
    assert execution.status is ScanStatus.INCOMPLETE
    assert f"expected osv-scanner 2.2.4, found {version}" in execution.detail


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


@pytest.mark.parametrize("lockfile", ["../outside.lock", "symlink.lock"])
def test_real_executable_boundary_rejects_lockfiles_outside_the_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    lockfile: str,
) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    external_lockfile = tmp_path / "outside.lock"
    external_lockfile.write_text("fixture\n", encoding="utf-8")
    if lockfile == "symlink.lock":
        (repo_root / lockfile).symlink_to(external_lockfile)
    _scanner_script(tmp_path)
    monkeypatch.setenv("PATH", os.fspath(tmp_path))

    rule = OsvScannerSca(repo_root, scanner_version="2.2.4", lockfiles=(lockfile,))

    passed, findings, execution = rule.evaluate()

    assert passed is False
    assert findings == []
    assert execution.status is ScanStatus.INCOMPLETE
    assert "must resolve beneath repository root" in execution.detail


def test_real_executable_boundary_rejects_an_absolute_lockfile_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    external_lockfile = tmp_path / "outside.lock"
    external_lockfile.write_text("fixture\n", encoding="utf-8")
    _scanner_script(tmp_path)
    monkeypatch.setenv("PATH", os.fspath(tmp_path))

    rule = OsvScannerSca(repo_root, scanner_version="2.2.4", lockfiles=(str(external_lockfile),))

    passed, findings, execution = rule.evaluate()

    assert passed is False
    assert findings == []
    assert execution.status is ScanStatus.INCOMPLETE
    assert "must be repository-relative" in execution.detail


def test_real_executable_boundary_rejects_clean_report_with_exit_one(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _scanner_script(tmp_path, exit_code=1)
    (tmp_path / "uv.lock").write_text("fixture\n", encoding="utf-8")
    monkeypatch.setenv("PATH", os.fspath(tmp_path))

    rule = OsvScannerSca(tmp_path, scanner_version="2.2.4", lockfiles=("uv.lock",))

    passed, findings, execution = rule.evaluate()

    assert passed is False
    assert findings == []
    assert execution.status is ScanStatus.INCOMPLETE
    assert "exit 1 with no vulnerabilities" in execution.detail


def test_unconfigured_core_check_is_a_vacuous_pass(tmp_path: Path) -> None:
    entry = RuleEntry(id="osv", gate="osv", check="core:osv_scanner_sca")

    run = _load_core_check(entry, RunnerConfig(repo_root=tmp_path))

    assert run() == 0


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
