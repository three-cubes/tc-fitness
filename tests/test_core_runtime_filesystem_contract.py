"""Public contract and sabotage tests for runtime filesystem declarations."""

from __future__ import annotations

import copy
import importlib
import json
import subprocess
import sys
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
            },
            "container-home": {
                "namespace": "container",
                "path": "/hermes-home",
                "kind": "directory",
                "lifecycle": "persistent",
            },
            "profile-home": {
                "namespace": "profile",
                "path": "/hermes-home/profiles/{profile}",
                "kind": "directory",
                "lifecycle": "persistent",
            },
            "profile-user": {
                "namespace": "profile",
                "path": "/hermes-home/profiles/{profile}/USER.md",
                "kind": "file",
                "lifecycle": "generated",
            },
            "vault": {
                "namespace": "container",
                "path": "/data/obsidian-vault",
                "kind": "directory",
                "lifecycle": "shared",
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
    return config


def _run_cli(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, "-m", "tc_fitness.runtime_contract", *args],
        check=False,
        capture_output=True,
    )


def test_valid_declaration_and_complete_live_observation_pass(tmp_path: Path) -> None:
    _seed(tmp_path, _contract(), _evidence())
    module = _module()

    assert module.build(_config(), repo_root=tmp_path).run() == 0
    assert module.build(_config(observations=True), repo_root=tmp_path).run() == 0


def test_empty_configuration_is_a_vacuous_pass(tmp_path: Path) -> None:
    assert _module().build({}, repo_root=tmp_path).run() == 0


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
                },
                "profile": {
                    "namespace": "profile",
                    "path": "/hermes-home/profiles/consultant-delivery-consultant/USER.md",
                    "kind": "file",
                    "lifecycle": "generated",
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
    }
    roots["nested"] = {
        "namespace": "container",
        "path": "/opt/runtime/bin",
        "kind": "directory",
        "lifecycle": "immutable",
    }
    allowances.append({"parent": "file-parent", "child": "nested", "reason": "invalid on purpose"})
    _seed(tmp_path, contract)

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "file-root-contains-path" in capsys.readouterr().err


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


def test_symlink_declaration_budget_bounds_resolution_work(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    count = 257
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

    assert _module().build(_config(), repo_root=tmp_path).run() == 1
    assert "filesystem-work-limit" in capsys.readouterr().err


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


def test_repeated_symlink_declaration_can_consume_suffix_and_terminate(tmp_path: Path) -> None:
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
                "path": "/safe/a/a/end",
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
                "target": "/safe/a/a/end",
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

    assert _module().build(_config(), repo_root=tmp_path).run() == 0


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


@pytest.mark.parametrize(
    ("source_path", "target_path"),
    [
        ("/safe/data", "/safe/data/child"),
        ("/safe/{profile}", "/safe/alice/child"),
    ],
)
def test_symlink_source_ancestor_of_its_target_is_a_cycle(
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
    assert "symlink-cycle" in capsys.readouterr().err


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
