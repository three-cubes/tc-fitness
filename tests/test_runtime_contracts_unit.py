"""Public contract tests for the shared runtime-contract protocol helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tc_fitness.core_checks._runtime_contracts import (
    CONTRACT_SCHEMA,
    absolute_posix_components,
    canonical_json_bytes,
    component_paths_overlap,
    is_component_prefix,
    is_integer_identity,
    is_sha256_digest,
    resolve_contract,
)

pytestmark = pytest.mark.unit


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


def test_canonical_json_bytes_are_stable_and_compact() -> None:
    assert canonical_json_bytes({"z": 1, "snowman": "☃", "a": [True, None]}) == (
        b'{"a":[true,null],"snowman":"\\u2603","z":1}'
    )


def test_canonical_json_bytes_reject_nan() -> None:
    with pytest.raises(ValueError, match="Out of range float"):
        canonical_json_bytes({"value": float("nan")})


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


@pytest.mark.parametrize("value", ["relative/path", "/safe/../escape", "\\windows\\path", ""])
def test_posix_path_helpers_reject_non_absolute_or_unsafe_paths(value: str) -> None:
    assert absolute_posix_components(value) is None


def test_identity_helpers_reject_boolean_ids_and_noncanonical_digests() -> None:
    assert is_integer_identity(1000)
    assert not is_integer_identity(True)
    assert is_sha256_digest("sha256:" + "a" * 64)
    assert not is_sha256_digest("sha256:" + "A" * 64)


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
