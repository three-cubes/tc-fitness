"""Public behaviour tests for the runtime evidence CORE check."""

from __future__ import annotations

import hashlib
import json
import os
import threading
import tracemalloc
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from tc_fitness.catalogue import RuleEntry
from tc_fitness.check_evidence import capture_check_evidence
from tc_fitness.core_checks import run_core_check
from tc_fitness.core_checks._runtime_contracts import CONTRACT_SCHEMA, EVIDENCE_SCHEMA, canonical_json_bytes
from tc_fitness.core_checks.runtime_evidence_contract import (
    RuntimeEvidenceContract,
    build,
    validate_runtime_evidence,
)
from tc_fitness.runner import run

pytestmark = pytest.mark.integration

_NOW = datetime(2026, 9, 11, 12, 0, tzinfo=UTC)
_SOURCE_SHA = "a" * 40
_IMAGE_DIGEST = "sha256:" + "b" * 64


def _contract() -> dict[str, object]:
    return {
        "schema": CONTRACT_SCHEMA,
        "environment": "prod",
        "target": "hermes",
        "filesystem": {},
        "access": {},
        "deployment": {},
        "evidence": {},
    }


def _evidence(
    contract: dict[str, object],
    artifact: bytes = b"probe details\n",
    *,
    captured_at: datetime,
) -> dict[str, object]:
    return {
        "schema": EVIDENCE_SCHEMA,
        "contract_digest": "sha256:" + hashlib.sha256(canonical_json_bytes(contract)).hexdigest(),
        "source_sha": _SOURCE_SHA,
        "image_digest": _IMAGE_DIGEST,
        "host_id": "vm-hermes-1",
        "runtime_user": "openclaw",
        "deployment_id": "deploy-20260911-001",
        "configuration_identity": "sha256:" + "c" * 64,
        "run_id": 42,
        "attempt_id": 1,
        "captured_at": captured_at.isoformat(),
        "checks": [
            {
                "id": "runtime-probe",
                "status": "passed",
                "observation": {"kind": "process", "state": "healthy"},
            }
        ],
        "artifacts": [
            {
                "path": "artifacts/probe.txt",
                "sha256": "sha256:" + hashlib.sha256(artifact).hexdigest(),
            }
        ],
    }


def _seed(
    tmp_path: Path,
    *,
    mutate: str | None = None,
    captured_at: datetime | None = None,
) -> dict[str, object]:
    contract = _contract()
    artifact = b"probe details\n"
    capture_time = captured_at or datetime.now(UTC)
    evidence = _evidence(contract, artifact, captured_at=capture_time)
    if mutate == "wrong-source":
        evidence["source_sha"] = "c" * 40
    elif mutate == "stale":
        evidence["captured_at"] = (capture_time - timedelta(seconds=301)).isoformat()
    elif mutate == "skipped":
        evidence["checks"] = [{"id": "runtime-probe", "status": "skipped"}]
    elif mutate == "exit-only":
        evidence["checks"] = [{"id": "runtime-probe", "status": "passed", "exit_code": 0}]
    elif mutate == "unsafe-artifact":
        evidence["artifacts"] = [{"path": "../secret", "sha256": "sha256:" + "0" * 64}]
    elif mutate == "bool-id":
        evidence["attempt_id"] = True

    (tmp_path / "contract.json").write_bytes(canonical_json_bytes(contract))
    (tmp_path / "evidence.json").write_bytes(canonical_json_bytes(evidence))
    (tmp_path / "artifacts").mkdir()
    (tmp_path / "artifacts" / "probe.txt").write_bytes(artifact)
    return contract


def _config() -> dict[str, object]:
    return {
        "contract_file": "contract.json",
        "evidence_file": "evidence.json",
        "expected_source_sha": _SOURCE_SHA,
        "expected_image_digest": _IMAGE_DIGEST,
        "expected_host_id": "vm-hermes-1",
        "expected_runtime_user": "openclaw",
        "expected_deployment_id": "deploy-20260911-001",
        "expected_configuration_identity": "sha256:" + "c" * 64,
        "expected_run_id": 42,
        "expected_attempt_id": 1,
        "required_checks": ["runtime-probe"],
        "max_age_seconds": 300,
    }


def test_valid_runtime_evidence_passes(tmp_path: Path) -> None:
    _seed(tmp_path, captured_at=_NOW)
    rule = build(_config(), repo_root=tmp_path)
    assert (
        validate_runtime_evidence(
            rule.load_documents(),
            expected_identity=rule.expected_identity,
            required_checks=rule.required_checks,
            now=_NOW,
            max_age_seconds=rule.max_age_seconds,
        )
        == ()
    )


def test_empty_configuration_is_vacuous_and_does_not_open_files(tmp_path: Path) -> None:
    assert build({}, repo_root=tmp_path / "does-not-exist").run() == 0


def test_configured_missing_files_fail_actionably(tmp_path: Path, capsys: object) -> None:
    rule = build({"contract_file": "contract.json", "evidence_file": "evidence.json"}, repo_root=tmp_path)
    assert rule.run() == 1
    assert "fix:" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_baseline_cannot_suppress_bad_evidence(tmp_path: Path, capsys: object) -> None:
    _seed(tmp_path, mutate="wrong-source")
    baseline = tmp_path / ".architecture" / "baseline"
    baseline.mkdir(parents=True)
    (baseline / "runtime-evidence-contract-files.txt").write_text(
        "# existing violation\nevidence.json\n", encoding="utf-8"
    )
    assert build(_config(), repo_root=tmp_path).run() == 1
    assert "source-sha-mismatch" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_establish_baseline_rejects_invalid_runtime_evidence(tmp_path: Path, capsys: object) -> None:
    rule = build(
        {"contract_file": "missing.json", "evidence_file": "missing-evidence.json"},
        repo_root=tmp_path,
    )

    with pytest.raises(RuntimeError, match="cannot establish a baseline"):
        rule.establish_baseline()

    assert "missing-file" in capsys.readouterr().err  # type: ignore[attr-defined]
    assert not (tmp_path / ".architecture" / "baseline" / "runtime-evidence-contract-files.txt").exists()


def test_shared_core_helper_cannot_baseline_invalid_runtime_evidence(tmp_path: Path) -> None:
    config = {"contract_file": "missing.json", "evidence_file": "missing-evidence.json"}

    with pytest.raises(RuntimeError, match="cannot establish a baseline"):
        run_core_check(
            RuntimeEvidenceContract,
            ["--establish-baseline", "--repo-root", str(tmp_path)],
            config=config,
        )

    assert not (tmp_path / ".architecture" / "baseline" / "runtime-evidence-contract-files.txt").exists()


def test_catalogue_runner_fails_invalid_runtime_evidence_baseline(
    tmp_path: Path,
    capsys: object,
) -> None:
    rules = (
        RuleEntry(
            id="runtime-evidence-contract",
            gate="runtime-evidence-contract",
            check="core:runtime_evidence_contract",
            summary="runtime evidence matches the deployment attempt",
        ),
    )
    config = {"contract_file": "missing.json", "evidence_file": "missing-evidence.json"}

    verdict = run(
        rules,
        repo_root=tmp_path,
        core_check_configs={"runtime_evidence_contract": config},
        establish_baseline=True,
    )

    assert not verdict.ok
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert "missing-file" in captured.err
    assert "FAIL [runtime-evidence-contract]" in captured.out
    assert not (tmp_path / ".architecture" / "baseline" / "runtime-evidence-contract-files.txt").exists()


def test_configured_duplicate_key_fails_actionably(tmp_path: Path, capsys: object) -> None:
    _seed(tmp_path)
    (tmp_path / "evidence.json").write_text(
        '{"schema":"tc-fitness/runtime-evidence/v1","schema":"duplicate"}', encoding="utf-8"
    )
    assert build(_config(), repo_root=tmp_path).run() == 1
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert "duplicate-key" in captured.err
    assert "fix:" in captured.err


def test_tampered_artifact_fails(tmp_path: Path, capsys: object) -> None:
    _seed(tmp_path)
    (tmp_path / "artifacts" / "probe.txt").write_bytes(b"tampered\n")
    assert build(_config(), repo_root=tmp_path).run() == 1
    assert "artifact-digest-mismatch" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_wrong_contract_schema_fails(tmp_path: Path, capsys: object) -> None:
    _seed(tmp_path)
    contract = _contract()
    contract["schema"] = "wrong"
    (tmp_path / "contract.json").write_bytes(canonical_json_bytes(contract))
    assert build(_config(), repo_root=tmp_path).run() == 1
    assert "wrong-schema" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_nan_evidence_fails(tmp_path: Path, capsys: object) -> None:
    _seed(tmp_path)
    (tmp_path / "evidence.json").write_text(
        '{"schema":"tc-fitness/runtime-evidence/v1","value":NaN}', encoding="utf-8"
    )
    assert build(_config(), repo_root=tmp_path).run() == 1
    assert "invalid-json-constant" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_boolean_integer_identity_fails(tmp_path: Path, capsys: object) -> None:
    _seed(tmp_path, mutate="bool-id")
    assert build(_config(), repo_root=tmp_path).run() == 1
    assert "integer-id" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_unsafe_artifact_reference_fails(tmp_path: Path, capsys: object) -> None:
    _seed(tmp_path, mutate="unsafe-artifact")
    assert build(_config(), repo_root=tmp_path).run() == 1
    assert "unsafe-artifact-path" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_stale_skipped_and_exit_code_only_evidence_fail(tmp_path: Path, capsys: object) -> None:
    for mutation, code in (
        ("stale", "stale-evidence"),
        ("skipped", "check-skipped"),
        ("exit-only", "incomplete-observation"),
    ):
        case = tmp_path / mutation
        case.mkdir()
        _seed(case, mutate=mutation)
        assert build(_config(), repo_root=case).run() == 1
        assert code in capsys.readouterr().err  # type: ignore[attr-defined]


@pytest.mark.parametrize("required_checks", ["runtime-probe", [""], [1], ["runtime-probe", "runtime-probe"]])
def test_malformed_required_checks_fail_actionably(
    tmp_path: Path,
    capsys: object,
    required_checks: object,
) -> None:
    _seed(tmp_path)
    config = _config()
    config["required_checks"] = required_checks
    assert build(config, repo_root=tmp_path).run() == 1
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert "invalid-required-checks" in captured.err
    assert "fix:" in captured.err


@pytest.mark.parametrize(
    "checks",
    [
        [
            {
                "id": "runtime-probe",
                "status": "passed",
                "exit_code": 1,
                "observation": {"kind": "process", "state": "failed"},
            }
        ],
        [
            {
                "id": "runtime-probe",
                "status": "passed",
                "observation": {"kind": "process", "state": "healthy"},
            },
            {
                "id": "cleanup",
                "status": "failed",
                "observation": {"kind": "cleanup", "state": "failed"},
            },
        ],
        [
            {
                "id": "runtime-probe",
                "status": "unknown",
                "observation": {"kind": "process", "state": "healthy"},
            }
        ],
        [
            {
                "id": "runtime-probe",
                "status": "passed",
                "observation": {"kind": "process", "state": "unhealthy"},
            }
        ],
    ],
)
def test_failed_or_contradictory_emitted_check_cannot_pass(
    tmp_path: Path,
    capsys: object,
    checks: list[dict[str, object]],
) -> None:
    _seed(tmp_path)
    evidence = json.loads((tmp_path / "evidence.json").read_bytes())
    evidence["checks"] = checks
    (tmp_path / "evidence.json").write_bytes(canonical_json_bytes(evidence))
    assert build(_config(), repo_root=tmp_path).run() == 1
    assert "check-verdict" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_expected_denial_is_an_explicit_success_outcome(tmp_path: Path) -> None:
    _seed(tmp_path)
    evidence = json.loads((tmp_path / "evidence.json").read_bytes())
    evidence["checks"] = [
        {
            "id": "secret-denial",
            "status": "expected-denial",
            "exit_code": 1,
            "observation": {"kind": "access", "outcome": "denied"},
        }
    ]
    (tmp_path / "evidence.json").write_bytes(canonical_json_bytes(evidence))
    config = _config()
    config["required_checks"] = ["secret-denial"]
    assert build(config, repo_root=tmp_path).run() == 0


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("run_id", None),
        ("attempt_id", None),
        ("deployment_id", None),
        ("configuration_identity", None),
        ("run_id", "1"),
        ("attempt_id", True),
        ("deployment_id", ""),
        ("configuration_identity", 1),
    ],
)
def test_receipt_requires_complete_typed_identity_envelope(
    tmp_path: Path,
    capsys: object,
    field: str,
    bad_value: object,
) -> None:
    _seed(tmp_path)
    evidence = json.loads((tmp_path / "evidence.json").read_bytes())
    if bad_value is None:
        del evidence[field]
    else:
        evidence[field] = bad_value
    (tmp_path / "evidence.json").write_bytes(canonical_json_bytes(evidence))
    assert build(_config(), repo_root=tmp_path).run() == 1
    captured = capsys.readouterr().err  # type: ignore[attr-defined]
    assert "receipt-identity" in captured or "integer-id" in captured
    assert "fix:" in captured


@pytest.mark.parametrize(
    ("field", "replacement", "code"),
    [
        ("deployment_id", "deploy-earlier", "deployment-id-mismatch"),
        ("configuration_identity", "sha256:" + "d" * 64, "configuration-identity-mismatch"),
        ("run_id", 41, "run-id-mismatch"),
        ("attempt_id", 0, "attempt-id-mismatch"),
    ],
)
def test_receipt_must_match_independently_expected_attempt_identity(
    tmp_path: Path,
    capsys: object,
    field: str,
    replacement: object,
    code: str,
) -> None:
    _seed(tmp_path)
    evidence = json.loads((tmp_path / "evidence.json").read_bytes())
    evidence[field] = replacement
    (tmp_path / "evidence.json").write_bytes(canonical_json_bytes(evidence))

    assert build(_config(), repo_root=tmp_path).run() == 1
    assert code in capsys.readouterr().err  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("expected_deployment_id", None),
        ("expected_configuration_identity", ""),
        ("expected_run_id", "42"),
        ("expected_attempt_id", True),
    ],
)
def test_expected_attempt_identity_is_complete_and_typed(
    tmp_path: Path,
    capsys: object,
    field: str,
    bad_value: object,
) -> None:
    _seed(tmp_path)
    config = _config()
    config[field] = bad_value

    assert build(config, repo_root=tmp_path).run() == 1
    assert "expected-identity" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_large_artifact_hashing_uses_bounded_memory(tmp_path: Path) -> None:
    artifact = b"x" * (8 * 1024 * 1024)
    contract = _contract()
    evidence = _evidence(contract, artifact, captured_at=datetime.now(UTC))
    (tmp_path / "contract.json").write_bytes(canonical_json_bytes(contract))
    (tmp_path / "evidence.json").write_bytes(canonical_json_bytes(evidence))
    (tmp_path / "artifacts").mkdir()
    (tmp_path / "artifacts" / "probe.txt").write_bytes(artifact)
    del artifact

    tracemalloc.start()
    try:
        assert build(_config(), repo_root=tmp_path).run() == 0
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    assert peak < 3 * 1024 * 1024


@pytest.mark.parametrize("location", ["config", "artifact"])
def test_nul_path_is_an_actionable_finding(tmp_path: Path, capsys: object, location: str) -> None:
    _seed(tmp_path)
    config = _config()
    if location == "config":
        config["contract_file"] = "bad\x00.json"
    else:
        evidence = json.loads((tmp_path / "evidence.json").read_bytes())
        evidence["artifacts"] = [{"path": "bad\x00.txt", "sha256": "sha256:" + "0" * 64}]
        (tmp_path / "evidence.json").write_bytes(canonical_json_bytes(evidence))
    assert build(config, repo_root=tmp_path).run() == 1
    assert "fix:" in capsys.readouterr().err  # type: ignore[attr-defined]


def test_fifo_invalid_then_valid_evidence_cannot_split_status_from_findings(tmp_path: Path) -> None:
    """One immutable finding tuple prevents a second FIFO read from changing the verdict."""
    _seed(tmp_path)
    valid = (tmp_path / "evidence.json").read_bytes()
    evidence_path = tmp_path / "evidence.json"
    evidence_path.unlink()
    os.mkfifo(evidence_path)
    valid_written = threading.Event()

    def writer() -> None:
        with evidence_path.open("wb", buffering=0) as pipe:
            # Replace the pathname while the application holds the first FIFO
            # inode. A second writer on the replacement can therefore connect
            # only to a genuine second application open, never to the tail of
            # the first read.
            evidence_path.unlink()
            os.mkfifo(evidence_path)
            pipe.write(b"{}")
        with evidence_path.open("wb", buffering=0) as pipe:
            pipe.write(valid)
            valid_written.set()

    thread = threading.Thread(target=writer, daemon=True)
    thread.start()
    rules = (
        RuleEntry(
            id="runtime-evidence-contract",
            gate="runtime-evidence-contract",
            check="core:runtime_evidence_contract",
            summary="runtime evidence matches the deployment attempt",
        ),
    )
    with capture_check_evidence() as evidence:
        verdict = run(
            rules,
            repo_root=tmp_path,
            core_check_configs={"runtime_evidence_contract": _config()},
        )
    second_application_read = valid_written.is_set()
    cleanup_reader = os.open(evidence_path, os.O_RDONLY | os.O_NONBLOCK)
    try:
        thread.join(timeout=2)
    finally:
        os.close(cleanup_reader)

    assert not thread.is_alive()
    assert not second_application_read
    assert not verdict.ok
    assert evidence.findings
    assert evidence.results[0].status == "fail"


def test_replaced_fifo_protocol_detects_a_deliberate_second_read(tmp_path: Path) -> None:
    """Sabotage control: the inode-separated protocol observes a real re-open."""
    _seed(tmp_path)
    valid = (tmp_path / "evidence.json").read_bytes()
    evidence_path = tmp_path / "evidence.json"
    evidence_path.unlink()
    os.mkfifo(evidence_path)
    second_written = threading.Event()

    def writer() -> None:
        with evidence_path.open("wb", buffering=0) as pipe:
            evidence_path.unlink()
            os.mkfifo(evidence_path)
            pipe.write(b"{}")
        with evidence_path.open("wb", buffering=0) as pipe:
            pipe.write(valid)
            second_written.set()

    thread = threading.Thread(target=writer, daemon=True)
    thread.start()

    assert evidence_path.read_bytes() == b"{}"
    assert evidence_path.read_bytes() == valid
    thread.join(timeout=2)

    assert not thread.is_alive()
    assert second_written.is_set()
