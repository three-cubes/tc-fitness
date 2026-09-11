"""Subprocess-level tests for the tc-fitness-runtime-contract executable."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

from tc_fitness.core_checks._runtime_contracts import CONTRACT_SCHEMA, EVIDENCE_SCHEMA, canonical_json_bytes


def _registry() -> dict[str, object]:
    return {
        "schema": CONTRACT_SCHEMA,
        "environments": {
            "prod": {
                "targets": {
                    "hermes": {
                        "filesystem": {},
                        "access": {},
                        "deployment": {},
                        "evidence": {},
                    }
                }
            }
        },
    }


def _run(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, "-m", "tc_fitness.runtime_contract", *args],
        check=False,
        capture_output=True,
    )


def test_resolve_and_digest_write_canonical_results(tmp_path: Path) -> None:
    registry = tmp_path / "registry.json"
    registry.write_bytes(canonical_json_bytes(_registry()))
    resolved = tmp_path / "resolved.json"
    digest_result = tmp_path / "digest.json"

    result = _run(
        "resolve",
        "--contract",
        str(registry),
        "--environment",
        "prod",
        "--target",
        "hermes",
        "--output",
        str(resolved),
    )
    assert result.returncode == 0, result.stderr.decode()
    assert resolved.read_bytes() == canonical_json_bytes(json.loads(resolved.read_bytes()))

    result = _run(
        "digest",
        "--contract",
        str(registry),
        "--environment",
        "prod",
        "--target",
        "hermes",
        "--output",
        str(digest_result),
    )
    assert result.returncode == 0, result.stderr.decode()
    assert json.loads(digest_result.read_bytes()) == {
        "contract_digest": "sha256:" + hashlib.sha256(resolved.read_bytes()).hexdigest()
    }


def test_verify_evidence_accepts_independent_identity_values(tmp_path: Path) -> None:
    registry = tmp_path / "registry.json"
    registry.write_bytes(canonical_json_bytes(_registry()))
    resolved = tmp_path / "resolved.json"
    assert (
        _run(
            "resolve",
            "--contract",
            str(registry),
            "--environment",
            "prod",
            "--target",
            "hermes",
            "--output",
            str(resolved),
        ).returncode
        == 0
    )
    source_sha = "a" * 40
    image_digest = "sha256:" + "b" * 64
    evidence = {
        "schema": EVIDENCE_SCHEMA,
        "contract_digest": "sha256:" + hashlib.sha256(resolved.read_bytes()).hexdigest(),
        "source_sha": source_sha,
        "image_digest": image_digest,
        "host_id": "vm-1",
        "runtime_user": "openclaw",
        "deployment_id": "deploy-20260911-001",
        "configuration_identity": "sha256:" + "c" * 64,
        "run_id": 1,
        "attempt_id": 1,
        "captured_at": datetime.now(UTC).isoformat(),
        "checks": [
            {
                "id": "runtime-probe",
                "status": "passed",
                "observation": {"kind": "process", "state": "healthy"},
            }
        ],
        "artifacts": [],
    }
    evidence_path = tmp_path / "evidence.json"
    evidence_path.write_bytes(canonical_json_bytes(evidence))
    output = tmp_path / "verification.json"

    result = _run(
        "verify-evidence",
        "--contract",
        str(registry),
        "--environment",
        "prod",
        "--target",
        "hermes",
        "--evidence",
        str(evidence_path),
        "--expected-source-sha",
        source_sha,
        "--expected-image-digest",
        image_digest,
        "--expected-host-id",
        "vm-1",
        "--expected-runtime-user",
        "openclaw",
        "--expected-deployment-id",
        "deploy-20260911-001",
        "--expected-configuration-identity",
        "sha256:" + "c" * 64,
        "--expected-run-id",
        "1",
        "--expected-attempt-id",
        "1",
        "--required-check",
        "runtime-probe",
        "--max-age-seconds",
        "300",
        "--output",
        str(output),
    )
    assert result.returncode == 0, result.stderr.decode()
    assert json.loads(output.read_bytes()) == {"findings": [], "valid": True}


def test_cli_returns_one_and_writes_findings_for_bad_input(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text('{"schema":"wrong"}', encoding="utf-8")
    output = tmp_path / "result.json"
    result = _run(
        "resolve",
        "--contract",
        str(bad),
        "--environment",
        "prod",
        "--target",
        "hermes",
        "--output",
        str(output),
    )
    assert result.returncode == 1
    payload = json.loads(output.read_bytes())
    assert payload["valid"] is False
    assert payload["findings"][0]["fix"]
    assert payload["findings"][0]["next"]
    assert payload["findings"][0]["run"]


def test_recursive_yaml_writes_canonical_invalid_result(tmp_path: Path) -> None:
    contract = tmp_path / "contract.yaml"
    contract.write_text(
        "schema: tc-fitness/runtime-contract/v1\n"
        "environment: prod\ntarget: hermes\nevidence: &loop [*loop]\n",
        encoding="utf-8",
    )
    output = tmp_path / "result.json"
    result = _run(
        "resolve",
        "--contract",
        str(contract),
        "--environment",
        "prod",
        "--target",
        "hermes",
        "--output",
        str(output),
    )
    assert result.returncode == 1
    assert output.exists(), result.stderr.decode()
    payload = json.loads(output.read_bytes())
    assert payload["valid"] is False
    assert payload["findings"][0]["code"] == "cyclic-document"


def test_depth_invalid_yaml_writes_canonical_invalid_result(tmp_path: Path) -> None:
    contract = tmp_path / "contract.yaml"
    nested = ""
    for depth in range(110):
        nested += f"{'  ' * depth}level-{depth}:\n"
    nested += f"{'  ' * 110}value: end\n"
    contract.write_text("schema: tc-fitness/runtime-contract/v1\n" + nested, encoding="utf-8")
    output = tmp_path / "result.json"
    result = _run(
        "resolve",
        "--contract",
        str(contract),
        "--environment",
        "prod",
        "--target",
        "hermes",
        "--output",
        str(output),
    )
    assert result.returncode == 1
    payload = json.loads(output.read_bytes())
    assert payload["valid"] is False
    assert payload["findings"][0]["code"] == "document-too-deep"


@pytest.mark.parametrize("key", ["1", "true", "null"])
def test_yaml_non_string_mapping_key_is_rejected_by_cli(tmp_path: Path, key: str) -> None:
    contract = tmp_path / "contract.yaml"
    contract.write_text(
        "schema: tc-fitness/runtime-contract/v1\n"
        "environment: prod\ntarget: hermes\nfilesystem:\n  roots:\n"
        f"    {key}: /state\n",
        encoding="utf-8",
    )
    output = tmp_path / "result.json"
    result = _run(
        "resolve",
        "--contract",
        str(contract),
        "--environment",
        "prod",
        "--target",
        "hermes",
        "--output",
        str(output),
    )
    assert result.returncode == 1
    payload = json.loads(output.read_bytes())
    assert payload["valid"] is False
    assert payload["findings"][0]["code"] == "non-string-key"


def test_verify_cli_rejects_missing_receipt_execution_identity(tmp_path: Path) -> None:
    registry = tmp_path / "registry.json"
    registry.write_bytes(canonical_json_bytes(_registry()))
    resolved = tmp_path / "resolved.json"
    assert (
        _run(
            "resolve",
            "--contract",
            str(registry),
            "--environment",
            "prod",
            "--target",
            "hermes",
            "--output",
            str(resolved),
        ).returncode
        == 0
    )
    source_sha = "a" * 40
    image_digest = "sha256:" + "b" * 64
    evidence = {
        "schema": EVIDENCE_SCHEMA,
        "contract_digest": "sha256:" + hashlib.sha256(resolved.read_bytes()).hexdigest(),
        "source_sha": source_sha,
        "image_digest": image_digest,
        "host_id": "vm-1",
        "runtime_user": "openclaw",
        "captured_at": datetime.now(UTC).isoformat(),
        "checks": [],
        "artifacts": [],
    }
    evidence_path = tmp_path / "evidence.json"
    evidence_path.write_bytes(canonical_json_bytes(evidence))
    output = tmp_path / "verification.json"
    result = _run(
        "verify-evidence",
        "--contract",
        str(registry),
        "--environment",
        "prod",
        "--target",
        "hermes",
        "--evidence",
        str(evidence_path),
        "--expected-source-sha",
        source_sha,
        "--expected-image-digest",
        image_digest,
        "--expected-host-id",
        "vm-1",
        "--expected-runtime-user",
        "openclaw",
        "--expected-deployment-id",
        "deploy-20260911-001",
        "--expected-configuration-identity",
        "sha256:" + "c" * 64,
        "--expected-run-id",
        "1",
        "--expected-attempt-id",
        "1",
        "--max-age-seconds",
        "300",
        "--output",
        str(output),
    )
    assert result.returncode == 1
    assert any(
        finding["code"] == "missing-receipt-identity"
        for finding in json.loads(output.read_bytes())["findings"]
    )


def test_verify_cli_rejects_receipt_from_an_earlier_attempt(tmp_path: Path) -> None:
    registry = tmp_path / "registry.json"
    registry.write_bytes(canonical_json_bytes(_registry()))
    resolved = tmp_path / "resolved.json"
    assert (
        _run(
            "resolve",
            "--contract",
            str(registry),
            "--environment",
            "prod",
            "--target",
            "hermes",
            "--output",
            str(resolved),
        ).returncode
        == 0
    )
    evidence = {
        "schema": EVIDENCE_SCHEMA,
        "contract_digest": "sha256:" + hashlib.sha256(resolved.read_bytes()).hexdigest(),
        "source_sha": "a" * 40,
        "image_digest": "sha256:" + "b" * 64,
        "host_id": "vm-1",
        "runtime_user": "openclaw",
        "deployment_id": "deploy-current",
        "configuration_identity": "sha256:" + "c" * 64,
        "run_id": 10,
        "attempt_id": 1,
        "captured_at": datetime.now(UTC).isoformat(),
        "checks": [],
        "artifacts": [],
    }
    evidence_path = tmp_path / "evidence.json"
    evidence_path.write_bytes(canonical_json_bytes(evidence))
    output = tmp_path / "verification.json"

    result = _run(
        "verify-evidence",
        "--contract",
        str(registry),
        "--environment",
        "prod",
        "--target",
        "hermes",
        "--evidence",
        str(evidence_path),
        "--expected-source-sha",
        "a" * 40,
        "--expected-image-digest",
        "sha256:" + "b" * 64,
        "--expected-host-id",
        "vm-1",
        "--expected-runtime-user",
        "openclaw",
        "--expected-deployment-id",
        "deploy-current",
        "--expected-configuration-identity",
        "sha256:" + "c" * 64,
        "--expected-run-id",
        "10",
        "--expected-attempt-id",
        "2",
        "--max-age-seconds",
        "300",
        "--output",
        str(output),
    )

    assert result.returncode == 1
    assert {finding["code"] for finding in json.loads(output.read_bytes())["findings"]} == {
        "attempt-id-mismatch"
    }
