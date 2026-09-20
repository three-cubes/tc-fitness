"""Load and reconcile behavioural contracts for shipped CORE checks."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tc_fitness.lib import load_yaml

SCHEMA = "tc.fitness/check-contract/v1"
_STATUSES = frozenset({"pass", "fail", "error"})
_EXITS = frozenset({"zero", "nonzero"})
_EVIDENCE_CLASSES = frozenset({"unclassified", "protocol-unit", "integration", "live"})
_LIVE_QUALIFICATIONS = frozenset({"not-required", "required-unmet", "qualified"})


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


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
class CaseEnvironment:
    """Portable process-search-path policy, never arbitrary environment values."""

    schema: str = "tc.fitness/check-environment/v1"
    path: str = "inherit"


@dataclass(frozen=True)
class GitFixtureEnvironment:
    """Deterministic Git history materialised before a contract case runs."""

    schema: str
    history: str
    checkout: str


@dataclass(frozen=True)
class GitCaseEnvironment:
    """Versioned case environment with a bound Git fast-import input."""

    schema: str
    path: str
    git: GitFixtureEnvironment


@dataclass(frozen=True)
class ContractCase:
    """A fixture and its expected terminal outcome."""

    id: str
    fixture: str
    expected: OutcomeExpectation
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()


@dataclass(frozen=True)
class CheckContract:
    """Validated ``tc.fitness/check-contract/v1`` manifest."""

    check: str
    config: Mapping[str, Any]
    cases: tuple[ContractCase, ...]
    dependencies: tuple[str, ...]
    evidence_class: str = "unclassified"
    live_qualification: str = "not-required"
    release_admission: bool = False
mutants_x__mapping__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__mapping__mutmut)
def _mapping(value: object, location: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CheckContractError(f"{location} must be a mapping")
    return {str(key): item for key, item in value.items()}


def x__mapping__mutmut_orig(value: object, location: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CheckContractError(f"{location} must be a mapping")
    return {str(key): item for key, item in value.items()}


def x__mapping__mutmut_1(value: object, location: str) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        raise CheckContractError(f"{location} must be a mapping")
    return {str(key): item for key, item in value.items()}


def x__mapping__mutmut_2(value: object, location: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CheckContractError(None)
    return {str(key): item for key, item in value.items()}


def x__mapping__mutmut_3(value: object, location: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CheckContractError(f"{location} must be a mapping")
    return {str(None): item for key, item in value.items()}

mutants_x__mapping__mutmut['_mutmut_orig'] = x__mapping__mutmut_orig # type: ignore # mutmut generated
mutants_x__mapping__mutmut['x__mapping__mutmut_1'] = x__mapping__mutmut_1 # type: ignore # mutmut generated
mutants_x__mapping__mutmut['x__mapping__mutmut_2'] = x__mapping__mutmut_2 # type: ignore # mutmut generated
mutants_x__mapping__mutmut['x__mapping__mutmut_3'] = x__mapping__mutmut_3 # type: ignore # mutmut generated
mutants_x__list__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__list__mutmut)
def _list(value: object, location: str) -> list[object]:
    if not isinstance(value, list):
        raise CheckContractError(f"{location} must be a list")
    return value


def x__list__mutmut_orig(value: object, location: str) -> list[object]:
    if not isinstance(value, list):
        raise CheckContractError(f"{location} must be a list")
    return value


def x__list__mutmut_1(value: object, location: str) -> list[object]:
    if isinstance(value, list):
        raise CheckContractError(f"{location} must be a list")
    return value


def x__list__mutmut_2(value: object, location: str) -> list[object]:
    if not isinstance(value, list):
        raise CheckContractError(None)
    return value

mutants_x__list__mutmut['_mutmut_orig'] = x__list__mutmut_orig # type: ignore # mutmut generated
mutants_x__list__mutmut['x__list__mutmut_1'] = x__list__mutmut_1 # type: ignore # mutmut generated
mutants_x__list__mutmut['x__list__mutmut_2'] = x__list__mutmut_2 # type: ignore # mutmut generated
mutants_x__required_string__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__required_string__mutmut)
def _required_string(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CheckContractError(f"{location} must be a non-empty string")
    return value


def x__required_string__mutmut_orig(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CheckContractError(f"{location} must be a non-empty string")
    return value


def x__required_string__mutmut_1(value: object, location: str) -> str:
    if not isinstance(value, str) and not value.strip():
        raise CheckContractError(f"{location} must be a non-empty string")
    return value


def x__required_string__mutmut_2(value: object, location: str) -> str:
    if isinstance(value, str) or not value.strip():
        raise CheckContractError(f"{location} must be a non-empty string")
    return value


def x__required_string__mutmut_3(value: object, location: str) -> str:
    if not isinstance(value, str) or value.strip():
        raise CheckContractError(f"{location} must be a non-empty string")
    return value


def x__required_string__mutmut_4(value: object, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CheckContractError(None)
    return value

mutants_x__required_string__mutmut['_mutmut_orig'] = x__required_string__mutmut_orig # type: ignore # mutmut generated
mutants_x__required_string__mutmut['x__required_string__mutmut_1'] = x__required_string__mutmut_1 # type: ignore # mutmut generated
mutants_x__required_string__mutmut['x__required_string__mutmut_2'] = x__required_string__mutmut_2 # type: ignore # mutmut generated
mutants_x__required_string__mutmut['x__required_string__mutmut_3'] = x__required_string__mutmut_3 # type: ignore # mutmut generated
mutants_x__required_string__mutmut['x__required_string__mutmut_4'] = x__required_string__mutmut_4 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__parse_finding__mutmut)
def _parse_finding(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_orig(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_1(value: object, location: str) -> FindingExpectation:
    raw = None
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_2(value: object, location: str) -> FindingExpectation:
    raw = _mapping(None, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_3(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, None)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_4(value: object, location: str) -> FindingExpectation:
    raw = _mapping(location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_5(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, )
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_6(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=None,
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_7(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=None,
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_8(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=None,
    )


def x__parse_finding__mutmut_9(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_10(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_11(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        )


def x__parse_finding__mutmut_12(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(None, f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_13(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), None),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_14(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_15(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), ),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_16(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get(None), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_17(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("XXruleXX"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_18(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("RULE"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_19(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(None, f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_20(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), None),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_21(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_22(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), ),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_23(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get(None), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_24(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("XXpathXX"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_25(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("PATH"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_26(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(None, f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_27(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), None),
    )


def x__parse_finding__mutmut_28(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_29(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("message_contains"), ),
    )


def x__parse_finding__mutmut_30(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get(None), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_31(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("XXmessage_containsXX"), f"{location}.message_contains"),
    )


def x__parse_finding__mutmut_32(value: object, location: str) -> FindingExpectation:
    raw = _mapping(value, location)
    return FindingExpectation(
        rule=_required_string(raw.get("rule"), f"{location}.rule"),
        path=_required_string(raw.get("path"), f"{location}.path"),
        message_contains=_required_string(raw.get("MESSAGE_CONTAINS"), f"{location}.message_contains"),
    )

mutants_x__parse_finding__mutmut['_mutmut_orig'] = x__parse_finding__mutmut_orig # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_1'] = x__parse_finding__mutmut_1 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_2'] = x__parse_finding__mutmut_2 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_3'] = x__parse_finding__mutmut_3 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_4'] = x__parse_finding__mutmut_4 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_5'] = x__parse_finding__mutmut_5 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_6'] = x__parse_finding__mutmut_6 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_7'] = x__parse_finding__mutmut_7 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_8'] = x__parse_finding__mutmut_8 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_9'] = x__parse_finding__mutmut_9 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_10'] = x__parse_finding__mutmut_10 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_11'] = x__parse_finding__mutmut_11 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_12'] = x__parse_finding__mutmut_12 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_13'] = x__parse_finding__mutmut_13 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_14'] = x__parse_finding__mutmut_14 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_15'] = x__parse_finding__mutmut_15 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_16'] = x__parse_finding__mutmut_16 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_17'] = x__parse_finding__mutmut_17 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_18'] = x__parse_finding__mutmut_18 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_19'] = x__parse_finding__mutmut_19 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_20'] = x__parse_finding__mutmut_20 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_21'] = x__parse_finding__mutmut_21 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_22'] = x__parse_finding__mutmut_22 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_23'] = x__parse_finding__mutmut_23 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_24'] = x__parse_finding__mutmut_24 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_25'] = x__parse_finding__mutmut_25 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_26'] = x__parse_finding__mutmut_26 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_27'] = x__parse_finding__mutmut_27 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_28'] = x__parse_finding__mutmut_28 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_29'] = x__parse_finding__mutmut_29 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_30'] = x__parse_finding__mutmut_30 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_31'] = x__parse_finding__mutmut_31 # type: ignore # mutmut generated
mutants_x__parse_finding__mutmut['x__parse_finding__mutmut_32'] = x__parse_finding__mutmut_32 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__parse_expected__mutmut)
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


def x__parse_expected__mutmut_orig(value: object, location: str) -> OutcomeExpectation:
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


def x__parse_expected__mutmut_1(value: object, location: str) -> OutcomeExpectation:
    raw = None
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


def x__parse_expected__mutmut_2(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(None, location)
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


def x__parse_expected__mutmut_3(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, None)
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


def x__parse_expected__mutmut_4(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(location)
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


def x__parse_expected__mutmut_5(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, )
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


def x__parse_expected__mutmut_6(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = None
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


def x__parse_expected__mutmut_7(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(None, f"{location}.status")
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


def x__parse_expected__mutmut_8(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), None)
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


def x__parse_expected__mutmut_9(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(f"{location}.status")
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


def x__parse_expected__mutmut_10(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), )
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


def x__parse_expected__mutmut_11(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get(None), f"{location}.status")
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


def x__parse_expected__mutmut_12(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("XXstatusXX"), f"{location}.status")
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


def x__parse_expected__mutmut_13(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("STATUS"), f"{location}.status")
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


def x__parse_expected__mutmut_14(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_15(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(None)
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_16(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(None)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_17(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = None
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_18(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(None, f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_19(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), None)
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_20(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_21(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), )
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_22(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get(None), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_23(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("XXexitXX"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_24(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("EXIT"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_25(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_26(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(None)
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_27(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(None)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_28(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = None
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_29(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        None
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_30(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(None, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_31(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, None)
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_32(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_33(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, )
        for index, item in enumerate(_list(raw.get("findings"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_34(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(None)
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_35(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(None, f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_36(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), None))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_37(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_38(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("findings"), ))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_39(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get(None), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_40(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("XXfindingsXX"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_41(value: object, location: str) -> OutcomeExpectation:
    raw = _mapping(value, location)
    status = _required_string(raw.get("status"), f"{location}.status")
    if status not in _STATUSES:
        raise CheckContractError(f"{location}.status must be one of {sorted(_STATUSES)}")
    exit_class = _required_string(raw.get("exit"), f"{location}.exit")
    if exit_class not in _EXITS:
        raise CheckContractError(f"{location}.exit must be one of {sorted(_EXITS)}")
    findings = tuple(
        _parse_finding(item, f"{location}.findings[{index}]")
        for index, item in enumerate(_list(raw.get("FINDINGS"), f"{location}.findings"))
    )
    return OutcomeExpectation(status=status, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_42(value: object, location: str) -> OutcomeExpectation:
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
    return OutcomeExpectation(status=None, exit=exit_class, findings=findings)


def x__parse_expected__mutmut_43(value: object, location: str) -> OutcomeExpectation:
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
    return OutcomeExpectation(status=status, exit=None, findings=findings)


def x__parse_expected__mutmut_44(value: object, location: str) -> OutcomeExpectation:
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
    return OutcomeExpectation(status=status, exit=exit_class, findings=None)


def x__parse_expected__mutmut_45(value: object, location: str) -> OutcomeExpectation:
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
    return OutcomeExpectation(exit=exit_class, findings=findings)


def x__parse_expected__mutmut_46(value: object, location: str) -> OutcomeExpectation:
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
    return OutcomeExpectation(status=status, findings=findings)


def x__parse_expected__mutmut_47(value: object, location: str) -> OutcomeExpectation:
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
    return OutcomeExpectation(status=status, exit=exit_class, )

mutants_x__parse_expected__mutmut['_mutmut_orig'] = x__parse_expected__mutmut_orig # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_1'] = x__parse_expected__mutmut_1 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_2'] = x__parse_expected__mutmut_2 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_3'] = x__parse_expected__mutmut_3 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_4'] = x__parse_expected__mutmut_4 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_5'] = x__parse_expected__mutmut_5 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_6'] = x__parse_expected__mutmut_6 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_7'] = x__parse_expected__mutmut_7 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_8'] = x__parse_expected__mutmut_8 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_9'] = x__parse_expected__mutmut_9 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_10'] = x__parse_expected__mutmut_10 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_11'] = x__parse_expected__mutmut_11 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_12'] = x__parse_expected__mutmut_12 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_13'] = x__parse_expected__mutmut_13 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_14'] = x__parse_expected__mutmut_14 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_15'] = x__parse_expected__mutmut_15 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_16'] = x__parse_expected__mutmut_16 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_17'] = x__parse_expected__mutmut_17 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_18'] = x__parse_expected__mutmut_18 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_19'] = x__parse_expected__mutmut_19 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_20'] = x__parse_expected__mutmut_20 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_21'] = x__parse_expected__mutmut_21 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_22'] = x__parse_expected__mutmut_22 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_23'] = x__parse_expected__mutmut_23 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_24'] = x__parse_expected__mutmut_24 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_25'] = x__parse_expected__mutmut_25 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_26'] = x__parse_expected__mutmut_26 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_27'] = x__parse_expected__mutmut_27 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_28'] = x__parse_expected__mutmut_28 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_29'] = x__parse_expected__mutmut_29 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_30'] = x__parse_expected__mutmut_30 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_31'] = x__parse_expected__mutmut_31 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_32'] = x__parse_expected__mutmut_32 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_33'] = x__parse_expected__mutmut_33 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_34'] = x__parse_expected__mutmut_34 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_35'] = x__parse_expected__mutmut_35 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_36'] = x__parse_expected__mutmut_36 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_37'] = x__parse_expected__mutmut_37 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_38'] = x__parse_expected__mutmut_38 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_39'] = x__parse_expected__mutmut_39 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_40'] = x__parse_expected__mutmut_40 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_41'] = x__parse_expected__mutmut_41 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_42'] = x__parse_expected__mutmut_42 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_43'] = x__parse_expected__mutmut_43 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_44'] = x__parse_expected__mutmut_44 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_45'] = x__parse_expected__mutmut_45 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_46'] = x__parse_expected__mutmut_46 # type: ignore # mutmut generated
mutants_x__parse_expected__mutmut['x__parse_expected__mutmut_47'] = x__parse_expected__mutmut_47 # type: ignore # mutmut generated


_GIT_CHECKOUT = re.compile(r"^refs/heads/[A-Za-z0-9](?:[A-Za-z0-9._/-]*[A-Za-z0-9])?$")
mutants_x__portable_git_history__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__portable_git_history__mutmut)
def _portable_git_history(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_orig(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_1(value: object, location: str) -> str:
    history = None
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_2(value: object, location: str) -> str:
    history = _required_string(None, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_3(value: object, location: str) -> str:
    history = _required_string(value, None)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_4(value: object, location: str) -> str:
    history = _required_string(location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_5(value: object, location: str) -> str:
    history = _required_string(value, )
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_6(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = None
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_7(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(None)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_8(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts and "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_9(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() and ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_10(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or "XX..XX" in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_11(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." not in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_12(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "XX\\XX" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_13(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" not in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_14(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(None)
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_15(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts and path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_16(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if path.parts or path.parts[0] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_17(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[1] != ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_18(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] == ".contract":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_19(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != "XX.contractXX":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_20(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".CONTRACT":
        raise CheckContractError(f"{location} must live beneath .contract")
    return path.as_posix()


def x__portable_git_history__mutmut_21(value: object, location: str) -> str:
    history = _required_string(value, location)
    path = Path(history)
    if path.is_absolute() or ".." in path.parts or "\\" in history:
        raise CheckContractError(f"{location} must be a portable path")
    if not path.parts or path.parts[0] != ".contract":
        raise CheckContractError(None)
    return path.as_posix()

mutants_x__portable_git_history__mutmut['_mutmut_orig'] = x__portable_git_history__mutmut_orig # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_1'] = x__portable_git_history__mutmut_1 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_2'] = x__portable_git_history__mutmut_2 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_3'] = x__portable_git_history__mutmut_3 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_4'] = x__portable_git_history__mutmut_4 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_5'] = x__portable_git_history__mutmut_5 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_6'] = x__portable_git_history__mutmut_6 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_7'] = x__portable_git_history__mutmut_7 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_8'] = x__portable_git_history__mutmut_8 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_9'] = x__portable_git_history__mutmut_9 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_10'] = x__portable_git_history__mutmut_10 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_11'] = x__portable_git_history__mutmut_11 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_12'] = x__portable_git_history__mutmut_12 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_13'] = x__portable_git_history__mutmut_13 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_14'] = x__portable_git_history__mutmut_14 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_15'] = x__portable_git_history__mutmut_15 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_16'] = x__portable_git_history__mutmut_16 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_17'] = x__portable_git_history__mutmut_17 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_18'] = x__portable_git_history__mutmut_18 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_19'] = x__portable_git_history__mutmut_19 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_20'] = x__portable_git_history__mutmut_20 # type: ignore # mutmut generated
mutants_x__portable_git_history__mutmut['x__portable_git_history__mutmut_21'] = x__portable_git_history__mutmut_21 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__parse_environment__mutmut)
def _parse_environment(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_orig(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_1(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = None
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_2(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(None, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_3(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, None)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_4(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_5(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, )
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_6(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = None
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_7(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get(None)
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_8(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("XXschemaXX")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_9(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("SCHEMA")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_10(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = None
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_11(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get(None)
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_12(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("XXpathXX")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_13(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("PATH")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_14(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) and path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_15(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_16(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_17(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"XXinheritXX", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_18(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"INHERIT", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_19(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "XXemptyXX"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_20(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "EMPTY"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_21(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(None)
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_22(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" or set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_23(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema != "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_24(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "XXtc.fitness/check-environment/v1XX" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_25(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "TC.FITNESS/CHECK-ENVIRONMENT/V1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_26(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(None) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_27(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) != {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_28(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"XXschemaXX", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_29(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"SCHEMA", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_30(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "XXpathXX"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_31(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "PATH"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_32(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=None)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_33(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" and set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_34(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema == "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_35(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "XXtc.fitness/check-environment/v2XX" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_36(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "TC.FITNESS/CHECK-ENVIRONMENT/V2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_37(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(None) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_38(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) == {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_39(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"XXschemaXX", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_40(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"SCHEMA", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_41(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "XXpathXX", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_42(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "PATH", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_43(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "XXgitXX"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_44(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "GIT"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_45(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(None)
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_46(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = None
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_47(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = None
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_48(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(None, git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_49(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], None)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_50(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_51(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], )
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_52(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["XXgitXX"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_53(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["GIT"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_54(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} and git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_55(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(None) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_56(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) == {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_57(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"XXschemaXX", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_58(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"SCHEMA", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_59(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "XXhistoryXX", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_60(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "HISTORY", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_61(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "XXcheckoutXX"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_62(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "CHECKOUT"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_63(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get(None) != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_64(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("XXschemaXX") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_65(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("SCHEMA") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_66(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") == "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_67(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "XXtc.fitness/git-fixture/v1XX":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_68(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "TC.FITNESS/GIT-FIXTURE/V1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_69(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(None)
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_70(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = None
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_71(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(None, f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_72(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), None)
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_73(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_74(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), )
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_75(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get(None), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_76(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("XXcheckoutXX"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_77(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("CHECKOUT"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_78(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) and any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_79(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_80(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(None) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_81(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        None
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_82(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden not in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_83(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("XX..XX", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_84(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "XX//XX", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_85(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "XX@{XX", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_86(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", "XX.lockXX")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_87(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".LOCK")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_88(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(None)
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_89(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema=None,
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_90(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=None,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_91(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=None,
    )


def x__parse_environment__mutmut_92(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_93(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_94(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        )


def x__parse_environment__mutmut_95(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="XXtc.fitness/check-environment/v2XX",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_96(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="TC.FITNESS/CHECK-ENVIRONMENT/V2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_97(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema=None,
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_98(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=None,
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_99(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=None,
        ),
    )


def x__parse_environment__mutmut_100(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_101(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_102(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            ),
    )


def x__parse_environment__mutmut_103(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="XXtc.fitness/git-fixture/v1XX",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_104(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="TC.FITNESS/GIT-FIXTURE/V1",
            history=_portable_git_history(git.get("history"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_105(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(None, f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_106(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), None),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_107(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_108(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("history"), ),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_109(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get(None), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_110(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("XXhistoryXX"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )


def x__parse_environment__mutmut_111(value: object, location: str) -> CaseEnvironment | GitCaseEnvironment:
    declaration = _mapping(value, location)
    schema = declaration.get("schema")
    path = declaration.get("path")
    if not isinstance(path, str) or path not in {"inherit", "empty"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    if schema == "tc.fitness/check-environment/v1" and set(declaration) == {"schema", "path"}:
        return CaseEnvironment(path=path)
    if schema != "tc.fitness/check-environment/v2" or set(declaration) != {"schema", "path", "git"}:
        raise CheckContractError(f"{location} requires a known schema and inherit/empty path")
    git_location = f"{location}.git"
    git = _mapping(declaration["git"], git_location)
    if set(git) != {"schema", "history", "checkout"} or git.get("schema") != "tc.fitness/git-fixture/v1":
        raise CheckContractError(f"{git_location} requires the tc.fitness/git-fixture/v1 schema")
    checkout = _required_string(git.get("checkout"), f"{git_location}.checkout")
    if not _GIT_CHECKOUT.fullmatch(checkout) or any(
        forbidden in checkout for forbidden in ("..", "//", "@{", ".lock")
    ):
        raise CheckContractError(f"{git_location}.checkout must be a safe refs/heads ref")
    return GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path=path,
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=_portable_git_history(git.get("HISTORY"), f"{git_location}.history"),
            checkout=checkout,
        ),
    )

mutants_x__parse_environment__mutmut['_mutmut_orig'] = x__parse_environment__mutmut_orig # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_1'] = x__parse_environment__mutmut_1 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_2'] = x__parse_environment__mutmut_2 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_3'] = x__parse_environment__mutmut_3 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_4'] = x__parse_environment__mutmut_4 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_5'] = x__parse_environment__mutmut_5 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_6'] = x__parse_environment__mutmut_6 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_7'] = x__parse_environment__mutmut_7 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_8'] = x__parse_environment__mutmut_8 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_9'] = x__parse_environment__mutmut_9 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_10'] = x__parse_environment__mutmut_10 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_11'] = x__parse_environment__mutmut_11 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_12'] = x__parse_environment__mutmut_12 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_13'] = x__parse_environment__mutmut_13 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_14'] = x__parse_environment__mutmut_14 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_15'] = x__parse_environment__mutmut_15 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_16'] = x__parse_environment__mutmut_16 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_17'] = x__parse_environment__mutmut_17 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_18'] = x__parse_environment__mutmut_18 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_19'] = x__parse_environment__mutmut_19 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_20'] = x__parse_environment__mutmut_20 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_21'] = x__parse_environment__mutmut_21 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_22'] = x__parse_environment__mutmut_22 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_23'] = x__parse_environment__mutmut_23 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_24'] = x__parse_environment__mutmut_24 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_25'] = x__parse_environment__mutmut_25 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_26'] = x__parse_environment__mutmut_26 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_27'] = x__parse_environment__mutmut_27 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_28'] = x__parse_environment__mutmut_28 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_29'] = x__parse_environment__mutmut_29 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_30'] = x__parse_environment__mutmut_30 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_31'] = x__parse_environment__mutmut_31 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_32'] = x__parse_environment__mutmut_32 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_33'] = x__parse_environment__mutmut_33 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_34'] = x__parse_environment__mutmut_34 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_35'] = x__parse_environment__mutmut_35 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_36'] = x__parse_environment__mutmut_36 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_37'] = x__parse_environment__mutmut_37 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_38'] = x__parse_environment__mutmut_38 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_39'] = x__parse_environment__mutmut_39 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_40'] = x__parse_environment__mutmut_40 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_41'] = x__parse_environment__mutmut_41 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_42'] = x__parse_environment__mutmut_42 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_43'] = x__parse_environment__mutmut_43 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_44'] = x__parse_environment__mutmut_44 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_45'] = x__parse_environment__mutmut_45 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_46'] = x__parse_environment__mutmut_46 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_47'] = x__parse_environment__mutmut_47 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_48'] = x__parse_environment__mutmut_48 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_49'] = x__parse_environment__mutmut_49 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_50'] = x__parse_environment__mutmut_50 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_51'] = x__parse_environment__mutmut_51 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_52'] = x__parse_environment__mutmut_52 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_53'] = x__parse_environment__mutmut_53 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_54'] = x__parse_environment__mutmut_54 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_55'] = x__parse_environment__mutmut_55 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_56'] = x__parse_environment__mutmut_56 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_57'] = x__parse_environment__mutmut_57 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_58'] = x__parse_environment__mutmut_58 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_59'] = x__parse_environment__mutmut_59 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_60'] = x__parse_environment__mutmut_60 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_61'] = x__parse_environment__mutmut_61 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_62'] = x__parse_environment__mutmut_62 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_63'] = x__parse_environment__mutmut_63 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_64'] = x__parse_environment__mutmut_64 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_65'] = x__parse_environment__mutmut_65 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_66'] = x__parse_environment__mutmut_66 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_67'] = x__parse_environment__mutmut_67 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_68'] = x__parse_environment__mutmut_68 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_69'] = x__parse_environment__mutmut_69 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_70'] = x__parse_environment__mutmut_70 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_71'] = x__parse_environment__mutmut_71 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_72'] = x__parse_environment__mutmut_72 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_73'] = x__parse_environment__mutmut_73 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_74'] = x__parse_environment__mutmut_74 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_75'] = x__parse_environment__mutmut_75 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_76'] = x__parse_environment__mutmut_76 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_77'] = x__parse_environment__mutmut_77 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_78'] = x__parse_environment__mutmut_78 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_79'] = x__parse_environment__mutmut_79 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_80'] = x__parse_environment__mutmut_80 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_81'] = x__parse_environment__mutmut_81 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_82'] = x__parse_environment__mutmut_82 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_83'] = x__parse_environment__mutmut_83 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_84'] = x__parse_environment__mutmut_84 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_85'] = x__parse_environment__mutmut_85 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_86'] = x__parse_environment__mutmut_86 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_87'] = x__parse_environment__mutmut_87 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_88'] = x__parse_environment__mutmut_88 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_89'] = x__parse_environment__mutmut_89 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_90'] = x__parse_environment__mutmut_90 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_91'] = x__parse_environment__mutmut_91 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_92'] = x__parse_environment__mutmut_92 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_93'] = x__parse_environment__mutmut_93 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_94'] = x__parse_environment__mutmut_94 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_95'] = x__parse_environment__mutmut_95 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_96'] = x__parse_environment__mutmut_96 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_97'] = x__parse_environment__mutmut_97 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_98'] = x__parse_environment__mutmut_98 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_99'] = x__parse_environment__mutmut_99 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_100'] = x__parse_environment__mutmut_100 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_101'] = x__parse_environment__mutmut_101 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_102'] = x__parse_environment__mutmut_102 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_103'] = x__parse_environment__mutmut_103 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_104'] = x__parse_environment__mutmut_104 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_105'] = x__parse_environment__mutmut_105 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_106'] = x__parse_environment__mutmut_106 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_107'] = x__parse_environment__mutmut_107 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_108'] = x__parse_environment__mutmut_108 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_109'] = x__parse_environment__mutmut_109 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_110'] = x__parse_environment__mutmut_110 # type: ignore # mutmut generated
mutants_x__parse_environment__mutmut['x__parse_environment__mutmut_111'] = x__parse_environment__mutmut_111 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__parse_case__mutmut)
def _parse_case(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_orig(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_1(value: object, index: int) -> ContractCase:
    location = None
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_2(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = None
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_3(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(None, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_4(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, None)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_5(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_6(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, )
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_7(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = None
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_8(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(None, f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_9(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), None)
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_10(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_11(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), )
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_12(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get(None), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_13(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("XXidXX"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_14(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("ID"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_15(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = None
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_16(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "XXenvironmentXX" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_17(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "ENVIRONMENT" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_18(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" not in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_19(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = None
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_20(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(None, f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_21(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], None)
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_22(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_23(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], )
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_24(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["XXenvironmentXX"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_25(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["ENVIRONMENT"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_26(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" or case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_27(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path != "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_28(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "XXemptyXX" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_29(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "EMPTY" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_30(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id == "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_31(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "XXunavailableXX":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_32(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "UNAVAILABLE":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_33(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError(None)
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_34(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("XXonly an unavailable case may request an empty environment pathXX")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_35(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("ONLY AN UNAVAILABLE CASE MAY REQUEST AN EMPTY ENVIRONMENT PATH")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_36(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=None,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_37(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=None,
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_38(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=None,
        environment=environment,
    )


def x__parse_case__mutmut_39(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=None,
    )


def x__parse_case__mutmut_40(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_41(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_42(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        environment=environment,
    )


def x__parse_case__mutmut_43(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        )


def x__parse_case__mutmut_44(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(None, f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_45(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), None),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_46(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_47(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), ),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_48(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get(None), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_49(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("XXfixtureXX"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_50(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("FIXTURE"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_51(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(None, f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_52(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), None),
        environment=environment,
    )


def x__parse_case__mutmut_53(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_54(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("expected"), ),
        environment=environment,
    )


def x__parse_case__mutmut_55(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get(None), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_56(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("XXexpectedXX"), f"{location}.expected"),
        environment=environment,
    )


def x__parse_case__mutmut_57(value: object, index: int) -> ContractCase:
    location = f"cases[{index}]"
    raw = _mapping(value, location)
    case_id = _required_string(raw.get("id"), f"{location}.id")
    environment: CaseEnvironment | GitCaseEnvironment = CaseEnvironment()
    if "environment" in raw:
        environment = _parse_environment(raw["environment"], f"{location}.environment")
    if environment.path == "empty" and case_id != "unavailable":
        raise CheckContractError("only an unavailable case may request an empty environment path")
    return ContractCase(
        id=case_id,
        fixture=_required_string(raw.get("fixture"), f"{location}.fixture"),
        expected=_parse_expected(raw.get("EXPECTED"), f"{location}.expected"),
        environment=environment,
    )

mutants_x__parse_case__mutmut['_mutmut_orig'] = x__parse_case__mutmut_orig # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_1'] = x__parse_case__mutmut_1 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_2'] = x__parse_case__mutmut_2 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_3'] = x__parse_case__mutmut_3 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_4'] = x__parse_case__mutmut_4 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_5'] = x__parse_case__mutmut_5 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_6'] = x__parse_case__mutmut_6 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_7'] = x__parse_case__mutmut_7 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_8'] = x__parse_case__mutmut_8 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_9'] = x__parse_case__mutmut_9 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_10'] = x__parse_case__mutmut_10 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_11'] = x__parse_case__mutmut_11 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_12'] = x__parse_case__mutmut_12 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_13'] = x__parse_case__mutmut_13 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_14'] = x__parse_case__mutmut_14 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_15'] = x__parse_case__mutmut_15 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_16'] = x__parse_case__mutmut_16 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_17'] = x__parse_case__mutmut_17 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_18'] = x__parse_case__mutmut_18 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_19'] = x__parse_case__mutmut_19 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_20'] = x__parse_case__mutmut_20 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_21'] = x__parse_case__mutmut_21 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_22'] = x__parse_case__mutmut_22 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_23'] = x__parse_case__mutmut_23 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_24'] = x__parse_case__mutmut_24 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_25'] = x__parse_case__mutmut_25 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_26'] = x__parse_case__mutmut_26 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_27'] = x__parse_case__mutmut_27 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_28'] = x__parse_case__mutmut_28 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_29'] = x__parse_case__mutmut_29 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_30'] = x__parse_case__mutmut_30 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_31'] = x__parse_case__mutmut_31 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_32'] = x__parse_case__mutmut_32 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_33'] = x__parse_case__mutmut_33 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_34'] = x__parse_case__mutmut_34 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_35'] = x__parse_case__mutmut_35 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_36'] = x__parse_case__mutmut_36 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_37'] = x__parse_case__mutmut_37 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_38'] = x__parse_case__mutmut_38 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_39'] = x__parse_case__mutmut_39 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_40'] = x__parse_case__mutmut_40 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_41'] = x__parse_case__mutmut_41 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_42'] = x__parse_case__mutmut_42 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_43'] = x__parse_case__mutmut_43 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_44'] = x__parse_case__mutmut_44 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_45'] = x__parse_case__mutmut_45 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_46'] = x__parse_case__mutmut_46 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_47'] = x__parse_case__mutmut_47 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_48'] = x__parse_case__mutmut_48 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_49'] = x__parse_case__mutmut_49 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_50'] = x__parse_case__mutmut_50 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_51'] = x__parse_case__mutmut_51 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_52'] = x__parse_case__mutmut_52 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_53'] = x__parse_case__mutmut_53 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_54'] = x__parse_case__mutmut_54 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_55'] = x__parse_case__mutmut_55 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_56'] = x__parse_case__mutmut_56 # type: ignore # mutmut generated
mutants_x__parse_case__mutmut['x__parse_case__mutmut_57'] = x__parse_case__mutmut_57 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__validate_case_set__mutmut)
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


def x__validate_case_set__mutmut_orig(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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


def x__validate_case_set__mutmut_1(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = None
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


def x__validate_case_set__mutmut_2(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = None
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


def x__validate_case_set__mutmut_3(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted(None)
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


def x__validate_case_set__mutmut_4(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(None) > 1})
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


def x__validate_case_set__mutmut_5(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) >= 1})
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


def x__validate_case_set__mutmut_6(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 2})
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


def x__validate_case_set__mutmut_7(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(None)
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


def x__validate_case_set__mutmut_8(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(None)}")
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


def x__validate_case_set__mutmut_9(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {'XX, XX'.join(duplicate_ids)}")
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


def x__validate_case_set__mutmut_10(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = None
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


def x__validate_case_set__mutmut_11(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = None
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


def x__validate_case_set__mutmut_12(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted(None)
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


def x__validate_case_set__mutmut_13(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"compliant", "violation"} + cases_by_id.keys())
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


def x__validate_case_set__mutmut_14(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"XXcompliantXX", "violation"} - cases_by_id.keys())
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


def x__validate_case_set__mutmut_15(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"COMPLIANT", "violation"} - cases_by_id.keys())
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


def x__validate_case_set__mutmut_16(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"compliant", "XXviolationXX"} - cases_by_id.keys())
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


def x__validate_case_set__mutmut_17(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"compliant", "VIOLATION"} - cases_by_id.keys())
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


def x__validate_case_set__mutmut_18(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"compliant", "violation"} - cases_by_id.keys())
    if missing:
        raise CheckContractError(None)
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


def x__validate_case_set__mutmut_19(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"compliant", "violation"} - cases_by_id.keys())
    if missing:
        raise CheckContractError(f"missing required cases: {', '.join(None)}")
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


def x__validate_case_set__mutmut_20(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"compliant", "violation"} - cases_by_id.keys())
    if missing:
        raise CheckContractError(f"missing required cases: {'XX, XX'.join(missing)}")
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


def x__validate_case_set__mutmut_21(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"compliant", "violation"} - cases_by_id.keys())
    if missing:
        raise CheckContractError(f"missing required cases: {', '.join(missing)}")
    compliant = None
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


def x__validate_case_set__mutmut_22(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"compliant", "violation"} - cases_by_id.keys())
    if missing:
        raise CheckContractError(f"missing required cases: {', '.join(missing)}")
    compliant = cases_by_id["XXcompliantXX"]
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


def x__validate_case_set__mutmut_23(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
    ids = [case.id for case in cases]
    duplicate_ids = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicate_ids:
        raise CheckContractError(f"duplicate case ids: {', '.join(duplicate_ids)}")
    cases_by_id = {case.id: case for case in cases}
    missing = sorted({"compliant", "violation"} - cases_by_id.keys())
    if missing:
        raise CheckContractError(f"missing required cases: {', '.join(missing)}")
    compliant = cases_by_id["COMPLIANT"]
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


def x__validate_case_set__mutmut_24(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or compliant.expected.exit != "zero" and compliant.expected.findings
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


def x__validate_case_set__mutmut_25(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        compliant.expected.status != "pass" and compliant.expected.exit != "zero"
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


def x__validate_case_set__mutmut_26(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        compliant.expected.status == "pass"
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


def x__validate_case_set__mutmut_27(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        compliant.expected.status != "XXpassXX"
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


def x__validate_case_set__mutmut_28(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        compliant.expected.status != "PASS"
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


def x__validate_case_set__mutmut_29(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or compliant.expected.exit == "zero"
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


def x__validate_case_set__mutmut_30(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or compliant.expected.exit != "XXzeroXX"
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


def x__validate_case_set__mutmut_31(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or compliant.expected.exit != "ZERO"
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


def x__validate_case_set__mutmut_32(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        raise CheckContractError(None)
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


def x__validate_case_set__mutmut_33(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        raise CheckContractError("XXcompliant case must expect status: pass and exit: zero with no findingsXX")
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


def x__validate_case_set__mutmut_34(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        raise CheckContractError("COMPLIANT CASE MUST EXPECT STATUS: PASS AND EXIT: ZERO WITH NO FINDINGS")
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


def x__validate_case_set__mutmut_35(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
    violation = None
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


def x__validate_case_set__mutmut_36(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
    violation = cases_by_id["XXviolationXX"]
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


def x__validate_case_set__mutmut_37(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
    violation = cases_by_id["VIOLATION"]
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


def x__validate_case_set__mutmut_38(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or violation.expected.exit != "nonzero" and not violation.expected.findings
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


def x__validate_case_set__mutmut_39(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        violation.expected.status != "fail" and violation.expected.exit != "nonzero"
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


def x__validate_case_set__mutmut_40(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        violation.expected.status == "fail"
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


def x__validate_case_set__mutmut_41(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        violation.expected.status != "XXfailXX"
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


def x__validate_case_set__mutmut_42(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        violation.expected.status != "FAIL"
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


def x__validate_case_set__mutmut_43(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or violation.expected.exit == "nonzero"
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


def x__validate_case_set__mutmut_44(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or violation.expected.exit != "XXnonzeroXX"
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


def x__validate_case_set__mutmut_45(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or violation.expected.exit != "NONZERO"
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


def x__validate_case_set__mutmut_46(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or violation.expected.findings
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


def x__validate_case_set__mutmut_47(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
            None
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


def x__validate_case_set__mutmut_48(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
            "XXviolation case must expect status: fail, exit: nonzero, and at least one findingXX"
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


def x__validate_case_set__mutmut_49(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
            "VIOLATION CASE MUST EXPECT STATUS: FAIL, EXIT: NONZERO, AND AT LEAST ONE FINDING"
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


def x__validate_case_set__mutmut_50(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
    unavailable = None
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


def x__validate_case_set__mutmut_51(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
    unavailable = cases_by_id.get(None)
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


def x__validate_case_set__mutmut_52(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
    unavailable = cases_by_id.get("XXunavailableXX")
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


def x__validate_case_set__mutmut_53(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
    unavailable = cases_by_id.get("UNAVAILABLE")
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


def x__validate_case_set__mutmut_54(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
    if dependencies:
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


def x__validate_case_set__mutmut_55(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        if unavailable is None:
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


def x__validate_case_set__mutmut_56(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
            raise CheckContractError(None)
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


def x__validate_case_set__mutmut_57(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
            raise CheckContractError("XXunavailable case requires at least one dependencyXX")
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


def x__validate_case_set__mutmut_58(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
            raise CheckContractError("UNAVAILABLE CASE REQUIRES AT LEAST ONE DEPENDENCY")
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


def x__validate_case_set__mutmut_59(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or unavailable.expected.status != "error" and unavailable.expected.exit != "nonzero"
    ):
        raise CheckContractError(
            "dependency-backed contracts require an unavailable case with status: error and exit: nonzero"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_60(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        unavailable is None and unavailable.expected.status != "error"
        or unavailable.expected.exit != "nonzero"
    ):
        raise CheckContractError(
            "dependency-backed contracts require an unavailable case with status: error and exit: nonzero"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_61(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        unavailable is not None
        or unavailable.expected.status != "error"
        or unavailable.expected.exit != "nonzero"
    ):
        raise CheckContractError(
            "dependency-backed contracts require an unavailable case with status: error and exit: nonzero"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_62(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or unavailable.expected.status == "error"
        or unavailable.expected.exit != "nonzero"
    ):
        raise CheckContractError(
            "dependency-backed contracts require an unavailable case with status: error and exit: nonzero"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_63(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or unavailable.expected.status != "XXerrorXX"
        or unavailable.expected.exit != "nonzero"
    ):
        raise CheckContractError(
            "dependency-backed contracts require an unavailable case with status: error and exit: nonzero"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_64(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or unavailable.expected.status != "ERROR"
        or unavailable.expected.exit != "nonzero"
    ):
        raise CheckContractError(
            "dependency-backed contracts require an unavailable case with status: error and exit: nonzero"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_65(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or unavailable.expected.exit == "nonzero"
    ):
        raise CheckContractError(
            "dependency-backed contracts require an unavailable case with status: error and exit: nonzero"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_66(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or unavailable.expected.exit != "XXnonzeroXX"
    ):
        raise CheckContractError(
            "dependency-backed contracts require an unavailable case with status: error and exit: nonzero"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_67(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        or unavailable.expected.exit != "NONZERO"
    ):
        raise CheckContractError(
            "dependency-backed contracts require an unavailable case with status: error and exit: nonzero"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_68(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
            None
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_69(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
            "XXdependency-backed contracts require an unavailable case with status: error and exit: nonzeroXX"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_70(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
            "DEPENDENCY-BACKED CONTRACTS REQUIRE AN UNAVAILABLE CASE WITH STATUS: ERROR AND EXIT: NONZERO"
        )
    if not unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_71(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
    if unavailable.expected.findings:
        raise CheckContractError("unavailable case must expect at least one stable finding")


def x__validate_case_set__mutmut_72(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        raise CheckContractError(None)


def x__validate_case_set__mutmut_73(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        raise CheckContractError("XXunavailable case must expect at least one stable findingXX")


def x__validate_case_set__mutmut_74(cases: tuple[ContractCase, ...], dependencies: tuple[str, ...]) -> None:
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
        raise CheckContractError("UNAVAILABLE CASE MUST EXPECT AT LEAST ONE STABLE FINDING")

mutants_x__validate_case_set__mutmut['_mutmut_orig'] = x__validate_case_set__mutmut_orig # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_1'] = x__validate_case_set__mutmut_1 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_2'] = x__validate_case_set__mutmut_2 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_3'] = x__validate_case_set__mutmut_3 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_4'] = x__validate_case_set__mutmut_4 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_5'] = x__validate_case_set__mutmut_5 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_6'] = x__validate_case_set__mutmut_6 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_7'] = x__validate_case_set__mutmut_7 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_8'] = x__validate_case_set__mutmut_8 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_9'] = x__validate_case_set__mutmut_9 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_10'] = x__validate_case_set__mutmut_10 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_11'] = x__validate_case_set__mutmut_11 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_12'] = x__validate_case_set__mutmut_12 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_13'] = x__validate_case_set__mutmut_13 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_14'] = x__validate_case_set__mutmut_14 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_15'] = x__validate_case_set__mutmut_15 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_16'] = x__validate_case_set__mutmut_16 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_17'] = x__validate_case_set__mutmut_17 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_18'] = x__validate_case_set__mutmut_18 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_19'] = x__validate_case_set__mutmut_19 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_20'] = x__validate_case_set__mutmut_20 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_21'] = x__validate_case_set__mutmut_21 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_22'] = x__validate_case_set__mutmut_22 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_23'] = x__validate_case_set__mutmut_23 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_24'] = x__validate_case_set__mutmut_24 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_25'] = x__validate_case_set__mutmut_25 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_26'] = x__validate_case_set__mutmut_26 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_27'] = x__validate_case_set__mutmut_27 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_28'] = x__validate_case_set__mutmut_28 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_29'] = x__validate_case_set__mutmut_29 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_30'] = x__validate_case_set__mutmut_30 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_31'] = x__validate_case_set__mutmut_31 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_32'] = x__validate_case_set__mutmut_32 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_33'] = x__validate_case_set__mutmut_33 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_34'] = x__validate_case_set__mutmut_34 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_35'] = x__validate_case_set__mutmut_35 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_36'] = x__validate_case_set__mutmut_36 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_37'] = x__validate_case_set__mutmut_37 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_38'] = x__validate_case_set__mutmut_38 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_39'] = x__validate_case_set__mutmut_39 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_40'] = x__validate_case_set__mutmut_40 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_41'] = x__validate_case_set__mutmut_41 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_42'] = x__validate_case_set__mutmut_42 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_43'] = x__validate_case_set__mutmut_43 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_44'] = x__validate_case_set__mutmut_44 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_45'] = x__validate_case_set__mutmut_45 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_46'] = x__validate_case_set__mutmut_46 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_47'] = x__validate_case_set__mutmut_47 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_48'] = x__validate_case_set__mutmut_48 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_49'] = x__validate_case_set__mutmut_49 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_50'] = x__validate_case_set__mutmut_50 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_51'] = x__validate_case_set__mutmut_51 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_52'] = x__validate_case_set__mutmut_52 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_53'] = x__validate_case_set__mutmut_53 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_54'] = x__validate_case_set__mutmut_54 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_55'] = x__validate_case_set__mutmut_55 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_56'] = x__validate_case_set__mutmut_56 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_57'] = x__validate_case_set__mutmut_57 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_58'] = x__validate_case_set__mutmut_58 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_59'] = x__validate_case_set__mutmut_59 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_60'] = x__validate_case_set__mutmut_60 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_61'] = x__validate_case_set__mutmut_61 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_62'] = x__validate_case_set__mutmut_62 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_63'] = x__validate_case_set__mutmut_63 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_64'] = x__validate_case_set__mutmut_64 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_65'] = x__validate_case_set__mutmut_65 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_66'] = x__validate_case_set__mutmut_66 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_67'] = x__validate_case_set__mutmut_67 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_68'] = x__validate_case_set__mutmut_68 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_69'] = x__validate_case_set__mutmut_69 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_70'] = x__validate_case_set__mutmut_70 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_71'] = x__validate_case_set__mutmut_71 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_72'] = x__validate_case_set__mutmut_72 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_73'] = x__validate_case_set__mutmut_73 # type: ignore # mutmut generated
mutants_x__validate_case_set__mutmut['x__validate_case_set__mutmut_74'] = x__validate_case_set__mutmut_74 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__parse_evidence_classification__mutmut)
def _parse_evidence_classification(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_orig(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_1(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = None
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_2(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(None)
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_3(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get(None, "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_4(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", None))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_5(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_6(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", ))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_7(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("XXevidence_classXX", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_8(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("EVIDENCE_CLASS", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_9(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "XXunclassifiedXX"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_10(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "UNCLASSIFIED"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_11(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_12(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(None)
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_13(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(None)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_14(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = None
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_15(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(None)
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_16(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get(None, "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_17(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", None))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_18(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_19(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", ))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_20(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("XXlive_qualificationXX", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_21(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("LIVE_QUALIFICATION", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_22(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "XXnot-requiredXX"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_23(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "NOT-REQUIRED"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_24(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_25(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(None)
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_26(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(None)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_27(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = None
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_28(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get(None, False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_29(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", None)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_30(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get(False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_31(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", )
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_32(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("XXrelease_admissionXX", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_33(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("RELEASE_ADMISSION", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_34(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", True)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_35(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(None) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_36(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_37(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError(None)
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_38(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("XXrelease_admission must be a booleanXX")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_39(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("RELEASE_ADMISSION MUST BE A BOOLEAN")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_40(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError(None)
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_41(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("XXcontract manifests cannot grant release admissionXX")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_42(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("CONTRACT MANIFESTS CANNOT GRANT RELEASE ADMISSION")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_43(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" or live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_44(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class != "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_45(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "XXprotocol-unitXX" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_46(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "PROTOCOL-UNIT" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_47(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification == "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_48(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "XXrequired-unmetXX":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_49(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "REQUIRED-UNMET":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_50(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError(None)
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_51(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("XXprotocol-unit evidence requires an explicitly unmet live qualificationXX")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_52(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("PROTOCOL-UNIT EVIDENCE REQUIRES AN EXPLICITLY UNMET LIVE QUALIFICATION")
    return evidence_class, live_qualification, False


def x__parse_evidence_classification__mutmut_53(raw: Mapping[str, Any]) -> tuple[str, str, bool]:
    """Bind evidence labels while reserving admission authority for protected receipts."""
    evidence_class = str(raw.get("evidence_class", "unclassified"))
    if evidence_class not in _EVIDENCE_CLASSES:
        raise CheckContractError(f"evidence_class must be one of {sorted(_EVIDENCE_CLASSES)}")
    live_qualification = str(raw.get("live_qualification", "not-required"))
    if live_qualification not in _LIVE_QUALIFICATIONS:
        raise CheckContractError(f"live_qualification must be one of {sorted(_LIVE_QUALIFICATIONS)}")
    release_admission = raw.get("release_admission", False)
    if type(release_admission) is not bool:
        raise CheckContractError("release_admission must be a boolean")
    if release_admission:
        raise CheckContractError("contract manifests cannot grant release admission")
    if evidence_class == "protocol-unit" and live_qualification != "required-unmet":
        raise CheckContractError("protocol-unit evidence requires an explicitly unmet live qualification")
    return evidence_class, live_qualification, True

mutants_x__parse_evidence_classification__mutmut['_mutmut_orig'] = x__parse_evidence_classification__mutmut_orig # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_1'] = x__parse_evidence_classification__mutmut_1 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_2'] = x__parse_evidence_classification__mutmut_2 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_3'] = x__parse_evidence_classification__mutmut_3 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_4'] = x__parse_evidence_classification__mutmut_4 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_5'] = x__parse_evidence_classification__mutmut_5 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_6'] = x__parse_evidence_classification__mutmut_6 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_7'] = x__parse_evidence_classification__mutmut_7 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_8'] = x__parse_evidence_classification__mutmut_8 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_9'] = x__parse_evidence_classification__mutmut_9 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_10'] = x__parse_evidence_classification__mutmut_10 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_11'] = x__parse_evidence_classification__mutmut_11 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_12'] = x__parse_evidence_classification__mutmut_12 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_13'] = x__parse_evidence_classification__mutmut_13 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_14'] = x__parse_evidence_classification__mutmut_14 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_15'] = x__parse_evidence_classification__mutmut_15 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_16'] = x__parse_evidence_classification__mutmut_16 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_17'] = x__parse_evidence_classification__mutmut_17 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_18'] = x__parse_evidence_classification__mutmut_18 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_19'] = x__parse_evidence_classification__mutmut_19 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_20'] = x__parse_evidence_classification__mutmut_20 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_21'] = x__parse_evidence_classification__mutmut_21 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_22'] = x__parse_evidence_classification__mutmut_22 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_23'] = x__parse_evidence_classification__mutmut_23 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_24'] = x__parse_evidence_classification__mutmut_24 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_25'] = x__parse_evidence_classification__mutmut_25 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_26'] = x__parse_evidence_classification__mutmut_26 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_27'] = x__parse_evidence_classification__mutmut_27 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_28'] = x__parse_evidence_classification__mutmut_28 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_29'] = x__parse_evidence_classification__mutmut_29 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_30'] = x__parse_evidence_classification__mutmut_30 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_31'] = x__parse_evidence_classification__mutmut_31 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_32'] = x__parse_evidence_classification__mutmut_32 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_33'] = x__parse_evidence_classification__mutmut_33 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_34'] = x__parse_evidence_classification__mutmut_34 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_35'] = x__parse_evidence_classification__mutmut_35 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_36'] = x__parse_evidence_classification__mutmut_36 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_37'] = x__parse_evidence_classification__mutmut_37 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_38'] = x__parse_evidence_classification__mutmut_38 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_39'] = x__parse_evidence_classification__mutmut_39 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_40'] = x__parse_evidence_classification__mutmut_40 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_41'] = x__parse_evidence_classification__mutmut_41 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_42'] = x__parse_evidence_classification__mutmut_42 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_43'] = x__parse_evidence_classification__mutmut_43 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_44'] = x__parse_evidence_classification__mutmut_44 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_45'] = x__parse_evidence_classification__mutmut_45 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_46'] = x__parse_evidence_classification__mutmut_46 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_47'] = x__parse_evidence_classification__mutmut_47 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_48'] = x__parse_evidence_classification__mutmut_48 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_49'] = x__parse_evidence_classification__mutmut_49 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_50'] = x__parse_evidence_classification__mutmut_50 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_51'] = x__parse_evidence_classification__mutmut_51 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_52'] = x__parse_evidence_classification__mutmut_52 # type: ignore # mutmut generated
mutants_x__parse_evidence_classification__mutmut['x__parse_evidence_classification__mutmut_53'] = x__parse_evidence_classification__mutmut_53 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_load_check_contract__mutmut)
def load_check_contract(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_orig(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_1(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None or not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_2(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is not None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_3(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_4(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(None)
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_5(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = None
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_6(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(None, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_7(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=None, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_8(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=None)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_9(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_10(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_11(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, )
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_12(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=False, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_13(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is None:
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_14(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(None)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_15(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = None
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_16(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(None, str(path))
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_17(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, None)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_18(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(str(path))
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_19(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, )
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_20(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(None))
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_21(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get(None) != SCHEMA:
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_22(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("XXschemaXX") != SCHEMA:
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_23(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("SCHEMA") != SCHEMA:
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_24(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") == SCHEMA:
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_25(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(None)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_26(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = None
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_27(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(None, "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_28(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), None)
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_29(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string("check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_30(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), )
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_31(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get(None), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_32(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("XXcheckXX"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_33(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("CHECK"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_34(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "XXcheckXX")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_35(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "CHECK")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_36(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") and check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_37(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_38(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith(None) or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_39(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("XXcore:XX") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_40(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("CORE:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_41(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check != "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_42(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "XXcore:XX":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_43(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "CORE:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_44(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError(None)
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_45(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("XXcheck must use the core:<module> namespaceXX")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_46(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("CHECK MUST USE THE CORE:<MODULE> NAMESPACE")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_47(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = None
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_48(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(None, "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_49(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), None)
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_50(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping("config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_51(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), )
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_52(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get(None), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_53(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("XXconfigXX"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_54(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("CONFIG"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_55(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "XXconfigXX")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_56(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "CONFIG")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_57(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = None
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_58(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(None)
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_59(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(None, index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_60(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, None) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_61(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(index) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_62(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, ) for index, item in enumerate(_list(raw.get("cases"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_63(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(None))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_64(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(None, "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_65(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), None)))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_66(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list("cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_67(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), )))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_68(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get(None), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_69(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("XXcasesXX"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_70(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("CASES"), "cases")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_71(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "XXcasesXX")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_72(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
    if error is not None:
        raise CheckContractError(f"{path}: {error}")
    raw = _mapping(value, str(path))
    if raw.get("schema") != SCHEMA:
        raise CheckContractError(f"schema must be {SCHEMA!r}")
    check = _required_string(raw.get("check"), "check")
    if not check.startswith("core:") or check == "core:":
        raise CheckContractError("check must use the core:<module> namespace")
    config = _mapping(raw.get("config"), "config")
    cases = tuple(_parse_case(item, index) for index, item in enumerate(_list(raw.get("cases"), "CASES")))
    dependencies = tuple(
        _required_string(item, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_73(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    dependencies = None
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_74(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        None
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_75(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        _required_string(None, f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_76(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        _required_string(item, None)
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_77(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        _required_string(f"dependencies[{index}]")
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_78(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        _required_string(item, )
        for index, item in enumerate(_list(raw.get("dependencies"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_79(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        for index, item in enumerate(None)
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_80(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        for index, item in enumerate(_list(None, "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_81(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        for index, item in enumerate(_list(raw.get("dependencies"), None))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_82(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        for index, item in enumerate(_list("dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_83(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        for index, item in enumerate(_list(raw.get("dependencies"), ))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_84(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        for index, item in enumerate(_list(raw.get(None), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_85(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        for index, item in enumerate(_list(raw.get("XXdependenciesXX"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_86(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        for index, item in enumerate(_list(raw.get("DEPENDENCIES"), "dependencies"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_87(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        for index, item in enumerate(_list(raw.get("dependencies"), "XXdependenciesXX"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_88(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
        for index, item in enumerate(_list(raw.get("dependencies"), "DEPENDENCIES"))
    )
    _validate_case_set(cases, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_89(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    _validate_case_set(None, dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_90(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    _validate_case_set(cases, None)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_91(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    _validate_case_set(dependencies)
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_92(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    _validate_case_set(cases, )
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_93(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = None
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_94(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(None)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_95(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=None,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_96(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=None,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_97(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=None,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_98(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=None,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_99(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=None,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_100(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=None,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_101(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=None,
    )


def x_load_check_contract__mutmut_102(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_103(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_104(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_105(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_106(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        live_qualification=live_qualification,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_107(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        release_admission=release_admission,
    )


def x_load_check_contract__mutmut_108(path: Path, *, source: bytes | None = None) -> CheckContract:
    """Load and validate one check-contract manifest."""
    if source is None and not path.is_file():
        raise CheckContractError(f"contract manifest does not exist: {path}")
    value, error = load_yaml(path, reject_duplicate_keys=True, source=source)
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
    evidence_class, live_qualification, release_admission = _parse_evidence_classification(raw)
    return CheckContract(
        check=check,
        config=config,
        cases=cases,
        dependencies=dependencies,
        evidence_class=evidence_class,
        live_qualification=live_qualification,
        )

mutants_x_load_check_contract__mutmut['_mutmut_orig'] = x_load_check_contract__mutmut_orig # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_1'] = x_load_check_contract__mutmut_1 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_2'] = x_load_check_contract__mutmut_2 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_3'] = x_load_check_contract__mutmut_3 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_4'] = x_load_check_contract__mutmut_4 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_5'] = x_load_check_contract__mutmut_5 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_6'] = x_load_check_contract__mutmut_6 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_7'] = x_load_check_contract__mutmut_7 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_8'] = x_load_check_contract__mutmut_8 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_9'] = x_load_check_contract__mutmut_9 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_10'] = x_load_check_contract__mutmut_10 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_11'] = x_load_check_contract__mutmut_11 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_12'] = x_load_check_contract__mutmut_12 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_13'] = x_load_check_contract__mutmut_13 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_14'] = x_load_check_contract__mutmut_14 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_15'] = x_load_check_contract__mutmut_15 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_16'] = x_load_check_contract__mutmut_16 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_17'] = x_load_check_contract__mutmut_17 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_18'] = x_load_check_contract__mutmut_18 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_19'] = x_load_check_contract__mutmut_19 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_20'] = x_load_check_contract__mutmut_20 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_21'] = x_load_check_contract__mutmut_21 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_22'] = x_load_check_contract__mutmut_22 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_23'] = x_load_check_contract__mutmut_23 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_24'] = x_load_check_contract__mutmut_24 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_25'] = x_load_check_contract__mutmut_25 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_26'] = x_load_check_contract__mutmut_26 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_27'] = x_load_check_contract__mutmut_27 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_28'] = x_load_check_contract__mutmut_28 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_29'] = x_load_check_contract__mutmut_29 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_30'] = x_load_check_contract__mutmut_30 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_31'] = x_load_check_contract__mutmut_31 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_32'] = x_load_check_contract__mutmut_32 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_33'] = x_load_check_contract__mutmut_33 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_34'] = x_load_check_contract__mutmut_34 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_35'] = x_load_check_contract__mutmut_35 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_36'] = x_load_check_contract__mutmut_36 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_37'] = x_load_check_contract__mutmut_37 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_38'] = x_load_check_contract__mutmut_38 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_39'] = x_load_check_contract__mutmut_39 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_40'] = x_load_check_contract__mutmut_40 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_41'] = x_load_check_contract__mutmut_41 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_42'] = x_load_check_contract__mutmut_42 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_43'] = x_load_check_contract__mutmut_43 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_44'] = x_load_check_contract__mutmut_44 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_45'] = x_load_check_contract__mutmut_45 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_46'] = x_load_check_contract__mutmut_46 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_47'] = x_load_check_contract__mutmut_47 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_48'] = x_load_check_contract__mutmut_48 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_49'] = x_load_check_contract__mutmut_49 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_50'] = x_load_check_contract__mutmut_50 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_51'] = x_load_check_contract__mutmut_51 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_52'] = x_load_check_contract__mutmut_52 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_53'] = x_load_check_contract__mutmut_53 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_54'] = x_load_check_contract__mutmut_54 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_55'] = x_load_check_contract__mutmut_55 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_56'] = x_load_check_contract__mutmut_56 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_57'] = x_load_check_contract__mutmut_57 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_58'] = x_load_check_contract__mutmut_58 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_59'] = x_load_check_contract__mutmut_59 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_60'] = x_load_check_contract__mutmut_60 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_61'] = x_load_check_contract__mutmut_61 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_62'] = x_load_check_contract__mutmut_62 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_63'] = x_load_check_contract__mutmut_63 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_64'] = x_load_check_contract__mutmut_64 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_65'] = x_load_check_contract__mutmut_65 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_66'] = x_load_check_contract__mutmut_66 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_67'] = x_load_check_contract__mutmut_67 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_68'] = x_load_check_contract__mutmut_68 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_69'] = x_load_check_contract__mutmut_69 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_70'] = x_load_check_contract__mutmut_70 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_71'] = x_load_check_contract__mutmut_71 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_72'] = x_load_check_contract__mutmut_72 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_73'] = x_load_check_contract__mutmut_73 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_74'] = x_load_check_contract__mutmut_74 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_75'] = x_load_check_contract__mutmut_75 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_76'] = x_load_check_contract__mutmut_76 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_77'] = x_load_check_contract__mutmut_77 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_78'] = x_load_check_contract__mutmut_78 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_79'] = x_load_check_contract__mutmut_79 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_80'] = x_load_check_contract__mutmut_80 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_81'] = x_load_check_contract__mutmut_81 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_82'] = x_load_check_contract__mutmut_82 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_83'] = x_load_check_contract__mutmut_83 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_84'] = x_load_check_contract__mutmut_84 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_85'] = x_load_check_contract__mutmut_85 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_86'] = x_load_check_contract__mutmut_86 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_87'] = x_load_check_contract__mutmut_87 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_88'] = x_load_check_contract__mutmut_88 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_89'] = x_load_check_contract__mutmut_89 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_90'] = x_load_check_contract__mutmut_90 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_91'] = x_load_check_contract__mutmut_91 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_92'] = x_load_check_contract__mutmut_92 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_93'] = x_load_check_contract__mutmut_93 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_94'] = x_load_check_contract__mutmut_94 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_95'] = x_load_check_contract__mutmut_95 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_96'] = x_load_check_contract__mutmut_96 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_97'] = x_load_check_contract__mutmut_97 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_98'] = x_load_check_contract__mutmut_98 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_99'] = x_load_check_contract__mutmut_99 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_100'] = x_load_check_contract__mutmut_100 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_101'] = x_load_check_contract__mutmut_101 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_102'] = x_load_check_contract__mutmut_102 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_103'] = x_load_check_contract__mutmut_103 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_104'] = x_load_check_contract__mutmut_104 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_105'] = x_load_check_contract__mutmut_105 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_106'] = x_load_check_contract__mutmut_106 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_107'] = x_load_check_contract__mutmut_107 # type: ignore # mutmut generated
mutants_x_load_check_contract__mutmut['x_load_check_contract__mutmut_108'] = x_load_check_contract__mutmut_108 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_registered_contract_directory__mutmut)
def registered_contract_directory(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_orig(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_1(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() and path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_2(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_3(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = None
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_4(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path * "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_5(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "XXcontract.yamlXX"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_6(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "CONTRACT.YAML"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_7(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = None
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_8(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(None)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_9(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" and contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_10(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check == f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_11(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_12(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = None
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_13(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(None)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_14(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = None
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_15(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path * relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_16(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or not fixture.is_dir() and fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_17(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts and not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_18(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() and ".." in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_19(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or "XX..XX" in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_20(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." not in relative.parts or not fixture.is_dir() or fixture.is_symlink():
            return None
    return contract


def x_registered_contract_directory__mutmut_21(path: Path, registered_checks: tuple[str, ...]) -> CheckContract | None:
    """Return the manifest only when ``path`` is a complete bound fixture registry.

    Test discovery uses this as an authority boundary. A directory name, an
    invalid manifest, a copied manifest, or a missing/escaping fixture cannot
    hide authored tests from pytest or the tier gate.
    """
    if not path.is_dir() or path.is_symlink():
        return None
    manifest = path / "contract.yaml"
    try:
        contract = load_check_contract(manifest)
    except (CheckContractError, OSError):
        return None
    if contract.check != f"core:{path.name}" or contract.check not in registered_checks:
        return None
    for case in contract.cases:
        relative = Path(case.fixture)
        fixture = path / relative
        if relative.is_absolute() or ".." in relative.parts or fixture.is_dir() or fixture.is_symlink():
            return None
    return contract

mutants_x_registered_contract_directory__mutmut['_mutmut_orig'] = x_registered_contract_directory__mutmut_orig # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_1'] = x_registered_contract_directory__mutmut_1 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_2'] = x_registered_contract_directory__mutmut_2 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_3'] = x_registered_contract_directory__mutmut_3 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_4'] = x_registered_contract_directory__mutmut_4 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_5'] = x_registered_contract_directory__mutmut_5 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_6'] = x_registered_contract_directory__mutmut_6 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_7'] = x_registered_contract_directory__mutmut_7 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_8'] = x_registered_contract_directory__mutmut_8 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_9'] = x_registered_contract_directory__mutmut_9 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_10'] = x_registered_contract_directory__mutmut_10 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_11'] = x_registered_contract_directory__mutmut_11 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_12'] = x_registered_contract_directory__mutmut_12 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_13'] = x_registered_contract_directory__mutmut_13 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_14'] = x_registered_contract_directory__mutmut_14 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_15'] = x_registered_contract_directory__mutmut_15 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_16'] = x_registered_contract_directory__mutmut_16 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_17'] = x_registered_contract_directory__mutmut_17 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_18'] = x_registered_contract_directory__mutmut_18 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_19'] = x_registered_contract_directory__mutmut_19 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_20'] = x_registered_contract_directory__mutmut_20 # type: ignore # mutmut generated
mutants_x_registered_contract_directory__mutmut['x_registered_contract_directory__mutmut_21'] = x_registered_contract_directory__mutmut_21 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_validate_contract_registry__mutmut)
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


def x_validate_contract_registry__mutmut_orig(
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


def x_validate_contract_registry__mutmut_1(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = None
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


def x_validate_contract_registry__mutmut_2(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(None)
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


def x_validate_contract_registry__mutmut_3(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") and check == "core:")
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


def x_validate_contract_registry__mutmut_4(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if check.startswith("core:") or check == "core:")
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


def x_validate_contract_registry__mutmut_5(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith(None) or check == "core:")
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


def x_validate_contract_registry__mutmut_6(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("XXcore:XX") or check == "core:")
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


def x_validate_contract_registry__mutmut_7(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("CORE:") or check == "core:")
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


def x_validate_contract_registry__mutmut_8(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check != "core:")
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


def x_validate_contract_registry__mutmut_9(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "XXcore:XX")
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


def x_validate_contract_registry__mutmut_10(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "CORE:")
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


def x_validate_contract_registry__mutmut_11(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(None)
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


def x_validate_contract_registry__mutmut_12(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(None)}")
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


def x_validate_contract_registry__mutmut_13(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {'XX, XX'.join(invalid_ids)}")
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


def x_validate_contract_registry__mutmut_14(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = None
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


def x_validate_contract_registry__mutmut_15(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix(None) for check in core_checks]
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


def x_validate_contract_registry__mutmut_16(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removesuffix("core:") for check in core_checks]
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


def x_validate_contract_registry__mutmut_17(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("XXcore:XX") for check in core_checks]
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


def x_validate_contract_registry__mutmut_18(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("CORE:") for check in core_checks]
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


def x_validate_contract_registry__mutmut_19(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("core:") for check in core_checks]
    duplicate_names = None
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


def x_validate_contract_registry__mutmut_20(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("core:") for check in core_checks]
    duplicate_names = sorted(None)
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


def x_validate_contract_registry__mutmut_21(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("core:") for check in core_checks]
    duplicate_names = sorted({name for name in expected_names if expected_names.count(None) > 1})
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


def x_validate_contract_registry__mutmut_22(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("core:") for check in core_checks]
    duplicate_names = sorted({name for name in expected_names if expected_names.count(name) >= 1})
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


def x_validate_contract_registry__mutmut_23(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("core:") for check in core_checks]
    duplicate_names = sorted({name for name in expected_names if expected_names.count(name) > 2})
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


def x_validate_contract_registry__mutmut_24(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("core:") for check in core_checks]
    duplicate_names = sorted({name for name in expected_names if expected_names.count(name) > 1})
    if duplicate_names:
        raise CheckContractError(None)
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


def x_validate_contract_registry__mutmut_25(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("core:") for check in core_checks]
    duplicate_names = sorted({name for name in expected_names if expected_names.count(name) > 1})
    if duplicate_names:
        raise CheckContractError(f"duplicate CORE_CHECKS ids: {', '.join(None)}")
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


def x_validate_contract_registry__mutmut_26(
    core_checks: tuple[str, ...], contracts_root: Path
) -> tuple[CheckContract, ...]:
    """Require exact directory coverage and bind every manifest to its directory."""
    invalid_ids = sorted(check for check in core_checks if not check.startswith("core:") or check == "core:")
    if invalid_ids:
        raise CheckContractError(f"CORE_CHECKS ids must use core:<module>: {', '.join(invalid_ids)}")
    expected_names = [check.removeprefix("core:") for check in core_checks]
    duplicate_names = sorted({name for name in expected_names if expected_names.count(name) > 1})
    if duplicate_names:
        raise CheckContractError(f"duplicate CORE_CHECKS ids: {'XX, XX'.join(duplicate_names)}")
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


def x_validate_contract_registry__mutmut_27(
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
    if contracts_root.is_dir():
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


def x_validate_contract_registry__mutmut_28(
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
        raise CheckContractError(None)
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


def x_validate_contract_registry__mutmut_29(
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
    expected = None
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


def x_validate_contract_registry__mutmut_30(
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
    expected = set(None)
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


def x_validate_contract_registry__mutmut_31(
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
    actual = None
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


def x_validate_contract_registry__mutmut_32(
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
    problems: list[str] = None
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


def x_validate_contract_registry__mutmut_33(
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
    missing = None
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


def x_validate_contract_registry__mutmut_34(
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
    missing = sorted(None)
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


def x_validate_contract_registry__mutmut_35(
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
    missing = sorted(expected + actual)
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


def x_validate_contract_registry__mutmut_36(
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
    orphan = None
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


def x_validate_contract_registry__mutmut_37(
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
    orphan = sorted(None)
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


def x_validate_contract_registry__mutmut_38(
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
    orphan = sorted(actual + expected)
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


def x_validate_contract_registry__mutmut_39(
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
        problems.append(None)
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


def x_validate_contract_registry__mutmut_40(
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
        problems.append(f"missing contract directories: {', '.join(None)}")
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


def x_validate_contract_registry__mutmut_41(
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
        problems.append(f"missing contract directories: {'XX, XX'.join(missing)}")
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


def x_validate_contract_registry__mutmut_42(
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
        problems.append(None)
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


def x_validate_contract_registry__mutmut_43(
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
        problems.append(f"orphan contract directories: {', '.join(None)}")
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


def x_validate_contract_registry__mutmut_44(
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
        problems.append(f"orphan contract directories: {'XX, XX'.join(orphan)}")
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


def x_validate_contract_registry__mutmut_45(
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
        raise CheckContractError(None)

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


def x_validate_contract_registry__mutmut_46(
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
        raise CheckContractError("; ".join(None))

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


def x_validate_contract_registry__mutmut_47(
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
        raise CheckContractError("XX; XX".join(problems))

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


def x_validate_contract_registry__mutmut_48(
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

    contracts: list[CheckContract] = None
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


def x_validate_contract_registry__mutmut_49(
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
    for name in sorted(None):
        manifest = contracts_root / name / "contract.yaml"
        contract = load_check_contract(manifest)
        required_id = f"core:{name}"
        if contract.check != required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_50(
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
        manifest = None
        contract = load_check_contract(manifest)
        required_id = f"core:{name}"
        if contract.check != required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_51(
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
        manifest = contracts_root / name * "contract.yaml"
        contract = load_check_contract(manifest)
        required_id = f"core:{name}"
        if contract.check != required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_52(
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
        manifest = contracts_root * name / "contract.yaml"
        contract = load_check_contract(manifest)
        required_id = f"core:{name}"
        if contract.check != required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_53(
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
        manifest = contracts_root / name / "XXcontract.yamlXX"
        contract = load_check_contract(manifest)
        required_id = f"core:{name}"
        if contract.check != required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_54(
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
        manifest = contracts_root / name / "CONTRACT.YAML"
        contract = load_check_contract(manifest)
        required_id = f"core:{name}"
        if contract.check != required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_55(
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
        contract = None
        required_id = f"core:{name}"
        if contract.check != required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_56(
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
        contract = load_check_contract(None)
        required_id = f"core:{name}"
        if contract.check != required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_57(
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
        required_id = None
        if contract.check != required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_58(
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
        if contract.check == required_id:
            raise CheckContractError(
                f"{name}/contract.yaml must declare {required_id}, found {contract.check}"
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_59(
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
                None
            )
        contracts.append(contract)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_60(
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
        contracts.append(None)
    return tuple(contracts)


def x_validate_contract_registry__mutmut_61(
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
    return tuple(None)

mutants_x_validate_contract_registry__mutmut['_mutmut_orig'] = x_validate_contract_registry__mutmut_orig # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_1'] = x_validate_contract_registry__mutmut_1 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_2'] = x_validate_contract_registry__mutmut_2 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_3'] = x_validate_contract_registry__mutmut_3 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_4'] = x_validate_contract_registry__mutmut_4 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_5'] = x_validate_contract_registry__mutmut_5 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_6'] = x_validate_contract_registry__mutmut_6 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_7'] = x_validate_contract_registry__mutmut_7 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_8'] = x_validate_contract_registry__mutmut_8 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_9'] = x_validate_contract_registry__mutmut_9 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_10'] = x_validate_contract_registry__mutmut_10 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_11'] = x_validate_contract_registry__mutmut_11 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_12'] = x_validate_contract_registry__mutmut_12 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_13'] = x_validate_contract_registry__mutmut_13 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_14'] = x_validate_contract_registry__mutmut_14 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_15'] = x_validate_contract_registry__mutmut_15 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_16'] = x_validate_contract_registry__mutmut_16 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_17'] = x_validate_contract_registry__mutmut_17 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_18'] = x_validate_contract_registry__mutmut_18 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_19'] = x_validate_contract_registry__mutmut_19 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_20'] = x_validate_contract_registry__mutmut_20 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_21'] = x_validate_contract_registry__mutmut_21 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_22'] = x_validate_contract_registry__mutmut_22 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_23'] = x_validate_contract_registry__mutmut_23 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_24'] = x_validate_contract_registry__mutmut_24 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_25'] = x_validate_contract_registry__mutmut_25 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_26'] = x_validate_contract_registry__mutmut_26 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_27'] = x_validate_contract_registry__mutmut_27 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_28'] = x_validate_contract_registry__mutmut_28 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_29'] = x_validate_contract_registry__mutmut_29 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_30'] = x_validate_contract_registry__mutmut_30 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_31'] = x_validate_contract_registry__mutmut_31 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_32'] = x_validate_contract_registry__mutmut_32 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_33'] = x_validate_contract_registry__mutmut_33 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_34'] = x_validate_contract_registry__mutmut_34 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_35'] = x_validate_contract_registry__mutmut_35 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_36'] = x_validate_contract_registry__mutmut_36 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_37'] = x_validate_contract_registry__mutmut_37 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_38'] = x_validate_contract_registry__mutmut_38 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_39'] = x_validate_contract_registry__mutmut_39 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_40'] = x_validate_contract_registry__mutmut_40 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_41'] = x_validate_contract_registry__mutmut_41 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_42'] = x_validate_contract_registry__mutmut_42 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_43'] = x_validate_contract_registry__mutmut_43 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_44'] = x_validate_contract_registry__mutmut_44 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_45'] = x_validate_contract_registry__mutmut_45 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_46'] = x_validate_contract_registry__mutmut_46 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_47'] = x_validate_contract_registry__mutmut_47 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_48'] = x_validate_contract_registry__mutmut_48 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_49'] = x_validate_contract_registry__mutmut_49 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_50'] = x_validate_contract_registry__mutmut_50 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_51'] = x_validate_contract_registry__mutmut_51 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_52'] = x_validate_contract_registry__mutmut_52 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_53'] = x_validate_contract_registry__mutmut_53 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_54'] = x_validate_contract_registry__mutmut_54 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_55'] = x_validate_contract_registry__mutmut_55 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_56'] = x_validate_contract_registry__mutmut_56 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_57'] = x_validate_contract_registry__mutmut_57 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_58'] = x_validate_contract_registry__mutmut_58 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_59'] = x_validate_contract_registry__mutmut_59 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_60'] = x_validate_contract_registry__mutmut_60 # type: ignore # mutmut generated
mutants_x_validate_contract_registry__mutmut['x_validate_contract_registry__mutmut_61'] = x_validate_contract_registry__mutmut_61 # type: ignore # mutmut generated


__all__ = [
    "CaseEnvironment",
    "GitCaseEnvironment",
    "GitFixtureEnvironment",
    "CheckContract",
    "CheckContractError",
    "ContractCase",
    "FindingExpectation",
    "OutcomeExpectation",
    "load_check_contract",
    "registered_contract_directory",
    "validate_contract_registry",
]
