"""Repository, Git, config and report contracts through the public command."""

from pathlib import Path

import pytest

from tc_fitness.check_contracts import load_check_contract
from tc_fitness.runner import run_contract_case

pytestmark = pytest.mark.integration

CONTRACTS = Path(__file__).parent / "check_contracts"
CHECKS = (
    "adr_number_unique",
    "canonical_commit_identity",
    "ci_consumes_shared_gate",
    "ci_fanin_parity",
    "ci_silencers_have_rationale",
    "contract_change_has_test",
    "coverage_floor",
    "coverage_includes_branches",
    "engine_version_floor",
    "every_test_has_tier_marker",
    "harness_canon_reference",
    "integrity_state_predicate",
    "mutation_survival_ratchet",
    "new_code_coverage",
    "readme_resolver_coverage",
    "schema_conformance",
    "sonar_ignore_rationale",
    "untrusted_automation_boundary",
)
GIT_CHECKS = {"canonical_commit_identity", "contract_change_has_test", "new_code_coverage"}


@pytest.mark.parametrize("check", CHECKS)
def test_repository_batch_contract_is_complete(check: str) -> None:
    manifest = CONTRACTS / check / "contract.yaml"
    assert manifest.is_file(), f"missing owned contract: {check}"
    contract = load_check_contract(manifest)
    assert contract.check == f"core:{check}"
    assert contract.dependencies == (("git",) if check in GIT_CHECKS else ())
    required = {"compliant", "violation"} | ({"unavailable"} if check in GIT_CHECKS else set())
    assert {case.id for case in contract.cases} == required
    for case in contract.cases:
        assert (manifest.parent / case.fixture).is_dir()
        assert case.environment.path == ("empty" if case.id == "unavailable" else "inherit")


@pytest.mark.parametrize(
    ("check", "case"),
    [(check, case) for check in CHECKS for case in ("compliant", "violation")]
    + [(check, "unavailable") for check in sorted(GIT_CHECKS)],
)
def test_repository_batch_public_run(check: str, case: str, tmp_path: Path) -> None:
    # This public wrapper launches tc-fitness run --contract/--case/--ledger
    # and validates the ledger against the real exit, invocation time, source
    # and fixture identities, and one-to-one structured finding expectations.
    evidence = run_contract_case(CONTRACTS / check / "contract.yaml", case, tmp_path / "ledger.json")
    assert evidence["check"] == f"core:{check}"
    assert evidence["case_id"] == case
    assert (
        evidence["actual"]["status"]
        == {"compliant": "pass", "violation": "fail", "unavailable": "error"}[case]
    )
