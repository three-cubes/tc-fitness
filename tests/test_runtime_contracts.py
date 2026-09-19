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
    absolute_posix_components,
    canonical_json_bytes,
    component_paths_overlap,
    is_component_prefix,
    is_integer_identity,
    is_sha256_digest,
    load_contract_documents,
    resolve_contract,
)


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


@pytest.mark.unit
def test_canonical_json_bytes_are_stable_and_compact() -> None:
    assert canonical_json_bytes({"z": 1, "snowman": "☃", "a": [True, None]}) == (
        b'{"a":[true,null],"snowman":"\\u2603","z":1}'
    )


@pytest.mark.unit
def test_canonical_json_bytes_reject_nan() -> None:
    with pytest.raises(ValueError, match="Out of range float"):
        canonical_json_bytes({"value": float("nan")})


@pytest.mark.unit
def test_posix_path_helpers_compare_components_not_string_prefixes() -> None:
    profiles = absolute_posix_components("/hermes-home/profiles")
    profile = absolute_posix_components("/hermes-home/profiles/consultant")
    sibling = absolute_posix_components("/hermes-home/profiles-backup")
    assert profiles == ("hermes-home", "profiles")
    assert profile is not None and profiles is not None
    assert is_component_prefix(profiles, profile)
    assert component_paths_overlap(profiles, profile)
    assert sibling is not None
    assert not is_component_prefix(profiles, sibling)
    assert not component_paths_overlap(profiles, sibling)


@pytest.mark.unit
@pytest.mark.parametrize("value", ["relative/path", "/safe/../escape", "\\windows\\path", ""])
def test_posix_path_helpers_reject_non_absolute_or_unsafe_paths(value: str) -> None:
    assert absolute_posix_components(value) is None


@pytest.mark.unit
def test_identity_helpers_reject_boolean_ids_and_noncanonical_digests() -> None:
    assert is_integer_identity(1000)
    assert not is_integer_identity(True)
    assert is_sha256_digest("sha256:" + "a" * 64)
    assert not is_sha256_digest("sha256:" + "A" * 64)


@pytest.mark.integration
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


@pytest.mark.integration
def test_configured_path_must_stay_beneath_repo_root(tmp_path: Path) -> None:
    documents, findings = load_contract_documents(
        {"contract_file": "../contract.json"},
        repo_root=tmp_path,
    )
    assert documents is None
    assert {finding.code for finding in findings} == {"unsafe-config-path"}


@pytest.mark.integration
def test_missing_configured_contract_is_a_finding(tmp_path: Path) -> None:
    documents, findings = load_contract_documents(
        {"contract_file": "missing.json"},
        repo_root=tmp_path,
    )
    assert documents is None
    assert {finding.code for finding in findings} == {"missing-file"}


@pytest.mark.integration
def test_resolve_selects_one_registry_target_without_mutating_input() -> None:
    registry = {
        "schema": CONTRACT_SCHEMA,
        "environments": {
            "prod": {
                "targets": {
                    "hermes": {
                        "filesystem": {"roots": []},
                        "access": {},
                        "deployment": {},
                        "evidence": {},
                    }
                }
            }
        },
    }
    before = canonical_json_bytes(registry)
    selected, findings = resolve_contract(registry, environment="prod", target="hermes", source=Path("x"))
    assert findings == ()
    assert selected == {
        "schema": CONTRACT_SCHEMA,
        "environment": "prod",
        "target": "hermes",
        "filesystem": {"roots": []},
        "access": {},
        "deployment": {},
        "evidence": {},
    }
    assert canonical_json_bytes(registry) == before


@pytest.mark.integration
def test_loader_preserves_exact_source_bytes(tmp_path: Path) -> None:
    contract = _selected_contract()
    body = json.dumps(contract, indent=2).encode("utf-8") + b"\n"
    (tmp_path / "contract.json").write_bytes(body)
    documents, findings = load_contract_documents({"contract_file": "contract.json"}, repo_root=tmp_path)
    assert findings == ()
    assert isinstance(documents, ContractDocuments)
    assert documents.contract_bytes == body
    assert documents.contract == contract


@pytest.mark.integration
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


@pytest.mark.integration
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


@pytest.mark.integration
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


@pytest.mark.integration
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
