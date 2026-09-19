"""Every owned static contract must execute both outcomes through the public gate."""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from tc_fitness.check_contract_execution import validate_contract_ledger
from tc_fitness.check_contracts import load_check_contract

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "tests/check_contracts"
OWNED = (
    "actionable_feedback",
    "behavioural_evidence",
    "cognitive_complexity",
    "empty_body_intent",
    "license_present",
    "no_commented_out_code",
    "no_duplicate_string",
    "no_env_monkeypatch",
    "no_hardcoded_repo_paths",
    "no_internal_monkeypatch",
    "no_internal_patches",
    "no_internal_patches_ts",
    "no_language_suffix_in_package_names",
    "no_llm_attribution",
    "no_logging_secrets",
    "no_noop_test_scripts",
    "no_production_suppressions",
    "no_real_names",
    "no_test_doubles_in_runtime_tiers",
    "no_test_imports_in_prod",
    "no_test_only_kwargs",
    "path_naming",
    "pattern_chokepoint",
    "posix_path_serialisation",
    "shellcheck_disable_with_reason",
    "suppressions_have_rationale",
    "test_skip_rationale",
    "unused_params_named",
)


def test_static_batch_contracts_are_complete_and_bound_to_the_owned_checks() -> None:
    missing = [name for name in OWNED if not (CONTRACTS / name / "contract.yaml").is_file()]
    assert not missing, f"missing public contracts: {missing}"
    for name in OWNED:
        contract = load_check_contract(CONTRACTS / name / "contract.yaml")
        assert contract.check == "core:" + name
        assert contract.dependencies == ()
        assert {case.id for case in contract.cases} == {"compliant", "violation"}
        for case in contract.cases:
            fixture = CONTRACTS / name / case.fixture
            assert any(path.is_file() for path in fixture.rglob("*")), fixture
            assert case.expected.status == ("pass" if case.id == "compliant" else "fail")


@pytest.mark.parametrize("name", OWNED)
@pytest.mark.parametrize("case", ["compliant", "violation"])
def test_static_contract_preserves_its_declared_public_outcome(tmp_path: Path, name: str, case: str) -> None:
    manifest = CONTRACTS / name / "contract.yaml"
    assert manifest.is_file(), f"missing public contract: {name}"
    destination = Path(os.environ.get("TC_STATIC_CONTRACT_EVIDENCE", str(tmp_path)))
    destination = destination / f"{name}-{case}-{uuid4()}"
    destination.mkdir(parents=True)
    ledger = destination / "ledger.json"
    started = datetime.now(UTC)
    result = subprocess.run(
        [
            str(Path(sys.executable).with_name("tc-fitness")),
            "run",
            "--contract",
            str(manifest),
            "--case",
            case,
            "--ledger",
            str(ledger),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    (destination / "stdout.log").write_text(result.stdout)
    (destination / "stderr.log").write_text(result.stderr)
    evidence = validate_contract_ledger(
        manifest, case, ledger, process_exit=result.returncode, started_after=started
    )
    assert evidence["actual"]["status"] == ("pass" if case == "compliant" else "fail")
    assert result.returncode == (0 if case == "compliant" else 1)
