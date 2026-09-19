"""Public contract execution for the external/process/runtime Task 3 batch."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from tc_fitness.runner import run_contract_case

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_ROOT = REPO_ROOT / "tests" / "check_contracts"
EXTERNAL_CONTRACTS = {
    "bicep_arm_lint": ("compliant", "violation"),
    "checkov_iac_security": ("compliant", "violation", "unavailable"),
    "deterministic_tests": ("compliant", "violation", "unavailable"),
    "osv_scanner_sca": ("compliant", "violation", "unavailable"),
    "runtime_evidence_contract": ("compliant", "violation"),
    "runtime_filesystem_contract": ("compliant", "violation"),
    "script_help_smoke": ("compliant", "violation", "unavailable"),
}

pytestmark = pytest.mark.integration


def _install_protocol_tool_doubles(tools: Path) -> None:
    """Install deterministic scanner protocols; these are not live scanner proof."""
    tools.mkdir()
    (tools / "checkov").write_text(
        "#!/bin/sh\n"
        'if [ -f "$2/violation.marker" ]; then\n'
        '  printf \'%s\\n\' \'{"results":{"failed_checks":[{"check_id":"CKV_FIXTURE_1","file_path":"infra/main.bicep","resource":"fixture","check_name":"fixture violation","file_line_range":[1,1]}]},"summary":{"parsing_errors":0}}\'\n'
        "else\n"
        '  printf \'%s\\n\' \'{"results":{"failed_checks":[]},"summary":{"parsing_errors":0}}\'\n'
        "fi\n",
        encoding="utf-8",
    )
    (tools / "osv-scanner").write_text(
        "#!/bin/sh\n"
        'if [ "$1" = "--version" ]; then printf "%s\\n" "osv-scanner version: 2.2.4"; exit 0; fi\n'
        'if [ -f "violation.marker" ]; then\n'
        '  printf \'%s\\n\' \'{"results":[{"packages":[{"vulnerabilities":[{"id":"GHSA-fixture"}]}]}]}\'\n'
        "  exit 1\n"
        "fi\n"
        "printf '%s\\n' '{\"results\":[]}'\n",
        encoding="utf-8",
    )
    for executable in tools.iterdir():
        executable.chmod(0o755)


def test_external_contract_batch_is_complete_and_runs_through_the_public_cli(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Each owned fixture executes and validates via the installed public command."""
    found = {
        path.parent.name
        for path in CONTRACTS_ROOT.glob("*/contract.yaml")
        if path.parent.name in EXTERNAL_CONTRACTS
    }
    assert found == set(EXTERNAL_CONTRACTS)

    tools = tmp_path / "protocol-tools"
    _install_protocol_tool_doubles(tools)
    monkeypatch.setenv("PATH", f"{tools}:{os.environ['PATH']}")

    for name, case_ids in EXTERNAL_CONTRACTS.items():
        manifest = CONTRACTS_ROOT / name / "contract.yaml"
        for case_id in case_ids:
            ledger = tmp_path / f"{name}-{case_id}.json"
            result = run_contract_case(manifest, case_id, ledger)
            assert ledger.is_file()
            assert result["check"] == f"core:{name}"
            assert result["case_id"] == case_id
            assert result["actual"]["status"] == result["expected"]["status"]
