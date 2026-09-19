"""Load and reconcile behavioural contracts for shipped CORE checks."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tc_fitness.lib import load_yaml

SCHEMA = "tc.fitness/check-contract/v1"
_STATUSES = frozenset({"pass", "fail", "error"})
_EXITS = frozenset({"zero", "nonzero"})


class CheckContractError(ValueError):
    """A check-contract manifest or registry is incomplete or inconsistent."""


@dataclass(frozen=True)
class FindingExpectation:
    """One stable finding the case must produce."""

    rule: str
    path: str
    message_contains: str


@dataclass(frozen=True)
class OutcomeExpectation:
    """The terminal outcome required from one contract case."""

    status: str
    exit: str
    findings: tuple[FindingExpectation, ...]


@dataclass(frozen=True)
class ContractCase:
    """A fixture and its expected terminal outcome."""

    id: str
    fixture: str
    expected: OutcomeExpectation


@dataclass(frozen=True)
class CheckContract:
    """Validated ``tc.fitness/check-contract/v1`` manifest."""

    check: str
    config: Mapping[str, Any]
    cases: tuple[ContractCase, ...]
    dependencies: tuple[str, ...]


def _mapping(value: object, location: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CheckContractError(f"{location} must be a mapping")
    return {str(key): item for key, item in value.items()}


def _list(value: object, location: str) -> list[object]:
    if not isinstance(value, list):
        raise CheckContractError(f"{location} must be a list")
    return value


def _required_string(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CheckContractError(f"{location} must be a non-empty string")
    return value


def _parse_finding(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def _parse_expected(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def _parse_case(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    return ContractCase(
        id=_required_string(raw.get("id"), f"{location}.id"),
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
    )


def _validate_case_set(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"compliant", "violation"} - cases_by_id.keys())
    if missing:
        raise CheckContractError(f"missing required cases: {', '.join(missing)}")
    compliant = cases_by_id["compliant"]
    if (
        compliant.expected.status != "pass"
        or compliant.expected.exit != "zero"
        or compliant.expected.findings
    ):
        raise CheckContractError("compliant case must expect status: pass and exit: zero with no findings")
    violation = cases_by_id["violation"]
    if (
        violation.expected.status != "fail"
        or violation.expected.exit != "nonzero"
        or not violation.expected.findings
    ):
        raise CheckContractError(
            "violation case must expect status: fail, exit: nonzero, and at least one finding"
        )
    unavailable = cases_by_id.get("unavailable")
    if not dependencies:
        if unavailable is not None:
            raise CheckContractError("unavailable case requires at least one dependency")
        return
    if (
        unavailable is None
        or unavailable.expected.status != "error"
        or unavailable.expected.exit != "nonzero"
    ):
        raise CheckContractError(
            "dependency-backed contracts require an unavailable case with status: error and exit: nonzero"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def load_check_contract(path: Path) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    return CheckContract(check=check, config=config, cases=cases, dependencies=dependencies)


def validate_contract_registry(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("core:") for check in core_checks]
    duplicate_names = sorted({name for name in expected_names if expected_names.count(name) > 1})
    if duplicate_names:
        raise CheckContractError(f"duplicate CORE_CHECKS ids: {', '.join(duplicate_names)}")
    if not contracts_root.is_dir():
        raise CheckContractError(f"contract registry directory does not exist: {contracts_root}")
    expected = set(expected_names)
    actual = {path.name for path in contracts_root.iterdir() if path.is_dir()}
    problems: list[str] = []
    missing = sorted(expected - actual)
    orphan = sorted(actual - expected)
    if missing:
        problems.append(f"missing contract directories: {', '.join(missing)}")
    if orphan:
        problems.append(f"orphan contract directories: {', '.join(orphan)}")
    if problems:
        raise CheckContractError("; ".join(problems))

    contracts: list[CheckContract] = []
    for name in sorted(expected):
        manifest = contracts_root / name / "contract.yaml"
        contract = load_check_contract(manifest)
        required_id = f"core:{name}"
        if contract.check != required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


__all__ = [
    "CheckContract",
    "CheckContractError",
    "ContractCase",
    "FindingExpectation",
    "OutcomeExpectation",
    "load_check_contract",
    "validate_contract_registry",
]
