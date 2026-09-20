"""Command boundary for resolving, hashing and verifying runtime contracts."""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from tc_fitness.core_checks._runtime_contracts import (
    CONTRACT_SCHEMA,
    EVIDENCE_SCHEMA,
    ContractDocuments,
    ContractFinding,
    canonical_json_bytes,
    finding_payload,
    load_runtime_document,
    resolve_contract,
    sort_findings,
)
from tc_fitness.core_checks.runtime_evidence_contract import validate_runtime_evidence


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__write__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__write__mutmut)
def _write(path: Path, value: object) -> None:
    path.write_bytes(canonical_json_bytes(value))


def x__write__mutmut_orig(path: Path, value: object) -> None:
    path.write_bytes(canonical_json_bytes(value))


def x__write__mutmut_1(path: Path, value: object) -> None:
    path.write_bytes(None)


def x__write__mutmut_2(path: Path, value: object) -> None:
    path.write_bytes(canonical_json_bytes(None))

mutants_x__write__mutmut['_mutmut_orig'] = x__write__mutmut_orig # type: ignore # mutmut generated
mutants_x__write__mutmut['x__write__mutmut_1'] = x__write__mutmut_1 # type: ignore # mutmut generated
mutants_x__write__mutmut['x__write__mutmut_2'] = x__write__mutmut_2 # type: ignore # mutmut generated
mutants_x__invalid__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__invalid__mutmut)
def _invalid(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "findings": [finding_payload(finding) for finding in sort_findings(findings)],
            "valid": False,
        },
    )
    return 1


def x__invalid__mutmut_orig(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "findings": [finding_payload(finding) for finding in sort_findings(findings)],
            "valid": False,
        },
    )
    return 1


def x__invalid__mutmut_1(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        None,
        {
            "findings": [finding_payload(finding) for finding in sort_findings(findings)],
            "valid": False,
        },
    )
    return 1


def x__invalid__mutmut_2(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        None,
    )
    return 1


def x__invalid__mutmut_3(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        {
            "findings": [finding_payload(finding) for finding in sort_findings(findings)],
            "valid": False,
        },
    )
    return 1


def x__invalid__mutmut_4(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        )
    return 1


def x__invalid__mutmut_5(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "XXfindingsXX": [finding_payload(finding) for finding in sort_findings(findings)],
            "valid": False,
        },
    )
    return 1


def x__invalid__mutmut_6(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "FINDINGS": [finding_payload(finding) for finding in sort_findings(findings)],
            "valid": False,
        },
    )
    return 1


def x__invalid__mutmut_7(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "findings": [finding_payload(None) for finding in sort_findings(findings)],
            "valid": False,
        },
    )
    return 1


def x__invalid__mutmut_8(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "findings": [finding_payload(finding) for finding in sort_findings(None)],
            "valid": False,
        },
    )
    return 1


def x__invalid__mutmut_9(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "findings": [finding_payload(finding) for finding in sort_findings(findings)],
            "XXvalidXX": False,
        },
    )
    return 1


def x__invalid__mutmut_10(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "findings": [finding_payload(finding) for finding in sort_findings(findings)],
            "VALID": False,
        },
    )
    return 1


def x__invalid__mutmut_11(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "findings": [finding_payload(finding) for finding in sort_findings(findings)],
            "valid": True,
        },
    )
    return 1


def x__invalid__mutmut_12(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "findings": [finding_payload(finding) for finding in sort_findings(findings)],
            "valid": False,
        },
    )
    return 2

mutants_x__invalid__mutmut['_mutmut_orig'] = x__invalid__mutmut_orig # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_1'] = x__invalid__mutmut_1 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_2'] = x__invalid__mutmut_2 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_3'] = x__invalid__mutmut_3 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_4'] = x__invalid__mutmut_4 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_5'] = x__invalid__mutmut_5 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_6'] = x__invalid__mutmut_6 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_7'] = x__invalid__mutmut_7 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_8'] = x__invalid__mutmut_8 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_9'] = x__invalid__mutmut_9 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_10'] = x__invalid__mutmut_10 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_11'] = x__invalid__mutmut_11 # type: ignore # mutmut generated
mutants_x__invalid__mutmut['x__invalid__mutmut_12'] = x__invalid__mutmut_12 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__selected_contract__mutmut)
def _selected_contract(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_orig(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_1(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = None
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_2(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(None, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_3(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=None)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_4(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_5(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, )
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_6(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None and raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_7(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings and registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_8(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is not None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_9(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is not None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_10(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = None
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_11(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        None,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_12(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=None,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_13(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=None,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_14(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=None,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_15(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_16(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_17(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_18(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_19(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings and contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_20(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is not None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_21(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=None,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_22(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=None,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_23(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=None,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_24(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_25(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_26(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        evidence_path=None,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_27(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_28(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence_bytes=None,
    ), ()


def x__selected_contract__mutmut_29(
    contract_path: Path,
    *,
    environment: str,
    target: str,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    registry, findings, raw = load_runtime_document(contract_path, expected_schema=CONTRACT_SCHEMA)
    if findings or registry is None or raw is None:
        return None, findings
    contract, findings = resolve_contract(
        registry,
        environment=environment,
        target=target,
        source=contract_path,
    )
    if findings or contract is None:
        return None, findings
    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=raw,
        evidence_path=None,
        evidence=None,
        ), ()

mutants_x__selected_contract__mutmut['_mutmut_orig'] = x__selected_contract__mutmut_orig # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_1'] = x__selected_contract__mutmut_1 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_2'] = x__selected_contract__mutmut_2 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_3'] = x__selected_contract__mutmut_3 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_4'] = x__selected_contract__mutmut_4 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_5'] = x__selected_contract__mutmut_5 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_6'] = x__selected_contract__mutmut_6 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_7'] = x__selected_contract__mutmut_7 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_8'] = x__selected_contract__mutmut_8 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_9'] = x__selected_contract__mutmut_9 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_10'] = x__selected_contract__mutmut_10 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_11'] = x__selected_contract__mutmut_11 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_12'] = x__selected_contract__mutmut_12 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_13'] = x__selected_contract__mutmut_13 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_14'] = x__selected_contract__mutmut_14 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_15'] = x__selected_contract__mutmut_15 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_16'] = x__selected_contract__mutmut_16 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_17'] = x__selected_contract__mutmut_17 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_18'] = x__selected_contract__mutmut_18 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_19'] = x__selected_contract__mutmut_19 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_20'] = x__selected_contract__mutmut_20 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_21'] = x__selected_contract__mutmut_21 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_22'] = x__selected_contract__mutmut_22 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_23'] = x__selected_contract__mutmut_23 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_24'] = x__selected_contract__mutmut_24 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_25'] = x__selected_contract__mutmut_25 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_26'] = x__selected_contract__mutmut_26 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_27'] = x__selected_contract__mutmut_27 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_28'] = x__selected_contract__mutmut_28 # type: ignore # mutmut generated
mutants_x__selected_contract__mutmut['x__selected_contract__mutmut_29'] = x__selected_contract__mutmut_29 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__run_resolve__mutmut)
def _run_resolve(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_orig(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_1(args: argparse.Namespace) -> int:
    documents, findings = None
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_2(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        None,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_3(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=None,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_4(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=None,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_5(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_6(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_7(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_8(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings and documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_9(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is not None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_10(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(None, findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_11(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, None)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_12(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(findings)
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_13(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, )
    _write(args.output, documents.contract)
    return 0


def x__run_resolve__mutmut_14(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(None, documents.contract)
    return 0


def x__run_resolve__mutmut_15(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, None)
    return 0


def x__run_resolve__mutmut_16(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(documents.contract)
    return 0


def x__run_resolve__mutmut_17(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, )
    return 0


def x__run_resolve__mutmut_18(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    _write(args.output, documents.contract)
    return 1

mutants_x__run_resolve__mutmut['_mutmut_orig'] = x__run_resolve__mutmut_orig # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_1'] = x__run_resolve__mutmut_1 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_2'] = x__run_resolve__mutmut_2 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_3'] = x__run_resolve__mutmut_3 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_4'] = x__run_resolve__mutmut_4 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_5'] = x__run_resolve__mutmut_5 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_6'] = x__run_resolve__mutmut_6 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_7'] = x__run_resolve__mutmut_7 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_8'] = x__run_resolve__mutmut_8 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_9'] = x__run_resolve__mutmut_9 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_10'] = x__run_resolve__mutmut_10 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_11'] = x__run_resolve__mutmut_11 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_12'] = x__run_resolve__mutmut_12 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_13'] = x__run_resolve__mutmut_13 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_14'] = x__run_resolve__mutmut_14 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_15'] = x__run_resolve__mutmut_15 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_16'] = x__run_resolve__mutmut_16 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_17'] = x__run_resolve__mutmut_17 # type: ignore # mutmut generated
mutants_x__run_resolve__mutmut['x__run_resolve__mutmut_18'] = x__run_resolve__mutmut_18 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__run_digest__mutmut)
def _run_digest(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_orig(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_1(args: argparse.Namespace) -> int:
    documents, findings = None
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_2(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        None,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_3(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=None,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_4(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=None,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_5(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_6(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_7(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_8(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings and documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_9(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is not None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_10(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(None, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_11(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, None)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_12(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_13(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, )
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_14(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = None
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_15(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" - hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_16(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "XXsha256:XX" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_17(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "SHA256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_18(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(None).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_19(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(None)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_20(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(None, {"contract_digest": digest})
    return 0


def x__run_digest__mutmut_21(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, None)
    return 0


def x__run_digest__mutmut_22(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write({"contract_digest": digest})
    return 0


def x__run_digest__mutmut_23(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, )
    return 0


def x__run_digest__mutmut_24(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"XXcontract_digestXX": digest})
    return 0


def x__run_digest__mutmut_25(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"CONTRACT_DIGEST": digest})
    return 0


def x__run_digest__mutmut_26(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    digest = "sha256:" + hashlib.sha256(canonical_json_bytes(documents.contract)).hexdigest()
    _write(args.output, {"contract_digest": digest})
    return 1

mutants_x__run_digest__mutmut['_mutmut_orig'] = x__run_digest__mutmut_orig # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_1'] = x__run_digest__mutmut_1 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_2'] = x__run_digest__mutmut_2 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_3'] = x__run_digest__mutmut_3 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_4'] = x__run_digest__mutmut_4 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_5'] = x__run_digest__mutmut_5 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_6'] = x__run_digest__mutmut_6 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_7'] = x__run_digest__mutmut_7 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_8'] = x__run_digest__mutmut_8 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_9'] = x__run_digest__mutmut_9 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_10'] = x__run_digest__mutmut_10 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_11'] = x__run_digest__mutmut_11 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_12'] = x__run_digest__mutmut_12 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_13'] = x__run_digest__mutmut_13 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_14'] = x__run_digest__mutmut_14 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_15'] = x__run_digest__mutmut_15 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_16'] = x__run_digest__mutmut_16 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_17'] = x__run_digest__mutmut_17 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_18'] = x__run_digest__mutmut_18 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_19'] = x__run_digest__mutmut_19 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_20'] = x__run_digest__mutmut_20 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_21'] = x__run_digest__mutmut_21 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_22'] = x__run_digest__mutmut_22 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_23'] = x__run_digest__mutmut_23 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_24'] = x__run_digest__mutmut_24 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_25'] = x__run_digest__mutmut_25 # type: ignore # mutmut generated
mutants_x__run_digest__mutmut['x__run_digest__mutmut_26'] = x__run_digest__mutmut_26 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__run_verify__mutmut)
def _run_verify(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_orig(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_1(args: argparse.Namespace) -> int:
    documents, findings = None
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_2(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        None,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_3(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=None,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_4(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=None,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_5(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_6(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_7(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_8(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings and documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_9(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is not None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_10(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(None, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_11(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, None)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_12(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_13(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, )
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_14(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = None
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_15(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        None,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_16(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=None,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_17(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_18(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_19(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None and evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_20(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings and evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_21(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is not None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_22(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is not None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_23(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(None, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_24(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, None)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_25(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_26(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, )
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_27(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = None
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_28(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=None,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_29(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=None,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_30(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=None,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_31(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=None,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_32(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=None,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_33(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=None,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_34(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_35(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_36(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_37(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_38(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_39(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_40(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = None
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_41(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        None,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_42(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity=None,
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_43(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=None,
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_44(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=None,
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_45(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=None,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_46(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_47(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_48(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_49(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_50(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_51(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "XXsource_shaXX": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_52(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "SOURCE_SHA": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_53(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "XXimage_digestXX": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_54(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "IMAGE_DIGEST": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_55(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "XXhost_idXX": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_56(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "HOST_ID": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_57(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "XXruntime_userXX": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_58(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "RUNTIME_USER": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_59(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "XXdeployment_idXX": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_60(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "DEPLOYMENT_ID": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_61(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "XXconfiguration_identityXX": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_62(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "CONFIGURATION_IDENTITY": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_63(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "XXrun_idXX": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_64(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "RUN_ID": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_65(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "XXattempt_idXX": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_66(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "ATTEMPT_ID": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_67(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(None),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_68(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(None),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_69(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(None, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_70(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, None)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_71(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(findings)
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_72(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, )
    _write(args.output, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_73(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(None, {"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_74(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, None)
    return 0


def x__run_verify__mutmut_75(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write({"findings": [], "valid": True})
    return 0


def x__run_verify__mutmut_76(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, )
    return 0


def x__run_verify__mutmut_77(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"XXfindingsXX": [], "valid": True})
    return 0


def x__run_verify__mutmut_78(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"FINDINGS": [], "valid": True})
    return 0


def x__run_verify__mutmut_79(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "XXvalidXX": True})
    return 0


def x__run_verify__mutmut_80(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "VALID": True})
    return 0


def x__run_verify__mutmut_81(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": False})
    return 0


def x__run_verify__mutmut_82(args: argparse.Namespace) -> int:
    documents, findings = _selected_contract(
        args.contract,
        environment=args.environment,
        target=args.target,
    )
    if findings or documents is None:
        return _invalid(args.output, findings)
    evidence, findings, evidence_bytes = load_runtime_document(
        args.evidence,
        expected_schema=EVIDENCE_SCHEMA,
    )
    if findings or evidence is None or evidence_bytes is None:
        return _invalid(args.output, findings)
    documents = ContractDocuments(
        contract_path=documents.contract_path,
        contract=documents.contract,
        contract_bytes=documents.contract_bytes,
        evidence_path=args.evidence,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    )
    findings = validate_runtime_evidence(
        documents,
        expected_identity={
            "source_sha": args.expected_source_sha,
            "image_digest": args.expected_image_digest,
            "host_id": args.expected_host_id,
            "runtime_user": args.expected_runtime_user,
            "deployment_id": args.expected_deployment_id,
            "configuration_identity": args.expected_configuration_identity,
            "run_id": args.expected_run_id,
            "attempt_id": args.expected_attempt_id,
        },
        required_checks=tuple(args.required_check),
        now=datetime.now(UTC),
        max_age_seconds=args.max_age_seconds,
    )
    if findings:
        return _invalid(args.output, findings)
    _write(args.output, {"findings": [], "valid": True})
    return 1

mutants_x__run_verify__mutmut['_mutmut_orig'] = x__run_verify__mutmut_orig # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_1'] = x__run_verify__mutmut_1 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_2'] = x__run_verify__mutmut_2 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_3'] = x__run_verify__mutmut_3 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_4'] = x__run_verify__mutmut_4 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_5'] = x__run_verify__mutmut_5 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_6'] = x__run_verify__mutmut_6 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_7'] = x__run_verify__mutmut_7 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_8'] = x__run_verify__mutmut_8 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_9'] = x__run_verify__mutmut_9 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_10'] = x__run_verify__mutmut_10 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_11'] = x__run_verify__mutmut_11 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_12'] = x__run_verify__mutmut_12 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_13'] = x__run_verify__mutmut_13 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_14'] = x__run_verify__mutmut_14 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_15'] = x__run_verify__mutmut_15 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_16'] = x__run_verify__mutmut_16 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_17'] = x__run_verify__mutmut_17 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_18'] = x__run_verify__mutmut_18 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_19'] = x__run_verify__mutmut_19 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_20'] = x__run_verify__mutmut_20 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_21'] = x__run_verify__mutmut_21 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_22'] = x__run_verify__mutmut_22 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_23'] = x__run_verify__mutmut_23 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_24'] = x__run_verify__mutmut_24 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_25'] = x__run_verify__mutmut_25 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_26'] = x__run_verify__mutmut_26 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_27'] = x__run_verify__mutmut_27 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_28'] = x__run_verify__mutmut_28 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_29'] = x__run_verify__mutmut_29 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_30'] = x__run_verify__mutmut_30 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_31'] = x__run_verify__mutmut_31 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_32'] = x__run_verify__mutmut_32 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_33'] = x__run_verify__mutmut_33 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_34'] = x__run_verify__mutmut_34 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_35'] = x__run_verify__mutmut_35 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_36'] = x__run_verify__mutmut_36 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_37'] = x__run_verify__mutmut_37 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_38'] = x__run_verify__mutmut_38 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_39'] = x__run_verify__mutmut_39 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_40'] = x__run_verify__mutmut_40 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_41'] = x__run_verify__mutmut_41 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_42'] = x__run_verify__mutmut_42 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_43'] = x__run_verify__mutmut_43 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_44'] = x__run_verify__mutmut_44 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_45'] = x__run_verify__mutmut_45 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_46'] = x__run_verify__mutmut_46 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_47'] = x__run_verify__mutmut_47 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_48'] = x__run_verify__mutmut_48 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_49'] = x__run_verify__mutmut_49 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_50'] = x__run_verify__mutmut_50 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_51'] = x__run_verify__mutmut_51 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_52'] = x__run_verify__mutmut_52 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_53'] = x__run_verify__mutmut_53 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_54'] = x__run_verify__mutmut_54 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_55'] = x__run_verify__mutmut_55 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_56'] = x__run_verify__mutmut_56 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_57'] = x__run_verify__mutmut_57 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_58'] = x__run_verify__mutmut_58 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_59'] = x__run_verify__mutmut_59 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_60'] = x__run_verify__mutmut_60 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_61'] = x__run_verify__mutmut_61 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_62'] = x__run_verify__mutmut_62 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_63'] = x__run_verify__mutmut_63 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_64'] = x__run_verify__mutmut_64 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_65'] = x__run_verify__mutmut_65 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_66'] = x__run_verify__mutmut_66 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_67'] = x__run_verify__mutmut_67 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_68'] = x__run_verify__mutmut_68 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_69'] = x__run_verify__mutmut_69 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_70'] = x__run_verify__mutmut_70 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_71'] = x__run_verify__mutmut_71 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_72'] = x__run_verify__mutmut_72 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_73'] = x__run_verify__mutmut_73 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_74'] = x__run_verify__mutmut_74 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_75'] = x__run_verify__mutmut_75 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_76'] = x__run_verify__mutmut_76 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_77'] = x__run_verify__mutmut_77 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_78'] = x__run_verify__mutmut_78 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_79'] = x__run_verify__mutmut_79 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_80'] = x__run_verify__mutmut_80 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_81'] = x__run_verify__mutmut_81 # type: ignore # mutmut generated
mutants_x__run_verify__mutmut['x__run_verify__mutmut_82'] = x__run_verify__mutmut_82 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__add_selection_arguments__mutmut)
def _add_selection_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_orig(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_1(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(None, type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_2(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=None, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_3(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=None, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_4(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help=None)
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_5(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_6(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_7(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_8(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, )
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_9(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("XX--contractXX", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_10(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--CONTRACT", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_11(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=False, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_12(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="XXruntime contract registry pathXX")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_13(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="RUNTIME CONTRACT REGISTRY PATH")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_14(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument(None, required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_15(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=None, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_16(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help=None)
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_17(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument(required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_18(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_19(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, )
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_20(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("XX--environmentXX", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_21(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--ENVIRONMENT", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_22(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=False, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_23(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="XXenvironment key to resolveXX")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_24(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="ENVIRONMENT KEY TO RESOLVE")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_25(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument(None, required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_26(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=None, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_27(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help=None)
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_28(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument(required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_29(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_30(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, )
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_31(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("XX--targetXX", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_32(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--TARGET", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_33(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=False, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_34(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="XXtarget key to resolveXX")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_35(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="TARGET KEY TO RESOLVE")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_36(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument(None, type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_37(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=None, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_38(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=None, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_39(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help=None)


def x__add_selection_arguments__mutmut_40(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument(type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_41(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_42(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_43(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, )


def x__add_selection_arguments__mutmut_44(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("XX--outputXX", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_45(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--OUTPUT", type=Path, required=True, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_46(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=False, help="canonical JSON output path")


def x__add_selection_arguments__mutmut_47(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="XXcanonical JSON output pathXX")


def x__add_selection_arguments__mutmut_48(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical json output path")


def x__add_selection_arguments__mutmut_49(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="CANONICAL JSON OUTPUT PATH")

mutants_x__add_selection_arguments__mutmut['_mutmut_orig'] = x__add_selection_arguments__mutmut_orig # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_1'] = x__add_selection_arguments__mutmut_1 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_2'] = x__add_selection_arguments__mutmut_2 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_3'] = x__add_selection_arguments__mutmut_3 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_4'] = x__add_selection_arguments__mutmut_4 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_5'] = x__add_selection_arguments__mutmut_5 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_6'] = x__add_selection_arguments__mutmut_6 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_7'] = x__add_selection_arguments__mutmut_7 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_8'] = x__add_selection_arguments__mutmut_8 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_9'] = x__add_selection_arguments__mutmut_9 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_10'] = x__add_selection_arguments__mutmut_10 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_11'] = x__add_selection_arguments__mutmut_11 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_12'] = x__add_selection_arguments__mutmut_12 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_13'] = x__add_selection_arguments__mutmut_13 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_14'] = x__add_selection_arguments__mutmut_14 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_15'] = x__add_selection_arguments__mutmut_15 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_16'] = x__add_selection_arguments__mutmut_16 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_17'] = x__add_selection_arguments__mutmut_17 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_18'] = x__add_selection_arguments__mutmut_18 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_19'] = x__add_selection_arguments__mutmut_19 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_20'] = x__add_selection_arguments__mutmut_20 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_21'] = x__add_selection_arguments__mutmut_21 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_22'] = x__add_selection_arguments__mutmut_22 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_23'] = x__add_selection_arguments__mutmut_23 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_24'] = x__add_selection_arguments__mutmut_24 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_25'] = x__add_selection_arguments__mutmut_25 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_26'] = x__add_selection_arguments__mutmut_26 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_27'] = x__add_selection_arguments__mutmut_27 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_28'] = x__add_selection_arguments__mutmut_28 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_29'] = x__add_selection_arguments__mutmut_29 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_30'] = x__add_selection_arguments__mutmut_30 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_31'] = x__add_selection_arguments__mutmut_31 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_32'] = x__add_selection_arguments__mutmut_32 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_33'] = x__add_selection_arguments__mutmut_33 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_34'] = x__add_selection_arguments__mutmut_34 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_35'] = x__add_selection_arguments__mutmut_35 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_36'] = x__add_selection_arguments__mutmut_36 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_37'] = x__add_selection_arguments__mutmut_37 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_38'] = x__add_selection_arguments__mutmut_38 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_39'] = x__add_selection_arguments__mutmut_39 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_40'] = x__add_selection_arguments__mutmut_40 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_41'] = x__add_selection_arguments__mutmut_41 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_42'] = x__add_selection_arguments__mutmut_42 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_43'] = x__add_selection_arguments__mutmut_43 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_44'] = x__add_selection_arguments__mutmut_44 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_45'] = x__add_selection_arguments__mutmut_45 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_46'] = x__add_selection_arguments__mutmut_46 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_47'] = x__add_selection_arguments__mutmut_47 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_48'] = x__add_selection_arguments__mutmut_48 # type: ignore # mutmut generated
mutants_x__add_selection_arguments__mutmut['x__add_selection_arguments__mutmut_49'] = x__add_selection_arguments__mutmut_49 # type: ignore # mutmut generated
mutants_x__parser__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__parser__mutmut)
def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_orig() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_1() -> argparse.ArgumentParser:
    parser = None
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_2() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=None)
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_3() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="XXtc-fitness-runtime-contractXX")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_4() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="TC-FITNESS-RUNTIME-CONTRACT")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_5() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = None

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_6() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest=None, required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_7() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=None)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_8() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_9() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", )

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_10() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="XXcommandXX", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_11() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="COMMAND", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_12() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=False)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_13() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = None
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_14() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser(None, help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_15() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help=None)
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_16() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser(help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_17() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", )
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_18() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("XXresolveXX", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_19() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("RESOLVE", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_20() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="XXresolve one target to canonical JSONXX")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_21() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical json")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_22() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="RESOLVE ONE TARGET TO CANONICAL JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_23() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(None)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_24() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=None)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_25() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = None
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_26() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser(None, help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_27() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help=None)
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_28() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser(help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_29() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", )
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_30() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("XXdigestXX", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_31() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("DIGEST", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_32() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="XXhash one selected canonical contractXX")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_33() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="HASH ONE SELECTED CANONICAL CONTRACT")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_34() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(None)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_35() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=None)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_36() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = None
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_37() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser(None, help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_38() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help=None)
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_39() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser(help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_40() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", )
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_41() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("XXverify-evidenceXX", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_42() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("VERIFY-EVIDENCE", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_43() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="XXverify a digest-bound runtime receiptXX")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_44() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="VERIFY A DIGEST-BOUND RUNTIME RECEIPT")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_45() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(None)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_46() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument(None, type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_47() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=None, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_48() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=None, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_49() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help=None)
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_50() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument(type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_51() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_52() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_53() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, )
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_54() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("XX--evidenceXX", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_55() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--EVIDENCE", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_56() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=False, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_57() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="XXruntime evidence JSON pathXX")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_58() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence json path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_59() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="RUNTIME EVIDENCE JSON PATH")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_60() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument(None, required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_61() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=None)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_62() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument(required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_63() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", )
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_64() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("XX--expected-source-shaXX", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_65() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--EXPECTED-SOURCE-SHA", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_66() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=False)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_67() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument(None, required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_68() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=None)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_69() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument(required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_70() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", )
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_71() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("XX--expected-image-digestXX", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_72() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--EXPECTED-IMAGE-DIGEST", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_73() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=False)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_74() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument(None, required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_75() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=None)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_76() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument(required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_77() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", )
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_78() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("XX--expected-host-idXX", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_79() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--EXPECTED-HOST-ID", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_80() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=False)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_81() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument(None, required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_82() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=None)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_83() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument(required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_84() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", )
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_85() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("XX--expected-runtime-userXX", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_86() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--EXPECTED-RUNTIME-USER", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_87() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=False)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_88() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument(None, required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_89() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=None)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_90() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument(required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_91() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", )
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_92() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("XX--expected-deployment-idXX", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_93() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--EXPECTED-DEPLOYMENT-ID", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_94() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=False)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_95() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument(None, required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_96() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=None)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_97() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument(required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_98() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", )
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_99() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("XX--expected-configuration-identityXX", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_100() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--EXPECTED-CONFIGURATION-IDENTITY", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_101() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=False)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_102() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument(None, type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_103() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=None, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_104() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=None)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_105() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument(type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_106() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_107() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, )
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_108() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("XX--expected-run-idXX", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_109() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--EXPECTED-RUN-ID", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_110() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=False)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_111() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument(None, type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_112() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=None, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_113() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=None)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_114() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument(type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_115() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_116() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, )
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_117() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("XX--expected-attempt-idXX", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_118() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--EXPECTED-ATTEMPT-ID", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_119() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=False)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_120() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument(None, action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_121() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action=None, default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_122() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=None)
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_123() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument(action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_124() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_125() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", )
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_126() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("XX--required-checkXX", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_127() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--REQUIRED-CHECK", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_128() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="XXappendXX", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_129() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="APPEND", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_130() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument(None, type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_131() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=None, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_132() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=None)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_133() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument(type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_134() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_135() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, )
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_136() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("XX--max-age-secondsXX", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_137() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--MAX-AGE-SECONDS", type=int, required=True)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_138() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=False)
    verify.set_defaults(handler=_run_verify)
    return parser


def x__parser__mutmut_139() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tc-fitness-runtime-contract")
    commands = parser.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve", help="resolve one target to canonical JSON")
    _add_selection_arguments(resolve)
    resolve.set_defaults(handler=_run_resolve)

    digest = commands.add_parser("digest", help="hash one selected canonical contract")
    _add_selection_arguments(digest)
    digest.set_defaults(handler=_run_digest)

    verify = commands.add_parser("verify-evidence", help="verify a digest-bound runtime receipt")
    _add_selection_arguments(verify)
    verify.add_argument("--evidence", type=Path, required=True, help="runtime evidence JSON path")
    verify.add_argument("--expected-source-sha", required=True)
    verify.add_argument("--expected-image-digest", required=True)
    verify.add_argument("--expected-host-id", required=True)
    verify.add_argument("--expected-runtime-user", required=True)
    verify.add_argument("--expected-deployment-id", required=True)
    verify.add_argument("--expected-configuration-identity", required=True)
    verify.add_argument("--expected-run-id", type=int, required=True)
    verify.add_argument("--expected-attempt-id", type=int, required=True)
    verify.add_argument("--required-check", action="append", default=[])
    verify.add_argument("--max-age-seconds", type=int, required=True)
    verify.set_defaults(handler=None)
    return parser

mutants_x__parser__mutmut['_mutmut_orig'] = x__parser__mutmut_orig # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_1'] = x__parser__mutmut_1 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_2'] = x__parser__mutmut_2 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_3'] = x__parser__mutmut_3 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_4'] = x__parser__mutmut_4 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_5'] = x__parser__mutmut_5 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_6'] = x__parser__mutmut_6 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_7'] = x__parser__mutmut_7 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_8'] = x__parser__mutmut_8 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_9'] = x__parser__mutmut_9 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_10'] = x__parser__mutmut_10 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_11'] = x__parser__mutmut_11 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_12'] = x__parser__mutmut_12 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_13'] = x__parser__mutmut_13 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_14'] = x__parser__mutmut_14 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_15'] = x__parser__mutmut_15 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_16'] = x__parser__mutmut_16 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_17'] = x__parser__mutmut_17 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_18'] = x__parser__mutmut_18 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_19'] = x__parser__mutmut_19 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_20'] = x__parser__mutmut_20 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_21'] = x__parser__mutmut_21 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_22'] = x__parser__mutmut_22 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_23'] = x__parser__mutmut_23 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_24'] = x__parser__mutmut_24 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_25'] = x__parser__mutmut_25 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_26'] = x__parser__mutmut_26 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_27'] = x__parser__mutmut_27 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_28'] = x__parser__mutmut_28 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_29'] = x__parser__mutmut_29 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_30'] = x__parser__mutmut_30 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_31'] = x__parser__mutmut_31 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_32'] = x__parser__mutmut_32 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_33'] = x__parser__mutmut_33 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_34'] = x__parser__mutmut_34 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_35'] = x__parser__mutmut_35 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_36'] = x__parser__mutmut_36 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_37'] = x__parser__mutmut_37 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_38'] = x__parser__mutmut_38 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_39'] = x__parser__mutmut_39 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_40'] = x__parser__mutmut_40 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_41'] = x__parser__mutmut_41 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_42'] = x__parser__mutmut_42 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_43'] = x__parser__mutmut_43 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_44'] = x__parser__mutmut_44 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_45'] = x__parser__mutmut_45 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_46'] = x__parser__mutmut_46 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_47'] = x__parser__mutmut_47 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_48'] = x__parser__mutmut_48 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_49'] = x__parser__mutmut_49 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_50'] = x__parser__mutmut_50 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_51'] = x__parser__mutmut_51 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_52'] = x__parser__mutmut_52 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_53'] = x__parser__mutmut_53 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_54'] = x__parser__mutmut_54 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_55'] = x__parser__mutmut_55 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_56'] = x__parser__mutmut_56 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_57'] = x__parser__mutmut_57 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_58'] = x__parser__mutmut_58 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_59'] = x__parser__mutmut_59 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_60'] = x__parser__mutmut_60 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_61'] = x__parser__mutmut_61 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_62'] = x__parser__mutmut_62 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_63'] = x__parser__mutmut_63 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_64'] = x__parser__mutmut_64 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_65'] = x__parser__mutmut_65 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_66'] = x__parser__mutmut_66 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_67'] = x__parser__mutmut_67 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_68'] = x__parser__mutmut_68 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_69'] = x__parser__mutmut_69 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_70'] = x__parser__mutmut_70 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_71'] = x__parser__mutmut_71 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_72'] = x__parser__mutmut_72 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_73'] = x__parser__mutmut_73 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_74'] = x__parser__mutmut_74 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_75'] = x__parser__mutmut_75 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_76'] = x__parser__mutmut_76 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_77'] = x__parser__mutmut_77 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_78'] = x__parser__mutmut_78 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_79'] = x__parser__mutmut_79 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_80'] = x__parser__mutmut_80 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_81'] = x__parser__mutmut_81 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_82'] = x__parser__mutmut_82 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_83'] = x__parser__mutmut_83 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_84'] = x__parser__mutmut_84 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_85'] = x__parser__mutmut_85 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_86'] = x__parser__mutmut_86 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_87'] = x__parser__mutmut_87 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_88'] = x__parser__mutmut_88 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_89'] = x__parser__mutmut_89 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_90'] = x__parser__mutmut_90 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_91'] = x__parser__mutmut_91 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_92'] = x__parser__mutmut_92 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_93'] = x__parser__mutmut_93 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_94'] = x__parser__mutmut_94 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_95'] = x__parser__mutmut_95 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_96'] = x__parser__mutmut_96 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_97'] = x__parser__mutmut_97 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_98'] = x__parser__mutmut_98 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_99'] = x__parser__mutmut_99 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_100'] = x__parser__mutmut_100 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_101'] = x__parser__mutmut_101 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_102'] = x__parser__mutmut_102 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_103'] = x__parser__mutmut_103 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_104'] = x__parser__mutmut_104 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_105'] = x__parser__mutmut_105 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_106'] = x__parser__mutmut_106 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_107'] = x__parser__mutmut_107 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_108'] = x__parser__mutmut_108 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_109'] = x__parser__mutmut_109 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_110'] = x__parser__mutmut_110 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_111'] = x__parser__mutmut_111 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_112'] = x__parser__mutmut_112 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_113'] = x__parser__mutmut_113 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_114'] = x__parser__mutmut_114 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_115'] = x__parser__mutmut_115 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_116'] = x__parser__mutmut_116 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_117'] = x__parser__mutmut_117 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_118'] = x__parser__mutmut_118 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_119'] = x__parser__mutmut_119 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_120'] = x__parser__mutmut_120 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_121'] = x__parser__mutmut_121 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_122'] = x__parser__mutmut_122 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_123'] = x__parser__mutmut_123 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_124'] = x__parser__mutmut_124 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_125'] = x__parser__mutmut_125 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_126'] = x__parser__mutmut_126 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_127'] = x__parser__mutmut_127 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_128'] = x__parser__mutmut_128 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_129'] = x__parser__mutmut_129 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_130'] = x__parser__mutmut_130 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_131'] = x__parser__mutmut_131 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_132'] = x__parser__mutmut_132 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_133'] = x__parser__mutmut_133 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_134'] = x__parser__mutmut_134 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_135'] = x__parser__mutmut_135 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_136'] = x__parser__mutmut_136 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_137'] = x__parser__mutmut_137 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_138'] = x__parser__mutmut_138 # type: ignore # mutmut generated
mutants_x__parser__mutmut['x__parser__mutmut_139'] = x__parser__mutmut_139 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """Run the selected runtime-contract operation."""
    args = _parser().parse_args(argv)
    handler = args.handler
    return int(handler(args))


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """Run the selected runtime-contract operation."""
    args = _parser().parse_args(argv)
    handler = args.handler
    return int(handler(args))


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """Run the selected runtime-contract operation."""
    args = None
    handler = args.handler
    return int(handler(args))


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """Run the selected runtime-contract operation."""
    args = _parser().parse_args(None)
    handler = args.handler
    return int(handler(args))


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """Run the selected runtime-contract operation."""
    args = _parser().parse_args(argv)
    handler = None
    return int(handler(args))


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """Run the selected runtime-contract operation."""
    args = _parser().parse_args(argv)
    handler = args.handler
    return int(None)


def x_main__mutmut_5(argv: list[str] | None = None) -> int:
    """Run the selected runtime-contract operation."""
    args = _parser().parse_args(argv)
    handler = args.handler
    return int(handler(None))

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_5'] = x_main__mutmut_5 # type: ignore # mutmut generated


if __name__ == "__main__":
    sys.exit(main())


__all__ = ["main"]
