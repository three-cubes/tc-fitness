"""Real Checkov contract tests for the absolute IaC security gate."""

from __future__ import annotations

import json
import os
import runpy
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks.checkov_iac_security import (
    CheckovIacSecurity,
    CheckovScanError,
    _finding_line,
    _finding_path,
    _parse_report,
    build,
    checkov_binary,
    main,
    run_checkov,
)

pytestmark = pytest.mark.integration
CONTRACT_ROOT = Path(__file__).parent / "check_contracts" / "checkov_iac_security"


def test_compliant_storage_fixture_passes_real_checkov() -> None:
    rule = CheckovIacSecurity(CONTRACT_ROOT / "compliant", scan_dir="infra")

    passed, errors, meta = rule.evaluate()

    assert checkov_binary()
    assert (passed, errors) == (True, [])
    assert meta == {
        "unavailable": False,
        "execution_error": False,
        "exit_code": 0,
        "failed": 0,
        "parsing_errors": 0,
        "findings": [],
    }


def test_network_open_storage_fails_real_checkov_with_actionable_finding() -> None:
    rule = CheckovIacSecurity(CONTRACT_ROOT / "violation", scan_dir="infra")

    passed, errors, meta = rule.evaluate()

    assert not passed
    assert meta["failed"] >= 1
    assert meta["parsing_errors"] == 0
    assert any("CKV_AZURE_35" in line for line in errors)
    assert any("network access" in line.lower() for line in errors)


def test_violation_run_returns_failure_and_emits_structured_checkov_finding(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rule = CheckovIacSecurity(CONTRACT_ROOT / "violation", scan_dir="infra")

    assert rule.run() == 1
    output = capsys.readouterr().out
    assert "CKV_AZURE_35" in output
    assert "FAIL checkov_iac_security" in output


def test_config_factory_and_public_run_use_the_configured_fixture(capsys: pytest.CaptureFixture[str]) -> None:
    rule = build(
        {"scan_dir": "compliant/infra", "framework": "bicep", "timeout": 60},
        repo_root=CONTRACT_ROOT,
    )

    assert rule.scan_path == (CONTRACT_ROOT / "compliant" / "infra").resolve()
    assert rule.run() == 0
    assert "PASS checkov_iac_security" in capsys.readouterr().out


def test_direct_cli_runs_the_real_scan_from_repository_root() -> None:
    assert main(["--repo-root", str(CONTRACT_ROOT / "compliant")]) == 0


def test_python_module_entrypoint_runs_the_real_scan() -> None:
    from tc_fitness.core_checks import checkov_iac_security

    original_argv = sys.argv
    sys.argv = [
        str(Path(checkov_iac_security.__file__)),
        "--repo-root",
        str(CONTRACT_ROOT / "compliant"),
    ]
    try:
        with pytest.raises(SystemExit) as result:
            runpy.run_path(str(Path(checkov_iac_security.__file__)), run_name="__main__")
        assert result.value.code == 0
    finally:
        sys.argv = original_argv


def test_missing_scanner_is_an_error_not_a_clean_result(tmp_path: Path) -> None:
    process = subprocess.run(
        [
            sys.executable,
            "-c",
            "from pathlib import Path; import json, sys; "
            "from tc_fitness.core_checks.checkov_iac_security import CheckovIacSecurity; "
            "print(json.dumps(CheckovIacSecurity(Path(sys.argv[1])).evaluate()))",
            str(tmp_path),
        ],
        env={**os.environ, "PATH": ""},
        capture_output=True,
        text=True,
        check=False,
    )

    assert process.returncode == 0
    passed, errors, meta = json.loads(process.stdout)
    assert not passed
    assert errors == []
    assert meta["unavailable"] is True


def test_missing_scanner_run_reports_structured_error_without_test_doubles(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    previous_path = os.environ.get("PATH")
    os.environ["PATH"] = ""
    try:
        rule = CheckovIacSecurity(tmp_path)
        passed, errors, meta = rule.evaluate()
        assert not passed
        assert errors == []
        assert meta["unavailable"] is True
        assert rule.run() == 2
        assert "checkov is unavailable" in capsys.readouterr().out
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path


def test_malformed_scanner_report_is_rejected() -> None:
    with pytest.raises(CheckovScanError, match="invalid JSON"):
        _parse_report("not-json")


def test_incomplete_scanner_report_is_rejected() -> None:
    with pytest.raises(CheckovScanError, match="missing results or summary"):
        _parse_report("{}")


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ("[]", "must be an object"),
        ('{"results": [], "summary": {}}', "missing results or summary"),
        (
            '{"results": {"failed_checks": [null]}, "summary": {"parsing_errors": 0}}',
            "invalid failed_checks",
        ),
        (
            '{"results": {"failed_checks": []}, "summary": {"parsing_errors": "0"}}',
            "invalid parsing_errors",
        ),
        (
            '{"results": {"failed_checks": []}, "summary": {"parsing_errors": true}}',
            "invalid parsing_errors",
        ),
        (
            '{"results": {"failed_checks": []}, "summary": {"parsing_errors": -1}}',
            "invalid parsing_errors",
        ),
    ],
)
def test_malformed_checkov_report_shapes_are_rejected(payload: str, message: str) -> None:
    with pytest.raises(CheckovScanError, match=message):
        _parse_report(payload)


def test_invalid_framework_cannot_turn_missing_report_into_a_pass() -> None:
    rule = CheckovIacSecurity(
        CONTRACT_ROOT / "compliant",
        scan_dir="infra",
        framework="not-a-framework",
    )

    passed, errors, meta = rule.evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors == ["Checkov exited with unexpected status 2"]


def test_checkov_timeout_fails_closed() -> None:
    rule = CheckovIacSecurity(CONTRACT_ROOT / "compliant", scan_dir="infra", timeout=0)

    passed, errors, meta = rule.evaluate()

    assert not passed
    assert meta["execution_error"] is True
    assert errors and "execution failed" in errors[0]


def test_checkov_timeout_is_reported_as_execution_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rule = CheckovIacSecurity(CONTRACT_ROOT / "compliant", scan_dir="infra", timeout=0)

    assert rule.run() == 2
    assert "ERROR checkov_iac_security" in capsys.readouterr().out


def test_actual_parser_failure_fails_the_scan(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "infra" / "main.bicep"
    source.parent.mkdir()
    source.write_text("resource broken 'Microsoft.Storage/storageAccounts@2023-01-01' = {\n  name: }\n")
    rule = CheckovIacSecurity(tmp_path, scan_dir="infra")

    passed, errors, meta = rule.evaluate()

    assert not passed
    assert meta["parsing_errors"] == 1
    assert any("could not parse" in error for error in errors)
    assert rule.run() == 1
    assert "Checkov could not parse 1 IaC file(s)" in capsys.readouterr().out


def test_finding_path_and_text_are_rendered_for_minimal_scanner_records() -> None:
    finding = {"check_id": "CKV_TEST_1", "resource": "resource", "file_path": "/nested/main.bicep"}

    assert _finding_line(finding) == (
        "  - [CKV_TEST_1] Checkov policy violation: resource at /nested/main.bicep."
    )
    assert _finding_path(finding, scan_path=CONTRACT_ROOT / "compliant" / "infra", scan_dir="infra") == (
        "infra/main.bicep"
    )


def test_checkov_report_paths_are_mapped_from_the_real_scan_root() -> None:
    scan_path = (CONTRACT_ROOT / "violation" / "infra").resolve()
    result = run_checkov(scan_path)
    assert result is not None
    _, report = result
    finding = report["results"]["failed_checks"][0]
    assert _finding_path(finding, scan_path=scan_path, scan_dir="infra") == "infra/main.bicep"
    outside_scan_root = {**finding, "file_abs_path": "/outside/tree/main.bicep"}
    assert _finding_path(outside_scan_root, scan_path=scan_path, scan_dir="infra") == "infra/main.bicep"
