"""Public contract tests for the shared runtime-contract protocol helpers."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks._runtime_contracts import (
    CONTRACT_SCHEMA,
    ContractDocuments,
    RuntimeContractRule,
    load_contract_documents,
    load_runtime_document,
    resolve_contract,
)

pytestmark = pytest.mark.integration


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


def _selected_contract() -> dict[str, object]:
    return {
        "schema": CONTRACT_SCHEMA,
        "environment": "prod",
        "target": "hermes",
        "filesystem": {},
        "access": {},
        "deployment": {},
        "evidence": {},
    }


@pytest.mark.parametrize(
    ("body", "code"),
    [
        ('{"schema":"tc-fitness/runtime-contract/v1","schema":"duplicate"}', "duplicate-key"),
        ('{"schema":"tc-fitness/runtime-contract/v1","value":NaN}', "invalid-json-constant"),
        ('{"schema":"wrong"}', "wrong-schema"),
        ('{"schema":"tc-fitness/runtime-contract/v1","access":{"identities":[{"uid":true}]}}', "integer-id"),
    ],
)
def test_strict_json_contract_failures_are_actionable(tmp_path: Path, body: str, code: str) -> None:
    (tmp_path / "contract.json").write_text(body, encoding="utf-8")
    documents, findings = load_contract_documents(
        {"contract_file": "contract.json"},
        repo_root=tmp_path,
    )
    assert documents is None
    assert code in {finding.code for finding in findings}
    assert all(finding.fix for finding in findings)


def test_configured_path_must_stay_beneath_repo_root(tmp_path: Path) -> None:
    documents, findings = load_contract_documents(
        {"contract_file": "../contract.json"},
        repo_root=tmp_path,
    )
    assert documents is None
    assert {finding.code for finding in findings} == {"unsafe-config-path"}


def test_missing_configured_contract_is_a_finding(tmp_path: Path) -> None:
    documents, findings = load_contract_documents(
        {"contract_file": "missing.json"},
        repo_root=tmp_path,
    )
    assert documents is None
    assert {finding.code for finding in findings} == {"missing-file"}


@pytest.mark.parametrize(
    ("name", "body", "code"),
    [
        ("contract.json", b"\xff", "invalid-utf8"),
        ("contract.json", b"[]", "wrong-document-shape"),
        ("contract.json", b'{"value": 1e999}', "invalid-number"),
        ("contract.yaml", b"\xff", "invalid-utf8"),
        ("contract.yaml", b"- item\n", "wrong-document-shape"),
        ("contract.yaml", b"key: [unterminated\n", "invalid-yaml"),
        ("contract.txt", b"{}", "unsupported-format"),
    ],
)
def test_runtime_document_rejects_invalid_public_inputs(
    tmp_path: Path, name: str, body: bytes, code: str
) -> None:
    path = tmp_path / name
    path.write_bytes(body)
    value, findings, _raw = load_runtime_document(path, expected_schema=None)
    assert value is None
    assert code in {finding.code for finding in findings}


def test_empty_contract_config_is_inactive(tmp_path: Path) -> None:
    assert load_contract_documents({}, repo_root=tmp_path) == (None, ())


def test_required_evidence_needs_a_configured_path(tmp_path: Path) -> None:
    _write_json(tmp_path / "contract.json", _selected_contract())
    documents, findings = load_contract_documents(
        {"contract_file": "contract.json"}, repo_root=tmp_path, require_evidence=True
    )
    assert documents is None
    assert {finding.code for finding in findings} == {"missing-config"}


def test_symlinked_contract_cannot_escape_repository(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-outside-contract.json"
    _write_json(outside, _selected_contract())
    (tmp_path / "contract.json").symlink_to(outside)
    try:
        documents, findings = load_contract_documents({"contract_file": "contract.json"}, repo_root=tmp_path)
    finally:
        outside.unlink()
    assert documents is None
    assert {finding.code for finding in findings} == {"unsafe-config-path"}


def test_runtime_contract_rule_public_base_behaviour(tmp_path: Path) -> None:
    inactive = RuntimeContractRule.from_config({}, repo_root=tmp_path)
    assert inactive.collect_findings() == ()
    assert inactive.validate_configuration() == ()
    assert (
        inactive.validate_documents(
            ContractDocuments(
                contract_path=tmp_path / "contract.json",
                contract=_selected_contract(),
                contract_bytes=b"{}",
                evidence_path=None,
                evidence=None,
                evidence_bytes=None,
            )
        )
        == ()
    )
    assert inactive.run() == 0
    with pytest.raises(ValueError, match="not configured"):
        inactive.load_documents()

    active = RuntimeContractRule.from_config({"contract_file": "missing.json"}, repo_root=tmp_path)
    assert active.file_has_violation(tmp_path / "anything") is False
    assert active.run() == 1


def test_loader_preserves_exact_source_bytes(tmp_path: Path) -> None:
    contract = _selected_contract()
    body = json.dumps(contract, indent=2).encode("utf-8") + b"\n"
    (tmp_path / "contract.json").write_bytes(body)
    documents, findings = load_contract_documents({"contract_file": "contract.json"}, repo_root=tmp_path)
    assert findings == ()
    assert isinstance(documents, ContractDocuments)
    assert documents.contract_bytes == body
    assert documents.contract == contract


def test_yaml_duplicate_keys_are_rejected(tmp_path: Path) -> None:
    pytest.importorskip("yaml")
    (tmp_path / "contract.yaml").write_text(
        "schema: tc-fitness/runtime-contract/v1\nschema: duplicate\n",
        encoding="utf-8",
    )
    documents, findings = load_contract_documents(
        {"contract_file": "contract.yaml"},
        repo_root=tmp_path,
    )
    assert documents is None
    assert {finding.code for finding in findings} == {"duplicate-key"}


def test_yaml_repeated_container_aliases_are_rejected_before_expansion(tmp_path: Path) -> None:
    pytest.importorskip("yaml")
    aliases = ["seed: &level0 [value]"]
    for level in range(1, 19):
        aliases.append(f"level{level}: &level{level} [*level{level - 1}, *level{level - 1}]")
    (tmp_path / "contract.yaml").write_text(
        "schema: tc-fitness/runtime-contract/v1\n"
        "environment: prod\n"
        "target: hermes\n" + "\n".join(aliases) + "\n",
        encoding="utf-8",
    )

    documents, findings = load_contract_documents(
        {"contract_file": "contract.yaml"},
        repo_root=tmp_path,
    )

    assert documents is None
    assert {finding.code for finding in findings} == {"repeated-container-alias"}


def test_explicit_null_environments_is_not_treated_as_a_selected_contract(tmp_path: Path) -> None:
    registry = {"schema": CONTRACT_SCHEMA, "environments": None}

    selected, findings = resolve_contract(
        registry,
        environment="prod",
        target="hermes",
        source=tmp_path / "contract.json",
    )

    assert selected is None
    assert {finding.code for finding in findings} == {"invalid-environments"}


def test_yaml_without_optional_dependency_is_actionable(tmp_path: Path) -> None:
    registry = tmp_path / "contract.yaml"
    registry.write_text(
        "schema: tc-fitness/runtime-contract/v1\nenvironments:\n  prod:\n    targets:\n      hermes: {}\n",
        encoding="utf-8",
    )
    output = tmp_path / "result.json"
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(Path(__file__).parents[1] / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-S",
            "-m",
            "tc_fitness.runtime_contract",
            "resolve",
            "--contract",
            str(registry),
            "--environment",
            "prod",
            "--target",
            "hermes",
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        env=environment,
    )
    assert result.returncode == 1
    payload = json.loads(output.read_bytes())
    assert payload["findings"][0]["code"] == "yaml-dependency-missing"
    assert payload["findings"][0]["fix"]
