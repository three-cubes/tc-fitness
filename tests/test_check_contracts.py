"""Behavioural contracts for CORE check-contract manifest validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness.check_contracts import (
    CheckContractError,
    load_check_contract,
    validate_contract_registry,
)

pytestmark = pytest.mark.integration


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


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
