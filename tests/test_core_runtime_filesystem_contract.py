"""Public contract and sabotage tests for runtime filesystem declarations."""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from tc_fitness.catalogue import RuleEntry
from tc_fitness.core_checks._runtime_contracts import (
    CONTRACT_SCHEMA,
    EVIDENCE_SCHEMA,
    canonical_json_bytes,
    resolve_contract,
)
from tc_fitness.runner import run

_SOURCE_SHA = "a" * 40
_IMAGE_DIGEST = "sha256:" + "b" * 64
_CONFIGURATION_IDENTITY = "sha256:" + "c" * 64
_ROOT_ACCESS = {
    "owner_uid": 1000,
    "owner_gid": 1000,
    "mode": 0o750,
    "access": {
        "uid": 1000,
        "gids": [1000, 1001],
        "read": True,
        "write": True,
        "traverse": True,
    },
}


def _filesystem() -> dict[str, object]:
    return {
        "namespaces": {
            "host": {"kind": "host", "root": "/"},
            "container": {"kind": "container", "root": "/"},
            "profile": {
                "kind": "profile",
                "root": "/hermes-home/profiles/{profile}",
                "physical_namespace": "container",
            },
        },
        "roots": {
            "host-home": {
                "namespace": "host",
                "path": "/data/hermes/service",
                "kind": "directory",
                "lifecycle": "persistent",
                **copy.deepcopy(_ROOT_ACCESS),
            },
            "container-home": {
                "namespace": "container",
                "path": "/hermes-home",
                "kind": "directory",
                "lifecycle": "persistent",
                **copy.deepcopy(_ROOT_ACCESS),
            },
            "profile-home": {
                "namespace": "profile",
                "path": "/hermes-home/profiles/{profile}",
                "kind": "directory",
                "lifecycle": "persistent",
                **copy.deepcopy(_ROOT_ACCESS),
            },
            "profile-user": {
                "namespace": "profile",
                "path": "/hermes-home/profiles/{profile}/USER.md",
                "kind": "file",
                "lifecycle": "generated",
                **copy.deepcopy(_ROOT_ACCESS),
            },
            "vault": {
                "namespace": "container",
                "path": "/data/obsidian-vault",
                "kind": "directory",
                "lifecycle": "shared",
                **copy.deepcopy(_ROOT_ACCESS),
            },
        },
        "mounts": [
            {
                "id": "home-mount",
                "source_root": "host-home",
                "target_namespace": "container",
                "target_path": "/hermes-home",
                "mode": "rw",
            }
        ],
        "aliases": [
            {
                "id": "profile-home-alias",
                "root": "profile-home",
                "namespace": "profile",
                "path": "/hermes-home/profiles/{profile}",
            }
        ],
        "symlinks": [
            {
                "id": "vault-link",
                "namespace": "container",
                "path": "/hermes-home/obsidian-vault",
                "target": "/data/obsidian-vault",
            }
        ],
        "allowed_nested_roots": [
            {
                "parent": "container-home",
                "child": "profile-home",
                "reason": "profiles are persistent children of the container home",
            },
            {
                "parent": "container-home",
                "child": "profile-user",
                "reason": "generated profile files live below the container home",
            },
            {
                "parent": "profile-home",
                "child": "profile-user",
                "reason": "the generated user file belongs to its profile",
            },
        ],
        "required_executables": [
            {
                "id": "runtime",
                "namespace": "container",
                "path": "/usr/local/bin/runtime",
            }
        ],
    }


def _contract() -> dict[str, object]:
    return {
        "schema": CONTRACT_SCHEMA,
        "environment": "prod",
        "target": "service",
        "filesystem": _filesystem(),
    }


def _minimal_contract(
    *,
    namespaces: dict[str, object],
    roots: dict[str, object],
    mounts: list[object] | None = None,
    symlinks: list[object] | None = None,
    required_executables: list[object] | None = None,
) -> dict[str, object]:
    for declaration in roots.values():
        if isinstance(declaration, dict):
            for field, value in _ROOT_ACCESS.items():
                declaration.setdefault(field, copy.deepcopy(value))
    return {
        "schema": CONTRACT_SCHEMA,
        "environment": "prod",
        "target": "service",
        "filesystem": {
            "namespaces": namespaces,
            "roots": roots,
            "mounts": mounts or [],
            "aliases": [],
            "symlinks": symlinks or [],
            "allowed_nested_roots": [],
            "required_executables": required_executables or [],
        },
    }


def _evidence() -> dict[str, object]:
    filesystem = _filesystem()
    roots = filesystem["roots"]
    assert isinstance(roots, dict)
    return {
        "schema": EVIDENCE_SCHEMA,
        "contract_digest": "sha256:" + hashlib.sha256(canonical_json_bytes(_contract())).hexdigest(),
        "source_sha": _SOURCE_SHA,
        "image_digest": _IMAGE_DIGEST,
        "host_id": "vm-service-1",
        "runtime_user": "service",
        "deployment_id": "deploy-20260911-001",
        "configuration_identity": _CONFIGURATION_IDENTITY,
        "run_id": 42,
        "attempt_id": 1,
        "captured_at": datetime.now(UTC).isoformat(),
        "checks": [
            {
                "id": "filesystem-probe",
                "status": "passed",
                "observation": {"kind": "filesystem", "state": "healthy"},
            }
        ],
        "artifacts": [],
        "filesystem": {
            "roots": [
                {"id": root_id, **declaration, "exists": True}
                for root_id, declaration in roots.items()
                if isinstance(declaration, dict)
            ],
            "mounts": [
                {
                    "id": "home-mount",
                    "source_root": "host-home",
                    "target_namespace": "container",
                    "target_path": "/hermes-home",
                    "mode": "rw",
                    "mounted": True,
                }
            ],
            "aliases": [
                {
                    "id": "profile-home-alias",
                    "root": "profile-home",
                    "namespace": "profile",
                    "path": "/hermes-home/profiles/{profile}",
                    "resolved_path": "/hermes-home/profiles/{profile}",
                    "exists": True,
                }
            ],
            "symlinks": [
                {
                    "id": "vault-link",
                    "namespace": "container",
                    "path": "/hermes-home/obsidian-vault",
                    "target": "/data/obsidian-vault",
                    "exists": True,
                }
            ],
            "executables": [
                {
                    "id": "runtime",
                    "namespace": "container",
                    "path": "/usr/local/bin/runtime",
                    "exists": True,
                    "executable": True,
                }
            ],
        },
    }


def _module() -> Any:
    try:
        return importlib.import_module("tc_fitness.core_checks.runtime_filesystem_contract")
    except ModuleNotFoundError:
        pytest.fail("core:runtime_filesystem_contract is not implemented")


def _seed(tmp_path: Path, contract: object, evidence: object | None = None) -> None:
    (tmp_path / "contract.json").write_bytes(canonical_json_bytes(contract))
    if evidence is not None:
        (tmp_path / "evidence.json").write_bytes(canonical_json_bytes(evidence))


def _config(*, observations: bool = False) -> dict[str, object]:
    config: dict[str, object] = {
        "contract_file": "contract.json",
        "environment": "prod",
        "target": "service",
    }
    if observations:
        config["evidence_file"] = "evidence.json"
        config.update(
            {
                "expected_source_sha": _SOURCE_SHA,
                "expected_image_digest": _IMAGE_DIGEST,
                "expected_host_id": "vm-service-1",
                "expected_runtime_user": "service",
                "expected_deployment_id": "deploy-20260911-001",
                "expected_configuration_identity": _CONFIGURATION_IDENTITY,
                "expected_run_id": 42,
                "expected_attempt_id": 1,
                "required_checks": ["filesystem-probe"],
                "max_age_seconds": 300,
            }
        )
    return config


def _run_cli(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, "-m", "tc_fitness.runtime_contract", *args],
        check=False,
        capture_output=True,
    )


def _run_filesystem_module_cli(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, "-m", "tc_fitness.core_checks.runtime_filesystem_contract", *args],
        check=False,
        capture_output=True,
    )


@pytest.mark.integration
def test_valid_declaration_and_complete_live_observation_pass(tmp_path: Path) -> None:
    _seed(tmp_path, _contract(), _evidence())
    module = _module()

    assert module.build(_config(), repo_root=tmp_path).run() == 0
    assert module.build(_config(observations=True), repo_root=tmp_path).run() == 0


@pytest.mark.integration
def test_module_cli_runs_a_selected_configured_contract(tmp_path: Path) -> None:
    """The module entry point must not silently skip a supplied contract."""
    contract = _contract()
    filesystem = contract["filesystem"]
    assert isinstance(filesystem, dict)
    roots = filesystem["roots"]
    assert isinstance(roots, dict)
    root = roots["vault"]
    assert isinstance(root, dict)
    root["namespace"] = "missing"
    _seed(tmp_path, contract)

    result = _run_filesystem_module_cli(
        "--repo-root",
        str(tmp_path),
        "--contract-file",
        "contract.json",
        "--environment",
        "prod",
        "--target",
        "service",
    )

    assert result.returncode == 1
    assert b"undefined-namespace" in result.stderr


@pytest.mark.integration
def test_empty_configuration_is_a_vacuous_pass(tmp_path: Path) -> None:
    assert _module().build({}, repo_root=tmp_path).run() == 0


@pytest.mark.integration
@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (
            lambda doc: doc["filesystem"]["roots"]["vault"].__setitem__("namespace", "missing"),
            "undefined-namespace",
        ),
        (
            lambda doc: doc["filesystem"]["mounts"][0].__setitem__("source_root", "missing"),
            "undefined-root",
        ),
        (
            lambda doc: doc["filesystem"]["mounts"][0].__setitem__("mode", "read-write"),
            "invalid-mount-mode",
        ),
        (
            lambda doc: (
                doc["filesystem"]["mounts"][0].__setitem__("target_path", "/outside")
                or doc["filesystem"]["mounts"][0].__setitem__("target_namespace", "profile")
            ),
            "namespace-escape",
        ),
        (
            lambda doc: doc["filesystem"]["aliases"][0].__setitem__("path", "/hermes-home/profiles/other"),
            "alias-disagreement",
        ),
        (
            lambda doc: (
                doc["filesystem"]["symlinks"][0].__setitem__("target", "/outside-profile")
                or doc["filesystem"]["symlinks"][0].__setitem__("namespace", "profile")
            ),
            "symlink-escape",
        ),
        (
            lambda doc: doc["filesystem"]["roots"]["profile-home"].__setitem__(
                "path", "/hermes-home/profiles/prefix-{profile}"
            ),
            "invalid-posix-path",
        ),
    ],
)
def test_invalid_references_and_namespaces_fail(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    mutation: Any,
    code: str,
) -> None:
    contract = _contract()
    mutation(contract)
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    error = capsys.readouterr().err
    assert code in error
    assert "fix:" in error
    assert "next:" in error
    assert "run:" in error


@pytest.mark.integration
def test_sibling_prefix_is_not_a_physical_overlap(tmp_path: Path) -> None:
    contract = _contract()
    filesystem = contract["filesystem"]
    assert isinstance(filesystem, dict)
    roots = filesystem["roots"]
    assert isinstance(roots, dict)
    roots["profiles-sibling"] = {
        "namespace": "container",
        "path": "/hermes-home/profiles-archive",
        "kind": "directory",
        "lifecycle": "archive",
        **copy.deepcopy(_ROOT_ACCESS),
    }
    allowances = filesystem["allowed_nested_roots"]
    assert isinstance(allowances, list)
    allowances.append(
        {
            "parent": "container-home",
            "child": "profiles-sibling",
            "reason": "the archive is an intentional child of the container home",
        }
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 0


@pytest.mark.integration
def test_cross_namespace_component_prefix_requires_reasoned_allowance(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = {
        "schema": CONTRACT_SCHEMA,
        "environment": "prod",
        "target": "service",
        "filesystem": {
            "namespaces": {
                "container": {"kind": "container", "root": "/"},
                "profile": {
                    "kind": "profile",
                    "root": "/hermes-home/profiles/{profile}",
                    "physical_namespace": "container",
                },
            },
            "roots": {
                "cluster": {
                    "namespace": "container",
                    "path": "/hermes-home/profiles/",
                    "kind": "directory",
                    "lifecycle": "persistent",
                    **copy.deepcopy(_ROOT_ACCESS),
                },
                "profile": {
                    "namespace": "profile",
                    "path": "/hermes-home/profiles/consultant-delivery-consultant/USER.md",
                    "kind": "file",
                    "lifecycle": "generated",
                    **copy.deepcopy(_ROOT_ACCESS),
                },
            },
            "mounts": [],
            "aliases": [],
            "symlinks": [],
            "allowed_nested_roots": [],
            "required_executables": [],
        },
    }
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    error = capsys.readouterr().err
    assert "nested-root-overlap" in error
    assert "/hermes-home/profiles/" in error
    assert "/hermes-home/profiles/consultant-delivery-consultant/USER.md" in error


@pytest.mark.integration
def test_literal_namespace_root_does_not_contain_child_identity_wildcard(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/safe"}},
        roots={
            "tenant-data": {
                "namespace": "container",
                "path": "/{tenant}/data",
                "kind": "directory",
                "lifecycle": "persistent",
            }
        },
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "namespace-escape" in capsys.readouterr().err


@pytest.mark.integration
@pytest.mark.parametrize(
    ("path", "exit_code"),
    [
        ("/data/a/b", 1),
        ("/data/a/a", 0),
        ("/data/{left}/{right}", 1),
        ("/data/{other}/{other}", 0),
    ],
)
def test_namespace_boundary_requires_consistent_repeated_identity(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], path: str, exit_code: int
) -> None:
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/data/{id}/{id}"}},
        roots={
            "data": {
                "namespace": "container",
                "path": path,
                "kind": "directory",
                "lifecycle": "persistent",
            }
        },
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    error = capsys.readouterr().err
    assert ("namespace-escape" in error) == bool(exit_code)


@pytest.mark.integration
@pytest.mark.parametrize(
    ("surface", "code"),
    [
        ("root", "duplicate-root-path"),
        ("mount", "duplicate-mount-destination"),
        ("symlink", "duplicate-symlink-source"),
        ("executable", "duplicate-executable"),
    ],
)
@pytest.mark.parametrize(("literal_path", "exit_code"), [("/data/x/y", 0), ("/data/x/x", 1)])
def test_repeated_identity_collisions_require_one_consistent_binding(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    surface: str,
    code: str,
    literal_path: str,
    exit_code: int,
) -> None:
    roots: dict[str, object] = {
        "target": {
            "namespace": "container",
            "path": "/target",
            "kind": "directory",
            "lifecycle": "persistent",
        }
    }
    mounts: list[object] = []
    symlinks: list[object] = []
    executables: list[object] = []
    for identifier, path in (("pattern", "/data/{id}/{id}"), ("literal", literal_path)):
        if surface == "root":
            roots[identifier] = {
                "namespace": "container",
                "path": path,
                "kind": "directory",
                "lifecycle": "persistent",
            }
        elif surface == "mount":
            mounts.append(
                {
                    "id": identifier,
                    "source_root": "target",
                    "target_namespace": "container",
                    "target_path": path,
                    "mode": "rw",
                }
            )
        elif surface == "symlink":
            symlinks.append({"id": identifier, "namespace": "container", "path": path, "target": "/target"})
        else:
            executables.append({"id": identifier, "namespace": "container", "path": path})
    _seed(
        tmp_path,
        _minimal_contract(
            namespaces={"container": {"kind": "container", "root": "/"}},
            roots=roots,
            mounts=mounts,
            symlinks=symlinks,
            required_executables=executables,
        ),
    )

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    error = capsys.readouterr().err
    assert (code in error) == bool(exit_code)


@pytest.mark.integration
@pytest.mark.parametrize(("identity", "exit_code"), [("x", 0), ("a", 1)])
def test_pattern_intersection_propagates_repeated_identity_equalities(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], identity: str, exit_code: int
) -> None:
    _seed(
        tmp_path,
        _minimal_contract(
            namespaces={"container": {"kind": "container", "root": "/"}},
            roots={
                identifier: {
                    "namespace": "container",
                    "path": path,
                    "kind": "directory",
                    "lifecycle": "persistent",
                }
                for identifier, path in (
                    ("left", "/data/{id}/{id}/a"),
                    ("right", f"/data/{identity}/{{other}}/{{other}}"),
                )
            },
        ),
    )

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    assert ("duplicate-root-path" in capsys.readouterr().err) == bool(exit_code)


@pytest.mark.integration
def test_independent_container_namespaces_may_reuse_absolute_paths(tmp_path: Path) -> None:
    contract = _minimal_contract(
        namespaces={
            "cluster-a": {"kind": "container", "root": "/"},
            "cluster-b": {"kind": "container", "root": "/"},
        },
        roots={
            "a-data": {
                "namespace": "cluster-a",
                "path": "/safe/data",
                "kind": "directory",
                "lifecycle": "persistent",
            },
            "b-data": {
                "namespace": "cluster-b",
                "path": "/safe/data",
                "kind": "directory",
                "lifecycle": "persistent",
            },
        },
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 0


@pytest.mark.integration
@pytest.mark.parametrize(
    ("namespaces", "expected_code"),
    [
        (
            {"container": {"kind": "container", "root": "/", "physical_namespace": []}},
            "invalid-physical-namespace",
        ),
        (
            {
                "container": {
                    "kind": "container",
                    "root": "/",
                    "physical_namespace": "missing",
                }
            },
            "undefined-physical-namespace",
        ),
        (
            {
                "cluster-a": {
                    "kind": "container",
                    "root": "/",
                    "physical_namespace": "cluster-b",
                },
                "cluster-b": {
                    "kind": "container",
                    "root": "/",
                    "physical_namespace": "cluster-a",
                },
            },
            "physical-namespace-cycle",
        ),
    ],
)
def test_invalid_physical_namespace_relationships_produce_structured_findings(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    namespaces: dict[str, object],
    expected_code: str,
) -> None:
    contract = _minimal_contract(namespaces=namespaces, roots={})
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert expected_code in capsys.readouterr().err


@pytest.mark.integration
def test_explicitly_shared_physical_namespaces_detect_duplicate_root_paths(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _minimal_contract(
        namespaces={
            "container": {"kind": "container", "root": "/"},
            "profile": {
                "kind": "profile",
                "root": "/safe/{profile}",
                "physical_namespace": "container",
            },
        },
        roots={
            "container-data": {
                "namespace": "container",
                "path": "/safe/alice",
                "kind": "directory",
                "lifecycle": "persistent",
            },
            "profile-data": {
                "namespace": "profile",
                "path": "/safe/{profile}",
                "kind": "directory",
                "lifecycle": "persistent",
            },
        },
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "duplicate-root-path" in capsys.readouterr().err


@pytest.mark.integration
@pytest.mark.parametrize(
    ("surface", "expected_code"),
    [
        ("mount", "duplicate-mount-destination"),
        ("symlink", "duplicate-symlink-source"),
        ("executable", "duplicate-executable"),
    ],
)
def test_identity_pattern_and_literal_paths_collide_within_one_namespace(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    surface: str,
    expected_code: str,
) -> None:
    roots: dict[str, object] = {
        "source-a": {
            "namespace": "container",
            "path": "/sources/a",
            "kind": "directory",
            "lifecycle": "persistent",
        },
        "source-b": {
            "namespace": "container",
            "path": "/sources/b",
            "kind": "directory",
            "lifecycle": "persistent",
        },
        "target-a": {
            "namespace": "container",
            "path": "/targets/a",
            "kind": "directory",
            "lifecycle": "persistent",
        },
        "target-b": {
            "namespace": "container",
            "path": "/targets/b",
            "kind": "directory",
            "lifecycle": "persistent",
        },
    }
    mounts: list[object] = []
    symlinks: list[object] = []
    executables: list[object] = []
    if surface == "mount":
        mounts = [
            {
                "id": "pattern",
                "source_root": "source-a",
                "target_namespace": "container",
                "target_path": "/safe/{profile}",
                "mode": "rw",
            },
            {
                "id": "literal",
                "source_root": "source-b",
                "target_namespace": "container",
                "target_path": "/safe/alice",
                "mode": "ro",
            },
        ]
    elif surface == "symlink":
        symlinks = [
            {
                "id": "pattern",
                "namespace": "container",
                "path": "/safe/{profile}",
                "target": "/targets/a",
            },
            {
                "id": "literal",
                "namespace": "container",
                "path": "/safe/alice",
                "target": "/targets/b",
            },
        ]
    else:
        executables = [
            {"id": "pattern", "namespace": "container", "path": "/safe/{profile}"},
            {"id": "literal", "namespace": "container", "path": "/safe/alice"},
        ]
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots=roots,
        mounts=mounts,
        symlinks=symlinks,
        required_executables=executables,
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert expected_code in capsys.readouterr().err


@pytest.mark.integration
def test_mount_collisions_follow_explicit_physical_namespace_relationships(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _minimal_contract(
        namespaces={
            "container": {"kind": "container", "root": "/"},
            "profile": {
                "kind": "profile",
                "root": "/safe/{profile}",
                "physical_namespace": "container",
            },
        },
        roots={
            "source-a": {
                "namespace": "container",
                "path": "/sources/a",
                "kind": "directory",
                "lifecycle": "persistent",
            },
            "source-b": {
                "namespace": "container",
                "path": "/sources/b",
                "kind": "directory",
                "lifecycle": "persistent",
            },
        },
        mounts=[
            {
                "id": "container-target",
                "source_root": "source-a",
                "target_namespace": "container",
                "target_path": "/safe/alice",
                "mode": "rw",
            },
            {
                "id": "profile-target",
                "source_root": "source-b",
                "target_namespace": "profile",
                "target_path": "/safe/{profile}",
                "mode": "ro",
            },
        ],
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "duplicate-mount-destination" in capsys.readouterr().err


@pytest.mark.integration
def test_catalogue_dispatches_configured_filesystem_check(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _contract()
    filesystem = contract["filesystem"]
    assert isinstance(filesystem, dict)
    filesystem["allowed_nested_roots"] = []
    _seed(tmp_path, contract)
    rules = (
        RuleEntry(
            id="runtime-filesystem-contract",
            gate="runtime-filesystem-contract",
            check="core:runtime_filesystem_contract",
            summary="runtime filesystem declarations agree",
        ),
    )

    verdict = run(
        rules,
        repo_root=tmp_path,
        core_check_configs={"runtime_filesystem_contract": _config()},
    )

    assert not verdict.ok
    captured = capsys.readouterr()
    assert "nested-root-overlap" in captured.err
    assert "FAIL [runtime-filesystem-contract]" in captured.out


@pytest.mark.integration
def test_file_root_cannot_be_parent_of_a_nested_root(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _contract()
    filesystem = contract["filesystem"]
    assert isinstance(filesystem, dict)
    roots = filesystem["roots"]
    allowances = filesystem["allowed_nested_roots"]
    assert isinstance(roots, dict)
    assert isinstance(allowances, list)
    roots["file-parent"] = {
        "namespace": "container",
        "path": "/opt/runtime",
        "kind": "file",
        "lifecycle": "immutable",
        **copy.deepcopy(_ROOT_ACCESS),
    }
    roots["nested"] = {
        "namespace": "container",
        "path": "/opt/runtime/bin",
        "kind": "directory",
        "lifecycle": "immutable",
        **copy.deepcopy(_ROOT_ACCESS),
    }
    allowances.append({"parent": "file-parent", "child": "nested", "reason": "invalid on purpose"})
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "file-root-contains-path" in capsys.readouterr().err


@pytest.mark.integration
def test_file_root_cannot_contain_a_mount_target(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """A regular file cannot provide a directory that can be mounted into."""
    contract = _contract()
    filesystem = contract["filesystem"]
    assert isinstance(filesystem, dict)
    roots = filesystem["roots"]
    mounts = filesystem["mounts"]
    assert isinstance(roots, dict)
    assert isinstance(mounts, list)
    roots["file-parent"] = {
        "namespace": "container",
        "path": "/opt/runtime",
        "kind": "file",
        "lifecycle": "immutable",
        **copy.deepcopy(_ROOT_ACCESS),
    }
    mounts.append(
        {
            "id": "impossible-mount",
            "source_root": "host-home",
            "target_namespace": "container",
            "target_path": "/opt/runtime/data",
            "mode": "rw",
        }
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "file-root-contains-path" in capsys.readouterr().err


@pytest.mark.integration
def test_symlink_cycle_is_rejected(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    contract = _contract()
    filesystem = contract["filesystem"]
    assert isinstance(filesystem, dict)
    filesystem["symlinks"] = [
        {
            "id": "first",
            "namespace": "container",
            "path": "/links/first",
            "target": "/links/second",
        },
        {
            "id": "second",
            "namespace": "container",
            "path": "/links/second",
            "target": "/links/first",
        },
    ]
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "symlink-cycle" in capsys.readouterr().err


@pytest.mark.integration
def test_symlink_chain_that_enters_a_cycle_reports_its_entry_path(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots={},
        symlinks=[
            {
                "id": "entry",
                "namespace": "container",
                "path": "/links/entry",
                "target": "/links/first",
            },
            {
                "id": "first",
                "namespace": "container",
                "path": "/links/first",
                "target": "/links/second",
            },
            {
                "id": "second",
                "namespace": "container",
                "path": "/links/second",
                "target": "/links/first",
            },
        ],
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    error = capsys.readouterr().err
    assert "symlink-cycle" in error
    assert "/links/entry" in error


@pytest.mark.integration
def test_shared_physical_namespaces_form_one_symlink_cycle(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _minimal_contract(
        namespaces={
            "a": {"kind": "container", "root": "/"},
            "b": {
                "kind": "profile",
                "root": "/",
                "physical_namespace": "a",
            },
        },
        roots={
            "a-target": {
                "namespace": "a",
                "path": "/b",
                "kind": "directory",
                "lifecycle": "persistent",
            },
            "b-target": {
                "namespace": "b",
                "path": "/a",
                "kind": "directory",
                "lifecycle": "persistent",
            },
        },
        symlinks=[
            {"id": "a-link", "namespace": "a", "path": "/a", "target": "/b"},
            {"id": "b-link", "namespace": "b", "path": "/b", "target": "/a"},
        ],
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "symlink-cycle" in capsys.readouterr().err


@pytest.mark.integration
def test_shared_physical_namespace_accepts_cross_logical_symlink_target(tmp_path: Path) -> None:
    contract = _minimal_contract(
        namespaces={
            "container": {"kind": "container", "root": "/"},
            "profile": {
                "kind": "profile",
                "root": "/",
                "physical_namespace": "container",
            },
        },
        roots={
            "target": {
                "namespace": "container",
                "path": "/target",
                "kind": "directory",
                "lifecycle": "persistent",
            }
        },
        symlinks=[
            {
                "id": "profile-alias",
                "namespace": "profile",
                "path": "/alias",
                "target": "/target",
            }
        ],
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 0


@pytest.mark.integration
def test_symlink_resolution_preserves_suffixes_when_detecting_cycles(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots={
            "y": {
                "namespace": "container",
                "path": "/y",
                "kind": "directory",
                "lifecycle": "persistent",
            },
            "x-z": {
                "namespace": "container",
                "path": "/x/z",
                "kind": "directory",
                "lifecycle": "persistent",
            },
        },
        symlinks=[
            {"id": "x", "namespace": "container", "path": "/x", "target": "/y"},
            {
                "id": "y-z",
                "namespace": "container",
                "path": "/y/z",
                "target": "/x/z",
            },
        ],
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "symlink-cycle" in capsys.readouterr().err


@pytest.mark.integration
@pytest.mark.parametrize(("count", "exit_code"), [(64, 0), (65, 1)])
def test_symlink_declaration_budget_bounds_resolution_work(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], count: int, exit_code: int
) -> None:
    roots = {
        f"target-{index}": {
            "namespace": "container",
            "path": f"/targets/{index}",
            "kind": "directory",
            "lifecycle": "persistent",
        }
        for index in range(count)
    }
    symlinks = [
        {
            "id": f"link-{index}",
            "namespace": "container",
            "path": f"/links/{index}",
            "target": f"/targets/{index}",
        }
        for index in range(count)
    ]
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots=roots,
        symlinks=symlinks,
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    error = capsys.readouterr().err
    if exit_code:
        assert "filesystem-work-limit" in error
        assert "64" in error
    else:
        assert error == ""


@pytest.mark.integration
@pytest.mark.parametrize(("length", "exit_code"), [(4096, 0), (4097, 1)])
def test_symlink_path_component_budget_is_checked_before_resolution(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], length: int, exit_code: int
) -> None:
    target = "/target" + "/x" * (length - 1)
    _seed(
        tmp_path,
        _minimal_contract(
            namespaces={"container": {"kind": "container", "root": "/"}},
            roots={
                "target": {
                    "namespace": "container",
                    "path": target,
                    "kind": "directory",
                    "lifecycle": "persistent",
                }
            },
            symlinks=[{"id": "entry", "namespace": "container", "path": "/entry", "target": target}],
        ),
    )

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    error = capsys.readouterr().err
    if exit_code:
        assert "filesystem-work-limit" in error
        assert "4096-component path" in error
    else:
        assert error == ""


@pytest.mark.integration
@pytest.mark.parametrize(("extra_component", "exit_code"), [(0, 0), (1, 1)])
def test_symlink_retained_path_node_budget_counts_distinct_suffixes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], extra_component: int, exit_code: int
) -> None:
    # 64 disjoint paths of 1024 components consume exactly 65536 nodes.
    targets = [
        "/"
        + "/".join(
            f"node-{index}-{position}" for position in range(1024 + (extra_component if index == 63 else 0))
        )
        for index in range(64)
    ]
    _seed(
        tmp_path,
        _minimal_contract(
            namespaces={"container": {"kind": "container", "root": "/"}},
            roots={
                f"target-{index}": {
                    "namespace": "container",
                    "path": target,
                    "kind": "directory",
                    "lifecycle": "persistent",
                }
                for index, target in enumerate(targets)
            },
            symlinks=[
                {
                    "id": f"entry-{index}",
                    "namespace": "container",
                    "path": f"/entry-{index}",
                    "target": target,
                }
                for index, target in enumerate(targets)
            ],
        ),
    )

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    error = capsys.readouterr().err
    if exit_code:
        assert "filesystem-work-limit" in error
        assert "65536-node" in error
    else:
        assert error == ""


@pytest.mark.integration
@pytest.mark.parametrize(("extra_component", "exit_code"), [(0, 0), (1, 1)])
def test_symlink_total_component_work_budget_has_an_exact_boundary(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], extra_component: int, exit_code: int
) -> None:
    # Each start costs 4095 target components plus 12289 source-prefix components:
    # 64 * (4095 + 193 + 63 * 192) = 1048576. One longer final target adds one unit.
    target = "/target" + "/x" * 4094
    final_target = target + "/x" * extra_component
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots={
            "target": {
                "namespace": "container",
                "path": target,
                "kind": "directory",
                "lifecycle": "persistent",
            }
        },
        symlinks=[
            {
                "id": f"entry-{index}",
                "namespace": "container",
                "path": f"/entry-{index}" + "/x" * (192 if index == 0 else 191),
                "target": final_target if index == 63 else target,
            }
            for index in range(64)
        ],
    )
    if extra_component:
        filesystem = contract["filesystem"]
        assert isinstance(filesystem, dict)
        roots = filesystem["roots"]
        assert isinstance(roots, dict)
        roots["final-target"] = {
            "namespace": "container",
            "path": final_target,
            "kind": "directory",
            "lifecycle": "persistent",
        }
        filesystem["allowed_nested_roots"] = [
            {
                "parent": "target",
                "child": "final-target",
                "reason": "the work-boundary fixture adds one component",
            }
        ]
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    error = capsys.readouterr().err
    if exit_code:
        assert "filesystem-work-limit" in error
        assert "1048576-component work" in error
    else:
        assert error == ""


@pytest.mark.integration
def test_compact_expanding_symlink_hits_path_budget_without_retaining_growing_paths(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    target = "/a" + "/x" * 128
    _seed(
        tmp_path,
        _minimal_contract(
            namespaces={"container": {"kind": "container", "root": "/"}},
            roots={
                "target": {
                    "namespace": "container",
                    "path": target,
                    "kind": "directory",
                    "lifecycle": "persistent",
                }
            },
            symlinks=[{"id": "expanding", "namespace": "container", "path": "/a", "target": target}],
        ),
    )

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    error = capsys.readouterr().err
    assert "filesystem-work-limit" in error
    assert "4096-component path" in error
    assert "symlink-cycle" not in error


@pytest.mark.integration
@pytest.mark.parametrize(("final_components", "exit_code"), [(4096, 0), (4097, 1)])
def test_finite_symlink_growth_respects_the_resolved_path_boundary(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], final_components: int, exit_code: int
) -> None:
    first_target = "/b" + "/x" * 128
    middle_target = "/a" + "/y" * (final_components - 129)
    _seed(
        tmp_path,
        _minimal_contract(
            namespaces={"container": {"kind": "container", "root": "/"}},
            roots={
                identifier: {
                    "namespace": "container",
                    "path": path,
                    "kind": "directory",
                    "lifecycle": "persistent",
                }
                for identifier, path in (
                    ("first", first_target),
                    ("middle", middle_target),
                    ("entry", "/a/start"),
                )
            },
            symlinks=[
                {"id": "first", "namespace": "container", "path": "/a", "target": first_target},
                {
                    "id": "middle",
                    "namespace": "container",
                    "path": first_target + "/start",
                    "target": middle_target,
                },
                {"id": "entry", "namespace": "container", "path": "/entry", "target": "/a/start"},
            ],
        ),
    )

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    error = capsys.readouterr().err
    assert "symlink-cycle" not in error
    if exit_code:
        assert "filesystem-work-limit" in error
        assert "4096-component path" in error
    else:
        assert error == ""


@pytest.mark.integration
def test_ambiguous_symlink_patterns_have_a_bounded_resolution_state_space(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    layers = 13
    symlinks = [
        {
            "id": f"layer-{layer}-{identity}",
            "namespace": "container",
            "path": f"/layer-{layer}/{identity}",
            "target": (f"/layer-{layer + 1}/{{choice_{layer + 1}}}" if layer + 1 < layers else "/end"),
        }
        for layer in range(layers)
        for identity in ("a", "b")
    ]
    roots = {
        "end": {
            "namespace": "container",
            "path": "/end",
            "kind": "directory",
            "lifecycle": "persistent",
        },
        **{
            f"layer-{layer}-target": {
                "namespace": "container",
                "path": f"/layer-{layer}/{{choice_{layer}}}",
                "kind": "directory",
                "lifecycle": "persistent",
            }
            for layer in range(1, layers)
        },
    }
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots=roots,
        symlinks=symlinks,
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    error = capsys.readouterr().err
    assert "filesystem-work-limit" in error
    assert "4096" in error


@pytest.mark.integration
def test_shorter_wildcard_branch_does_not_suppress_longer_binding_specific_cycle(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots={
            "launch-target": {
                "namespace": "container",
                "path": "/data/{choice}/long",
                "kind": "directory",
                "lifecycle": "persistent",
            },
            "done": {
                "namespace": "container",
                "path": "/done/end",
                "kind": "directory",
                "lifecycle": "persistent",
            },
        },
        symlinks=[
            {
                "id": "launch",
                "namespace": "container",
                "path": "/launch/entry",
                "target": "/data/{choice}/long",
            },
            {
                "id": "short-a",
                "namespace": "container",
                "path": "/data/a",
                "target": "/done/end",
            },
            {
                "id": "long-b",
                "namespace": "container",
                "path": "/data/b/long",
                "target": "/launch/entry",
            },
        ],
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "symlink-cycle" in capsys.readouterr().err


@pytest.mark.integration
@pytest.mark.parametrize(
    ("shorter_path", "longer_path", "exit_code"),
    [
        ("/data", "/data/x", 0),
        ("/data/{id}", "/data/{id}/x", 0),
        ("/data/{other}", "/data/{id}/x", 1),
    ],
)
def test_shorter_symlink_takes_precedence_only_for_the_same_binding(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    shorter_path: str,
    longer_path: str,
    exit_code: int,
) -> None:
    _seed(
        tmp_path,
        _minimal_contract(
            namespaces={"container": {"kind": "container", "root": "/"}},
            roots={
                "done": {
                    "namespace": "container",
                    "path": "/done",
                    "kind": "directory",
                    "lifecycle": "persistent",
                }
            },
            symlinks=[
                {"id": "shorter", "namespace": "container", "path": shorter_path, "target": "/done"},
                {"id": "longer", "namespace": "container", "path": longer_path, "target": longer_path},
            ],
        ),
    )

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    assert ("symlink-cycle" in capsys.readouterr().err) == bool(exit_code)


@pytest.mark.integration
@pytest.mark.parametrize(("depth", "exit_code"), [(2, 0), (4094, 0), (4095, 1)])
def test_repeated_symlink_declaration_can_consume_suffix_and_terminate(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], depth: int, exit_code: int
) -> None:
    nested_path = "/safe/" + "a/" * depth + "end"
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots={
            "safe": {
                "namespace": "container",
                "path": "/safe",
                "kind": "directory",
                "lifecycle": "persistent",
            },
            "nested-end": {
                "namespace": "container",
                "path": nested_path,
                "kind": "directory",
                "lifecycle": "persistent",
            },
        },
        symlinks=[
            {
                "id": "consume-a",
                "namespace": "container",
                "path": "/safe/a",
                "target": "/safe",
            },
            {
                "id": "entry",
                "namespace": "container",
                "path": "/link",
                "target": nested_path,
            },
        ],
    )
    filesystem = contract["filesystem"]
    assert isinstance(filesystem, dict)
    filesystem["allowed_nested_roots"] = [
        {
            "parent": "safe",
            "child": "nested-end",
            "reason": "the finite resolution fixture terminates at a child of the safe root",
        }
    ]
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    error = capsys.readouterr().err
    assert "symlink-cycle" not in error
    if exit_code:
        assert "filesystem-work-limit" in error
        assert "4096" in error
    else:
        assert error == ""


@pytest.mark.integration
@pytest.mark.parametrize(
    ("middle_target", "exit_code"),
    [("/a/y/z", 0), ("/a/x", 1)],
)
def test_symlink_suffix_growth_requires_full_state_repetition_for_a_cycle(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], middle_target: str, exit_code: int
) -> None:
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots={
            identifier: {
                "namespace": "container",
                "path": path,
                "kind": "directory",
                "lifecycle": "persistent",
            }
            for identifier, path in (("b-c", "/b/c"), ("a-y-z", "/a/y/z"), ("a-x", "/a/x"))
        },
        symlinks=[
            {"id": "a", "namespace": "container", "path": "/a", "target": "/b/c"},
            {"id": "b-c-x", "namespace": "container", "path": "/b/c/x", "target": middle_target},
            {"id": "entry", "namespace": "container", "path": "/entry", "target": "/a/x"},
        ],
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    error = capsys.readouterr().err
    assert ("symlink-cycle" in error) == bool(exit_code)
    assert "filesystem-work-limit" not in error


@pytest.mark.integration
def test_symlink_resolution_keeps_identity_binding_when_a_path_omits_it(tmp_path: Path) -> None:
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots={
            "two": {
                "namespace": "container",
                "path": "/two/{id}",
                "kind": "directory",
                "lifecycle": "persistent",
            }
        },
        symlinks=[
            {"id": "one", "namespace": "container", "path": "/one/{id}", "target": "/bridge"},
            {"id": "bridge", "namespace": "container", "path": "/bridge", "target": "/two/{id}"},
            {"id": "two-b", "namespace": "container", "path": "/two/b", "target": "/one/a"},
        ],
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 0


@pytest.mark.integration
@pytest.mark.parametrize(("target_path", "exit_code"), [("/data/x/y", 0), ("/data/x/x", 1)])
def test_symlink_source_matching_requires_consistent_repeated_identity(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], target_path: str, exit_code: int
) -> None:
    _seed(
        tmp_path,
        _minimal_contract(
            namespaces={"container": {"kind": "container", "root": "/"}},
            roots={
                "target": {
                    "namespace": "container",
                    "path": target_path,
                    "kind": "directory",
                    "lifecycle": "persistent",
                }
            },
            symlinks=[
                {"id": "repeated", "namespace": "container", "path": "/data/{id}/{id}", "target": "/entry"},
                {"id": "entry", "namespace": "container", "path": "/entry", "target": target_path},
            ],
        ),
    )

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    assert ("symlink-cycle" in capsys.readouterr().err) == bool(exit_code)


@pytest.mark.integration
@pytest.mark.parametrize(
    ("target_path", "exit_code"),
    [("/data/x/y", 1), ("/data/{left}/{right}", 1), ("/data/{other}/{other}", 0)],
)
def test_symlink_target_coverage_requires_consistent_repeated_identity(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], target_path: str, exit_code: int
) -> None:
    _seed(
        tmp_path,
        _minimal_contract(
            namespaces={"container": {"kind": "container", "root": "/"}},
            roots={
                "target": {
                    "namespace": "container",
                    "path": "/data/{id}/{id}",
                    "kind": "directory",
                    "lifecycle": "persistent",
                }
            },
            symlinks=[{"id": "entry", "namespace": "container", "path": "/entry", "target": target_path}],
        ),
    )

    assert _module().build(_config(), repo_root=tmp_path).run() == exit_code
    assert ("undefined-symlink-target" in capsys.readouterr().err) == bool(exit_code)


@pytest.mark.integration
def test_wildcard_symlink_target_requires_complete_declared_pattern_coverage(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots={
            "known": {
                "namespace": "container",
                "path": "/data/known",
                "kind": "directory",
                "lifecycle": "persistent",
            }
        },
        symlinks=[
            {
                "id": "entry",
                "namespace": "container",
                "path": "/entry",
                "target": "/data/{choice}",
            }
        ],
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "undefined-symlink-target" in capsys.readouterr().err


@pytest.mark.integration
@pytest.mark.parametrize(
    ("source_path", "target_path"),
    [
        ("/safe/data", "/safe/data/child"),
        ("/safe/{profile}", "/safe/alice/child"),
    ],
)
def test_nonrepeating_symlink_expansion_exhausts_work_budget_without_claiming_a_cycle(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    source_path: str,
    target_path: str,
) -> None:
    contract = _minimal_contract(
        namespaces={"container": {"kind": "container", "root": "/"}},
        roots={
            "target": {
                "namespace": "container",
                "path": target_path,
                "kind": "directory",
                "lifecycle": "persistent",
            }
        },
        symlinks=[
            {
                "id": "expanding-link",
                "namespace": "container",
                "path": source_path,
                "target": target_path,
            }
        ],
    )
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    error = capsys.readouterr().err
    assert "filesystem-work-limit" in error
    assert "4096" in error
    assert "symlink-cycle" not in error


@pytest.mark.integration
def test_symlink_missing_declared_target_is_rejected(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    contract = _contract()
    filesystem = contract["filesystem"]
    assert isinstance(filesystem, dict)
    symlinks = filesystem["symlinks"]
    assert isinstance(symlinks, list)
    symlink = symlinks[0]
    assert isinstance(symlink, dict)
    symlink["target"] = "/data/missing"
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "undefined-symlink-target" in capsys.readouterr().err


@pytest.mark.integration
def test_duplicate_mount_destination_is_rejected(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    contract = _contract()
    filesystem = contract["filesystem"]
    assert isinstance(filesystem, dict)
    mounts = filesystem["mounts"]
    assert isinstance(mounts, list)
    duplicate = copy.deepcopy(mounts[0])
    assert isinstance(duplicate, dict)
    duplicate["id"] = "duplicate-home-mount"
    mounts.append(duplicate)
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "duplicate-mount-destination" in capsys.readouterr().err


@pytest.mark.integration
@pytest.mark.parametrize(
    ("section", "field", "bad_value", "expected_code"),
    [
        ("namespace", "kind", [], "invalid-namespace-kind"),
        ("root", "kind", {}, "invalid-root-kind"),
        ("mount", "mode", [], "invalid-mount-mode"),
    ],
)
def test_enum_container_shapes_produce_structured_findings(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    section: str,
    field: str,
    bad_value: object,
    expected_code: str,
) -> None:
    contract = _contract()
    filesystem = contract["filesystem"]
    assert isinstance(filesystem, dict)
    if section == "namespace":
        namespaces = filesystem["namespaces"]
        assert isinstance(namespaces, dict)
        declaration = namespaces["container"]
    elif section == "root":
        roots = filesystem["roots"]
        assert isinstance(roots, dict)
        declaration = roots["vault"]
    else:
        mounts = filesystem["mounts"]
        assert isinstance(mounts, list)
        declaration = mounts[0]
    assert isinstance(declaration, dict)
    declaration[field] = bad_value
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert expected_code in capsys.readouterr().err


@pytest.mark.integration
@pytest.mark.parametrize(
    ("collection", "code"),
    [
        ("roots", "missing-root-observation"),
        ("mounts", "missing-mount-observation"),
        ("aliases", "missing-alias-observation"),
        ("symlinks", "missing-symlink-observation"),
        ("executables", "missing-executable-observation"),
    ],
)
def test_live_observation_requires_every_declared_item_once(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    collection: str,
    code: str,
) -> None:
    evidence = _evidence()
    filesystem = evidence["filesystem"]
    assert isinstance(filesystem, dict)
    observations = filesystem[collection]
    assert isinstance(observations, list)
    observations.clear()
    _seed(tmp_path, _contract(), evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 1
    assert code in capsys.readouterr().err


@pytest.mark.integration
def test_duplicate_live_observation_is_rejected(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    evidence = _evidence()
    filesystem = evidence["filesystem"]
    assert isinstance(filesystem, dict)
    roots = filesystem["roots"]
    assert isinstance(roots, list)
    roots.append(copy.deepcopy(roots[0]))
    _seed(tmp_path, _contract(), evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 1
    assert "duplicate-root-observation" in capsys.readouterr().err


@pytest.mark.integration
@pytest.mark.parametrize(
    ("collection", "field", "bad_value", "code"),
    [
        ("roots", "exists", False, "root-observation-mismatch"),
        ("mounts", "mode", "ro", "mount-observation-mismatch"),
        ("aliases", "resolved_path", "/wrong", "alias-observation-mismatch"),
        ("symlinks", "target", "/wrong", "symlink-observation-mismatch"),
        ("executables", "executable", False, "executable-observation-mismatch"),
    ],
)
def test_partial_or_conflicting_live_observation_is_rejected(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    collection: str,
    field: str,
    bad_value: object,
    code: str,
) -> None:
    evidence = _evidence()
    filesystem = evidence["filesystem"]
    assert isinstance(filesystem, dict)
    observations = filesystem[collection]
    assert isinstance(observations, list)
    observation = observations[0]
    assert isinstance(observation, dict)
    observation[field] = bad_value
    _seed(tmp_path, _contract(), evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 1
    assert code in capsys.readouterr().err


@pytest.mark.integration
def test_observation_boolean_does_not_accept_integer_truthiness(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    evidence = _evidence()
    filesystem = evidence["filesystem"]
    assert isinstance(filesystem, dict)
    roots = filesystem["roots"]
    assert isinstance(roots, list)
    root = roots[0]
    assert isinstance(root, dict)
    root["exists"] = 1
    _seed(tmp_path, _contract(), evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 1
    assert "root-observation-mismatch" in capsys.readouterr().err


@pytest.mark.integration
def test_observation_unknown_fields_are_rejected(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    evidence = _evidence()
    filesystem = evidence["filesystem"]
    assert isinstance(filesystem, dict)
    roots = filesystem["roots"]
    assert isinstance(roots, list)
    root = roots[0]
    assert isinstance(root, dict)
    root["stale"] = False
    _seed(tmp_path, _contract(), evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 1
    assert "root-observation-unknown-field" in capsys.readouterr().err


@pytest.mark.integration
def test_unknown_observation_collection_is_rejected(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    evidence = _evidence()
    filesystem = evidence["filesystem"]
    assert isinstance(filesystem, dict)
    filesystem["old_executables"] = []
    _seed(tmp_path, _contract(), evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 1
    assert "unknown-filesystem-observation-collection" in capsys.readouterr().err


@pytest.mark.integration
def test_filesystem_observation_rejects_evidence_for_another_contract(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Filesystem observations must be cryptographically bound to this contract."""
    evidence = _evidence()
    evidence["contract_digest"] = "sha256:" + "0" * 64
    _seed(tmp_path, _contract(), evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 1
    assert "contract-digest-mismatch" in capsys.readouterr().err


@pytest.mark.integration
def test_filesystem_observation_rejects_other_deployment_identity(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A matching filesystem shape cannot satisfy a different deployment receipt."""
    evidence = _evidence()
    evidence["deployment_id"] = "deploy-20260911-other"
    _seed(tmp_path, _contract(), evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 1
    assert "deployment-id-mismatch" in capsys.readouterr().err


@pytest.mark.integration
def test_root_permissions_and_effective_access_observation_pass_when_exact(tmp_path: Path) -> None:
    """Observed ownership, mode, identity and access must match the declaration."""
    contract = _contract()
    evidence = _evidence()
    _seed(tmp_path, contract, evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 0


@pytest.mark.integration
def test_root_effective_group_membership_mismatch_is_rejected(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A collector cannot report access for a different supplementary-group set."""
    evidence = _evidence()
    filesystem = evidence["filesystem"]
    assert isinstance(filesystem, dict)
    roots = filesystem["roots"]
    assert isinstance(roots, list)
    root = next(item for item in roots if item["id"] == "vault")
    assert isinstance(root, dict)
    access = root["access"]
    assert isinstance(access, dict)
    access["gids"] = [1000]
    _seed(tmp_path, _contract(), evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 1
    assert "root-observation-mismatch" in capsys.readouterr().err


@pytest.mark.integration
def test_filesystem_observation_rejects_stale_evidence(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A receipt outside the configured freshness window cannot prove live state."""
    evidence = _evidence()
    evidence["captured_at"] = (datetime.now(UTC) - timedelta(seconds=301)).isoformat()
    _seed(tmp_path, _contract(), evidence)

    assert _module().build(_config(observations=True), repo_root=tmp_path).run() == 1
    assert "stale-evidence" in capsys.readouterr().err


@pytest.mark.integration
def test_external_registry_reference_is_resolved_by_public_cli(tmp_path: Path) -> None:
    clusters = tmp_path / "platform" / "clusters.yaml"
    clusters.parent.mkdir()
    clusters.write_text(
        "kind: persistent-cluster-registry\n"
        "version: 1\n"
        "clusters:\n"
        "  - cluster_id: alpha\n"
        "    home: /data/alpha\n"
        "  - cluster_id: beta\n"
        "    home: /data/beta\n",
        encoding="utf-8",
    )
    registry = {
        "schema": CONTRACT_SCHEMA,
        "external_references": {"clusters": {"file": "platform/clusters.yaml", "pointer": "/clusters"}},
        "environments": {
            "prod": {
                "targets": {
                    "service": {
                        "cluster_registry": {"$external_ref": "clusters"},
                        "filesystem": _filesystem(),
                    }
                }
            }
        },
    }
    registry_path = tmp_path / "deployment-targets.yaml"
    registry_path.write_text(
        json.dumps(registry),
        encoding="utf-8",
    )
    output = tmp_path / "resolved.json"

    result = _run_cli(
        "resolve",
        "--contract",
        str(registry_path),
        "--environment",
        "prod",
        "--target",
        "service",
        "--output",
        str(output),
    )

    assert result.returncode == 0, result.stderr.decode()
    resolved = json.loads(output.read_bytes())
    assert resolved["cluster_registry"] == [
        {"cluster_id": "alpha", "home": "/data/alpha"},
        {"cluster_id": "beta", "home": "/data/beta"},
    ]
    assert "external_references" not in resolved


@pytest.mark.integration
def test_selected_registry_ignores_unreferenced_missing_external_file(tmp_path: Path) -> None:
    """A selected target is not coupled to another target's external input."""
    (tmp_path / "selected.yaml").write_text("clusters: []\n", encoding="utf-8")
    registry = {
        "schema": CONTRACT_SCHEMA,
        "external_references": {
            "selected": {"file": "selected.yaml", "pointer": "/clusters"},
            "other-target": {"file": "missing.yaml", "pointer": "/clusters"},
        },
        "environments": {
            "prod": {
                "targets": {"service": {"clusters": {"$external_ref": "selected"}}},
            },
            "staging": {
                "targets": {"service": {"clusters": {"$external_ref": "other-target"}}},
            },
        },
    }

    resolved, findings = resolve_contract(
        registry,
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )

    assert findings == ()
    assert resolved is not None
    assert resolved["clusters"] == []


@pytest.mark.integration
@pytest.mark.parametrize(
    ("reference", "expected_code"),
    [
        ({"file": "../outside.yaml", "pointer": "/clusters"}, "unsafe-external-reference"),
        ({"file": "clusters.yaml", "pointer": "/missing"}, "external-pointer-missing"),
        ({"file": "clusters.yaml", "pointer": "clusters"}, "invalid-external-pointer"),
    ],
)
def test_external_registry_reference_fails_closed(
    tmp_path: Path,
    reference: dict[str, str],
    expected_code: str,
) -> None:
    (tmp_path / "clusters.yaml").write_text("clusters: []\n", encoding="utf-8")
    registry = {
        "schema": CONTRACT_SCHEMA,
        "external_references": {"clusters": reference},
        "environments": {"prod": {"targets": {"service": {"clusters": {"$external_ref": "clusters"}}}}},
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_bytes(canonical_json_bytes(registry))
    output = tmp_path / "result.json"

    result = _run_cli(
        "resolve",
        "--contract",
        str(registry_path),
        "--environment",
        "prod",
        "--target",
        "service",
        "--output",
        str(output),
    )

    assert result.returncode == 1
    assert expected_code in {item["code"] for item in json.loads(output.read_bytes())["findings"]}


@pytest.mark.integration
def test_external_registry_reference_rejects_duplicate_yaml_keys(tmp_path: Path) -> None:
    (tmp_path / "clusters.yaml").write_text(
        "clusters: []\nclusters: [{cluster_id: duplicate}]\n",
        encoding="utf-8",
    )
    registry = {
        "schema": CONTRACT_SCHEMA,
        "external_references": {"clusters": {"file": "clusters.yaml", "pointer": "/clusters"}},
        "environments": {"prod": {"targets": {"service": {"clusters": {"$external_ref": "clusters"}}}}},
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_bytes(canonical_json_bytes(registry))
    output = tmp_path / "result.json"

    result = _run_cli(
        "resolve",
        "--contract",
        str(registry_path),
        "--environment",
        "prod",
        "--target",
        "service",
        "--output",
        str(output),
    )

    assert result.returncode == 1
    assert "duplicate-key" in {item["code"] for item in json.loads(output.read_bytes())["findings"]}


@pytest.mark.integration
def test_external_registry_symlink_escape_is_rejected(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-outside.yaml"
    outside.write_text("clusters: []\n", encoding="utf-8")
    (tmp_path / "clusters.yaml").symlink_to(outside)
    registry = {
        "schema": CONTRACT_SCHEMA,
        "external_references": {"clusters": {"file": "clusters.yaml", "pointer": "/clusters"}},
        "environments": {"prod": {"targets": {"service": {"clusters": {"$external_ref": "clusters"}}}}},
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_bytes(canonical_json_bytes(registry))
    output = tmp_path / "result.json"

    result = _run_cli(
        "resolve",
        "--contract",
        str(registry_path),
        "--environment",
        "prod",
        "--target",
        "service",
        "--output",
        str(output),
    )

    assert result.returncode == 1
    assert "unsafe-external-reference" in {
        item["code"] for item in json.loads(output.read_bytes())["findings"]
    }


@pytest.mark.integration
def test_undefined_external_reference_is_rejected(tmp_path: Path) -> None:
    registry = {
        "schema": CONTRACT_SCHEMA,
        "environments": {"prod": {"targets": {"service": {"clusters": {"$external_ref": "missing"}}}}},
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_bytes(canonical_json_bytes(registry))
    output = tmp_path / "result.json"

    result = _run_cli(
        "resolve",
        "--contract",
        str(registry_path),
        "--environment",
        "prod",
        "--target",
        "service",
        "--output",
        str(output),
    )

    assert result.returncode == 1
    assert "undefined-external-reference" in {
        item["code"] for item in json.loads(output.read_bytes())["findings"]
    }


@pytest.mark.integration
def test_direct_resolution_supports_json_pointer_escapes_and_list_indices(tmp_path: Path) -> None:
    external = tmp_path / "external.json"
    external.write_bytes(canonical_json_bytes({"groups": {"a/b": [{"id": "selected"}]}}))
    registry = {
        "schema": CONTRACT_SCHEMA,
        "external_references": {"selected": {"file": "external.json", "pointer": "/groups/a~1b/0"}},
        "environments": {"prod": {"targets": {"service": {"selection": {"$external_ref": "selected"}}}}},
    }

    resolved, findings = resolve_contract(
        registry,
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )

    assert findings == ()
    assert resolved is not None
    assert resolved["selection"] == {"id": "selected"}


@pytest.mark.integration
def test_external_pointer_rejects_unbounded_array_index_without_raising(tmp_path: Path) -> None:
    (tmp_path / "external.json").write_bytes(canonical_json_bytes({"items": []}))
    registry = {
        "schema": CONTRACT_SCHEMA,
        "external_references": {
            "selected": {
                "file": "external.json",
                "pointer": f"/items/{'9' * 5000}",
            }
        },
        "environments": {"prod": {"targets": {"service": {"selection": {"$external_ref": "selected"}}}}},
    }

    resolved, findings = resolve_contract(
        registry,
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )

    assert resolved is None
    assert "invalid-external-pointer" in {finding.code for finding in findings}


@pytest.mark.integration
def test_external_pointer_rejects_noncanonical_array_index(tmp_path: Path) -> None:
    (tmp_path / "external.json").write_bytes(canonical_json_bytes({"items": ["first"]}))
    registry = {
        "schema": CONTRACT_SCHEMA,
        "external_references": {"selected": {"file": "external.json", "pointer": "/items/00"}},
        "environments": {"prod": {"targets": {"service": {"selection": {"$external_ref": "selected"}}}}},
    }

    resolved, findings = resolve_contract(
        registry,
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )

    assert resolved is None
    assert "invalid-external-pointer" in {finding.code for finding in findings}


@pytest.mark.integration
@pytest.mark.parametrize(
    ("declarations", "code"),
    [
        ([], "invalid-external-references"),
        ({"clusters": "clusters.yaml"}, "invalid-external-reference"),
        ({"clusters": {"file": "clusters.yaml"}}, "invalid-external-reference"),
        (
            {"clusters": {"file": "clusters.yaml", "pointer": "/clusters", "extra": True}},
            "invalid-external-reference",
        ),
        ({"clusters": {"file": 42, "pointer": "/clusters"}}, "invalid-external-reference"),
        ({"clusters": {"file": "clusters.yaml", "pointer": "/bad~escape"}}, "invalid-external-pointer"),
        ({"clusters": {"file": "missing.yaml", "pointer": "/clusters"}}, "missing-file"),
    ],
)
def test_direct_resolution_rejects_malformed_external_declarations(
    tmp_path: Path,
    declarations: object,
    code: str,
) -> None:
    (tmp_path / "clusters.yaml").write_text("clusters: []\n", encoding="utf-8")
    registry = {
        "schema": CONTRACT_SCHEMA,
        "external_references": declarations,
        "environments": {"prod": {"targets": {"service": {"clusters": {"$external_ref": "clusters"}}}}},
    }

    resolved, findings = resolve_contract(
        registry,
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )

    assert resolved is None
    assert code in {finding.code for finding in findings}


@pytest.mark.integration
def test_external_reference_placeholder_cannot_have_sibling_fields(tmp_path: Path) -> None:
    (tmp_path / "clusters.yaml").write_text("clusters: []\n", encoding="utf-8")
    registry = {
        "schema": CONTRACT_SCHEMA,
        "external_references": {"clusters": {"file": "clusters.yaml", "pointer": "/clusters"}},
        "environments": {
            "prod": {"targets": {"service": {"clusters": {"$external_ref": "clusters", "fallback": []}}}}
        },
    }

    resolved, findings = resolve_contract(
        registry,
        environment="prod",
        target="service",
        source=tmp_path / "registry.json",
    )

    assert resolved is None
    assert {finding.code for finding in findings} == {"invalid-external-reference-use"}


@pytest.mark.integration
def test_already_selected_contract_resolves_its_external_references(tmp_path: Path) -> None:
    (tmp_path / "clusters.yaml").write_text("clusters: [{cluster_id: alpha}]\n", encoding="utf-8")
    contract = {
        "schema": CONTRACT_SCHEMA,
        "environment": "prod",
        "target": "service",
        "external_references": {"clusters": {"file": "clusters.yaml", "pointer": "/clusters"}},
        "clusters": {"$external_ref": "clusters"},
    }

    resolved, findings = resolve_contract(
        contract,
        environment="prod",
        target="service",
        source=tmp_path / "contract.json",
    )

    assert findings == ()
    assert resolved is not None
    assert resolved["clusters"] == [{"cluster_id": "alpha"}]
    assert "external_references" not in resolved
