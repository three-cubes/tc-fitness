"""Public behaviour tests for the runtime evidence CORE check."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from pathlib import Path

from tc_fitness.core_checks._runtime_contracts import CONTRACT_SCHEMA, EVIDENCE_SCHEMA, canonical_json_bytes
from tc_fitness.core_checks.runtime_evidence_contract import build, validate_runtime_evidence

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
