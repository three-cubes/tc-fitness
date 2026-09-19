"""Public contract execution for the external/process/runtime Task 3 batch."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness.check_contracts import load_check_contract
from tc_fitness.runner import run_contract_case

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_ROOT = REPO_ROOT / "tests" / "check_contracts"
EXTERNAL_CONTRACTS = {
    "bicep_arm_lint": ("compliant", "violation"),
    "deterministic_tests": ("compliant", "violation", "unavailable"),
    "osv_scanner_sca": ("compliant", "violation", "unavailable"),
    "runtime_evidence_contract": ("compliant", "violation"),
    "runtime_filesystem_contract": ("compliant", "violation"),
    "script_help_smoke": ("compliant", "violation", "unavailable"),
}

pytestmark = pytest.mark.contract


def _install_protocol_tool_doubles(tools: Path) -> None:
    """Install protocol-unit scanner collaborators; they never establish live proof."""
    tools.mkdir()
    (tools / "osv-scanner").write_text(
        "#!/bin/sh\n"
        'if [ "$1" = "--version" ]; then printf "%s\\n" "osv-scanner version: 2.2.4"; exit 0; fi\n'
        'if grep -q "fixture-vulnerable" uv.lock; then\n'
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


@pytest.mark.parametrize("name", ["osv_scanner_sca"])
def test_scanner_protocol_contracts_are_explicitly_non_admissible(
    name: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Controlled scanner protocols cannot be mistaken for live qualification."""
    contract_root = CONTRACTS_ROOT / name
    contract = load_check_contract(contract_root / "contract.yaml")

    assert contract.evidence_class == "protocol-unit"
    assert contract.live_qualification == "required-unmet"
    assert not contract.release_admission
    assert not list((contract_root / "violation").glob("*.marker"))
    tools = tmp_path / "protocol-tools"
    _install_protocol_tool_doubles(tools)
    monkeypatch.setenv("PATH", f"{tools}:{os.environ['PATH']}")
    ledger = run_contract_case(contract_root / "contract.yaml", "violation", tmp_path / "ledger.json")
    assert ledger["evidence_class"] == "protocol-unit"
    assert ledger["live_qualification"] == "required-unmet"
    assert not ledger["release_admission"]


def test_checkov_contract_runs_the_pinned_scanner_against_real_iac_fixtures(tmp_path: Path) -> None:
    """The Checkov contract calls the installed scanner, not a protocol double."""
    contract_path = CONTRACTS_ROOT / "checkov_iac_security" / "contract.yaml"
    contract = load_check_contract(contract_path)

    assert contract.evidence_class == "integration"
    assert contract.live_qualification == "required-unmet"
    assert not contract.release_admission
    for case_id in ("compliant", "violation", "unavailable"):
        ledger = run_contract_case(contract_path, case_id, tmp_path / f"checkov-{case_id}.json")
        assert ledger["check"] == "core:checkov_iac_security"
        assert ledger["case_id"] == case_id
        assert ledger["actual"]["status"] == ledger["expected"]["status"]


def test_contract_fixture_registry_is_not_collected_as_an_outer_test_suite() -> None:
    """Only registry drivers are tests; files below a contract manifest are fixture data."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "--strict-markers", "-q", "tests"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "tests/check_contracts/deterministic_tests/compliant/tests/test_stable.py" not in result.stdout
    assert (
        "tests/test_check_contracts_external_batch.py::test_external_contract_batch_is_complete"
        in result.stdout
    )
