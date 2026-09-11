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


def _write(path: Path, value: object) -> None:
    path.write_bytes(canonical_json_bytes(value))


def _invalid(path: Path, findings: Sequence[ContractFinding]) -> int:
    _write(
        path,
        {
            "findings": [finding_payload(finding) for finding in sort_findings(findings)],
            "valid": False,
        },
    )
    return 1


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


def _add_selection_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", type=Path, required=True, help="runtime contract registry path")
    parser.add_argument("--environment", required=True, help="environment key to resolve")
    parser.add_argument("--target", required=True, help="target key to resolve")
    parser.add_argument("--output", type=Path, required=True, help="canonical JSON output path")


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


def main(argv: list[str] | None = None) -> int:
    """Run the selected runtime-contract operation."""
    args = _parser().parse_args(argv)
    handler = args.handler
    return int(handler(args))


if __name__ == "__main__":
    sys.exit(main())


__all__ = ["main"]
