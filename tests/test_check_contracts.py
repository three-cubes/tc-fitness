"""Behavioural contracts for CORE check-contract manifest validation."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from tc_fitness.check_contracts import (
    CheckContractError,
    load_check_contract,
    registered_contract_directory,
    validate_contract_registry,
)
from tc_fitness.core_checks import CORE_CHECKS
from tc_fitness.runner import run_contract_case

pytestmark = pytest.mark.integration

ROOT = Path(__file__).resolve().parents[1]
SHIPPED_CONTRACTS = ROOT / "tests" / "check_contracts"


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _valid_contract(check: str = "core:example_check") -> dict[str, object]:
    return {
        "schema": "tc.fitness/check-contract/v1",
        "check": check,
        "config": {},
        "cases": [
            {
                "id": "compliant",
                "fixture": "compliant",
                "expected": {"status": "pass", "exit": "zero", "findings": []},
            },
            {
                "id": "violation",
                "fixture": "violation",
                "expected": {
                    "status": "fail",
                    "exit": "nonzero",
                    "findings": [{"rule": "example", "path": "src/broken.py", "message_contains": "missing"}],
                },
            },
        ],
        "dependencies": [],
    }


def test_shipped_core_registry_has_exact_behavioural_contract_coverage() -> None:
    contracts = validate_contract_registry(CORE_CHECKS, SHIPPED_CONTRACTS)

    assert len(contracts) == len(CORE_CHECKS) == 53
    assert {contract.check for contract in contracts} == set(CORE_CHECKS)


def test_shipped_registry_rejects_a_sabotaged_manifest_binding(tmp_path: Path) -> None:
    for manifest in SHIPPED_CONTRACTS.glob("*/contract.yaml"):
        destination = tmp_path / manifest.parent.name / "contract.yaml"
        destination.parent.mkdir()
        destination.write_bytes(manifest.read_bytes())
    target = tmp_path / "license_present" / "contract.yaml"
    target.write_text(
        target.read_text().replace("check: core:license_present", "check: core:path_naming"),
        encoding="utf-8",
    )

    with pytest.raises(CheckContractError, match=r"license_present/contract\.yaml"):
        validate_contract_registry(CORE_CHECKS, tmp_path)


def test_public_contract_runner_rejects_a_sabotaged_expected_result(tmp_path: Path) -> None:
    source = SHIPPED_CONTRACTS / "license_present"
    sabotaged = tmp_path / "license_present"
    shutil.copytree(source, sabotaged)
    manifest = sabotaged / "contract.yaml"
    value = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    value["cases"][1]["expected"]["findings"][0]["message_contains"] = "impossible result"
    manifest.write_text(yaml.safe_dump(value), encoding="utf-8")

    with pytest.raises(CheckContractError, match="ledger findings do not match"):
        run_contract_case(manifest, "violation", tmp_path / "ledger.json")


def test_repository_collection_executes_contract_drivers_without_collecting_fixture_tests() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "--strict-markers",
            "-p",
            "tc_fitness.pytest_tiers",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "tests/test_check_contracts_static_batch.py::" in result.stdout
    assert "tests/test_check_contracts_repository.py::" in result.stdout
    assert "tests/check_contracts/" not in result.stdout


def test_invalid_contract_manifest_cannot_hide_an_unclassified_test(
    tmp_path: Path,
) -> None:
    contract = tmp_path / "tests" / "check_contracts" / "example"
    _write(
        contract / "contract.yaml",
        """schema: tc.fitness/check-contract/v1
check: core:example
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example
          path: test_hidden.py
          message_contains: intended violation
dependencies: []
""",
    )
    (contract / "compliant").mkdir()
    _write(contract / "violation" / "test_hidden.py", "def test_hidden(): pass\n")
    _write(
        tmp_path / "tests" / "test_control.py",
        "import pytest\npytestmark = pytest.mark.integration\ndef test_control(): pass\n",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "--strict-markers",
            "-o",
            "markers=integration: repository composition test",
            "-p",
            "tc_fitness.pytest_tiers",
            str(tmp_path / "tests"),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )

    assert result.returncode == 4, result.stdout + result.stderr
    assert "test_hidden.py::test_hidden" in result.stdout
    assert "items must have exactly one effective tier" in result.stderr


def test_loads_complete_contract_with_explicit_exit_expectations(tmp_path: Path) -> None:
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:example_check
config:
  roots: [src]
cases:
  - id: compliant
    fixture: compliant
    expected:
      status: pass
      exit: zero
      findings: []
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: []
""",
    )

    contract = load_check_contract(manifest)

    assert contract.check == "core:example_check"
    assert [case.id for case in contract.cases] == ["compliant", "violation"]
    assert contract.cases[1].expected.exit == "nonzero"
    assert contract.cases[1].expected.findings[0].path == "src/broken.py"


@pytest.mark.parametrize(
    ("metadata", "message"),
    [
        ({"evidence_class": "unreviewed"}, "evidence_class must be one of"),
        ({"live_qualification": "unreviewed"}, "live_qualification must be one of"),
        ({"release_admission": "yes"}, "release_admission must be a boolean"),
        ({"evidence_class": "protocol-unit"}, "requires an explicitly unmet live qualification"),
    ],
)
def test_evidence_metadata_rejects_unqualified_manifest_claims(
    tmp_path: Path, metadata: dict[str, object], message: str
) -> None:
    contract = _valid_contract()
    contract.update(metadata)
    manifest = _write(tmp_path / "contract.yaml", yaml.safe_dump(contract, sort_keys=False))

    with pytest.raises(CheckContractError, match=message):
        load_check_contract(manifest)


def test_git_case_environment_rejects_an_unknown_nested_schema(tmp_path: Path) -> None:
    contract = _valid_contract()
    cases = contract["cases"]
    assert isinstance(cases, list)
    cases[0]["environment"] = {
        "schema": "tc.fitness/check-environment/v2",
        "path": "inherit",
        "git": {
            "schema": "tc.fitness/git-fixture/v0",
            "history": ".contract/history.fi",
            "checkout": "refs/heads/main",
        },
    }
    manifest = _write(tmp_path / "contract.yaml", yaml.safe_dump(contract, sort_keys=False))

    with pytest.raises(CheckContractError, match="v1 schema"):
        load_check_contract(manifest)


def test_registered_contract_directory_requires_its_name_registration_and_fixtures(tmp_path: Path) -> None:
    registry = tmp_path / "example_check"
    registry.mkdir()
    for case in ("compliant", "violation"):
        (registry / case).mkdir()
    manifest = _write(registry / "contract.yaml", yaml.safe_dump(_valid_contract(), sort_keys=False))

    assert registered_contract_directory(registry, ("core:example_check",)) is not None
    assert registered_contract_directory(registry, ()) is None

    copied = tmp_path / "copied"
    copied.mkdir()
    for case in ("compliant", "violation"):
        (copied / case).mkdir()
    _write(copied / "contract.yaml", manifest.read_text())
    assert registered_contract_directory(copied, ("core:example_check",)) is None


@pytest.mark.parametrize("fixture", ["/absolute-fixture", "../escape", "missing", "linked"])
def test_registered_contract_directory_rejects_nonportable_or_unbound_fixtures(
    tmp_path: Path, fixture: str
) -> None:
    registry = tmp_path / "example_check"
    registry.mkdir()
    (registry / "compliant").mkdir()
    if fixture == "linked":
        target = tmp_path / "outside"
        target.mkdir()
        (registry / fixture).symlink_to(target, target_is_directory=True)
    contract = _valid_contract()
    cases = contract["cases"]
    assert isinstance(cases, list)
    cases[1]["fixture"] = fixture
    _write(registry / "contract.yaml", yaml.safe_dump(contract, sort_keys=False))

    assert registered_contract_directory(registry, ("core:example_check",)) is None


def test_manifest_cannot_grant_its_own_release_admission(tmp_path: Path) -> None:
    """Only protected release receipts, never fixture-authored metadata, grant admission."""
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:example_check
evidence_class: live
live_qualification: qualified
release_admission: true
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: []
""",
    )

    with pytest.raises(CheckContractError, match="cannot grant release admission"):
        load_check_contract(manifest)


def test_rejects_case_without_exit_expectation(tmp_path: Path) -> None:
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:example_check
config: {}
cases:
  - id: violation
    fixture: violation
    expected:
      status: fail
      findings: []
dependencies: []
""",
    )

    with pytest.raises(CheckContractError, match=r"cases\[0\]\.expected\.exit"):
        load_check_contract(manifest)


def test_dependency_contract_requires_unavailable_error_case(tmp_path: Path) -> None:
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:example_check
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: [example-tool]
""",
    )

    with pytest.raises(CheckContractError, match=r"unavailable.*status: error.*exit: nonzero"):
        load_check_contract(manifest)


def test_loads_dependency_backed_contract_with_an_unavailable_error_case(tmp_path: Path) -> None:
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:example_check
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
  - id: unavailable
    fixture: unavailable
    expected:
      status: error
      exit: nonzero
      findings:
        - rule: example-tool
          path: pyproject.toml
          message_contains: example-tool is unavailable
dependencies: [example-tool]
""",
    )

    contract = load_check_contract(manifest)

    assert contract.dependencies == ("example-tool",)
    assert contract.cases[-1].expected.status == "error"


def test_dependency_contract_requires_an_unavailable_stable_finding(tmp_path: Path) -> None:
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:example_check
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
  - id: unavailable
    fixture: unavailable
    expected: {status: error, exit: nonzero, findings: []}
dependencies: [example-tool]
""",
    )

    with pytest.raises(CheckContractError, match="unavailable case must expect at least one stable finding"):
        load_check_contract(manifest)


@pytest.mark.parametrize(
    ("case_id", "status", "exit_class", "findings", "message"),
    [
        ("compliant", "fail", "nonzero", "[]", "compliant case must expect status: pass and exit: zero"),
        (
            "violation",
            "pass",
            "zero",
            "[]",
            "violation case must expect status: fail, exit: nonzero, and at least one finding",
        ),
    ],
)
def test_rejects_required_cases_without_their_declared_control_outcome(
    tmp_path: Path,
    case_id: str,
    status: str,
    exit_class: str,
    findings: str,
    message: str,
) -> None:
    expectations = {
        "compliant": "{status: pass, exit: zero, findings: []}",
        "violation": (
            "{status: fail, exit: nonzero, findings: "
            "[{rule: example-check, path: src/broken.py, message_contains: required behaviour is missing}]}"
        ),
    }
    expectations[case_id] = f"{{status: {status}, exit: {exit_class}, findings: {findings}}}"
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:example_check
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: __COMPLIANT__
  - id: violation
    fixture: violation
    expected: __VIOLATION__
dependencies: []
""".replace("__COMPLIANT__", expectations["compliant"]).replace("__VIOLATION__", expectations["violation"]),
    )

    with pytest.raises(CheckContractError, match=message):
        load_check_contract(manifest)


def test_rejects_unavailable_case_without_a_declared_dependency(tmp_path: Path) -> None:
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:example_check
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
  - id: unavailable
    fixture: unavailable
    expected: {status: error, exit: nonzero, findings: []}
dependencies: []
""",
    )

    with pytest.raises(CheckContractError, match="unavailable case requires at least one dependency"):
        load_check_contract(manifest)


def test_registry_rejects_manifest_bound_to_another_check(tmp_path: Path) -> None:
    _write(
        tmp_path / "alpha" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:beta
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: beta
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: []
""",
    )

    with pytest.raises(CheckContractError, match=r"alpha/contract.yaml.*core:alpha.*core:beta"):
        validate_contract_registry(("core:alpha",), tmp_path)


def test_registry_reports_missing_and_orphan_contracts_together(tmp_path: Path) -> None:
    _write(
        tmp_path / "orphan" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:orphan
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: orphan
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: []
""",
    )

    with pytest.raises(CheckContractError) as captured:
        validate_contract_registry(("core:missing",), tmp_path)

    assert "missing contract directories: missing" in str(captured.value)
    assert "orphan contract directories: orphan" in str(captured.value)


def test_registry_rejects_a_directory_without_a_contract_manifest(tmp_path: Path) -> None:
    _write(
        tmp_path / "alpha" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:alpha
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: alpha
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: []
""",
    )
    (tmp_path / "orphan").mkdir()

    with pytest.raises(CheckContractError, match="orphan contract directories: orphan"):
        validate_contract_registry(("core:alpha",), tmp_path)


@pytest.mark.parametrize(
    ("expected", "match"),
    [
        ("{status: unknown, exit: zero, findings: []}", r"expected\.status must be one of"),
        ("{status: pass, exit: unknown, findings: []}", r"expected\.exit must be one of"),
    ],
)
def test_rejects_an_unknown_status_or_exit_classification(tmp_path: Path, expected: str, match: str) -> None:
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:example_check
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: __EXPECTED__
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: []
""".replace("__EXPECTED__", expected),
    )

    with pytest.raises(CheckContractError, match=match):
        load_check_contract(manifest)


@pytest.mark.parametrize(
    ("cases", "match"),
    [
        (
            """
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
""",
            "missing required cases: violation",
        ),
        (
            """
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: compliant
    fixture: another-compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
""",
            "duplicate case ids: compliant",
        ),
    ],
)
def test_rejects_missing_or_duplicate_required_cases(tmp_path: Path, cases: str, match: str) -> None:
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        f"""
schema: tc.fitness/check-contract/v1
check: core:example_check
config: {{}}
cases:
{cases}dependencies: []
""",
    )

    with pytest.raises(CheckContractError, match=match):
        load_check_contract(manifest)


def test_registry_loads_an_exact_valid_contract_set(tmp_path: Path) -> None:
    for name in ("alpha", "beta"):
        _write(
            tmp_path / name / "contract.yaml",
            f"""
schema: tc.fitness/check-contract/v1
check: core:{name}
config: {{}}
cases:
  - id: compliant
    fixture: compliant
    expected: {{status: pass, exit: zero, findings: []}}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: {name}
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: []
""",
        )

    contracts = validate_contract_registry(("core:alpha", "core:beta"), tmp_path)

    assert [contract.check for contract in contracts] == ["core:alpha", "core:beta"]


@pytest.mark.parametrize(
    ("field", "replacement", "match"),
    [
        ("schema", "schema: another-schema", "schema must be"),
        ("check", "check: 'core:'", "check must use the core:<module> namespace"),
        ("config", "config: []", "config must be a mapping"),
        ("cases", "cases: {}", "cases must be a list"),
        ("dependencies", "dependencies: {}", "dependencies must be a list"),
    ],
)
def test_rejects_malformed_manifest_structure(
    tmp_path: Path, field: str, replacement: str, match: str
) -> None:
    fields = {
        "schema": "schema: tc.fitness/check-contract/v1",
        "check": "check: core:example_check",
        "config": "config: {}",
        "cases": """cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing""",
        "dependencies": "dependencies: []",
    }
    fields[field] = replacement
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
__SCHEMA__
__CHECK__
__CONFIG__
__CASES__
__DEPENDENCIES__
""".replace("__SCHEMA__", fields["schema"])
        .replace("__CHECK__", fields["check"])
        .replace("__CONFIG__", fields["config"])
        .replace("__CASES__", fields["cases"])
        .replace("__DEPENDENCIES__", fields["dependencies"]),
    )

    with pytest.raises(CheckContractError, match=match):
        load_check_contract(manifest)


def test_rejects_a_missing_or_invalid_yaml_contract_manifest(tmp_path: Path) -> None:
    missing = tmp_path / "missing" / "contract.yaml"

    with pytest.raises(CheckContractError, match="contract manifest does not exist"):
        load_check_contract(missing)

    invalid = _write(tmp_path / "invalid" / "contract.yaml", "cases: [\n")

    with pytest.raises(CheckContractError, match="invalid YAML"):
        load_check_contract(invalid)


def test_rejects_duplicate_yaml_mapping_keys(tmp_path: Path) -> None:
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
schema: tc.fitness/check-contract/v1
check: core:another_check
check: core:example_check
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: []
""",
    )

    with pytest.raises(CheckContractError, match="duplicate YAML mapping key: 'check'"):
        load_check_contract(manifest)


def test_rejects_an_unhashable_yaml_mapping_key_as_a_contract_error(tmp_path: Path) -> None:
    manifest = _write(
        tmp_path / "example_check" / "contract.yaml",
        """
? [a]
: ignored
schema: tc.fitness/check-contract/v1
check: core:example_check
config: {}
cases:
  - id: compliant
    fixture: compliant
    expected: {status: pass, exit: zero, findings: []}
  - id: violation
    fixture: violation
    expected:
      status: fail
      exit: nonzero
      findings:
        - rule: example-check
          path: src/broken.py
          message_contains: required behaviour is missing
dependencies: []
""",
    )

    with pytest.raises(CheckContractError, match=r"(?s)invalid YAML.*unhashable YAML mapping key"):
        load_check_contract(manifest)


@pytest.mark.parametrize(
    ("core_checks", "contracts_root", "match"),
    [
        (("core:",), "root", "CORE_CHECKS ids must use core:<module>"),
        (("core:alpha", "core:alpha"), "root", "duplicate CORE_CHECKS ids: alpha"),
        (("core:alpha",), "missing", "contract registry directory does not exist"),
    ],
)
def test_registry_rejects_invalid_registry_inputs(
    tmp_path: Path, core_checks: tuple[str, ...], contracts_root: str, match: str
) -> None:
    root = tmp_path / contracts_root
    if contracts_root == "root":
        root.mkdir()

    with pytest.raises(CheckContractError, match=match):
        validate_contract_registry(core_checks, root)
