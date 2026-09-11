"""CORE check for component-aware runtime filesystem contracts."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from itertools import combinations
from pathlib import Path
from typing import Any, cast

from tc_fitness.core_checks._runtime_contracts import (
    ContractDocuments,
    ContractFinding,
    PathPatternBindings,
    RuntimeContractRule,
    absolute_posix_components,
    component_pattern_paths_overlap,
    is_component_pattern_prefix,
    is_integer_identity,
    is_path_identity_segment,
    sort_findings,
)
from tc_fitness.core_checks.runtime_evidence_contract import (
    RuntimeEvidenceContract,
    validate_runtime_evidence,
)
from tc_fitness.lib import remediation as _remediation

_NAMESPACE_KINDS = frozenset({"host", "container", "profile"})
_ROOT_KINDS = frozenset({"directory", "file"})
_MOUNT_MODES = frozenset({"ro", "rw"})
_MAX_SYMLINK_DECLARATIONS = 64
_MAX_SYMLINK_RESOLUTION_STATES = 4_096
_MAX_SYMLINK_PATH_COMPONENTS = 4_096
_MAX_SYMLINK_PATH_NODES = 65_536
_MAX_SYMLINK_COMPONENT_WORK = 1_048_576

REMEDIATION = _remediation(
    fix=(
        "declare every runtime namespace, root, mount, alias, symlink and executable once; "
        "add a named reason for each intentional nested-root pair and collect complete live observations"
    ),
    nxt="resolve the selected contract and re-run the filesystem check before deployment",
    run="python -m tc_fitness.core_checks.runtime_filesystem_contract",
    passing="component-safe paths and one matching observation for every declared filesystem surface",
    forbidden="undefined, overlapping, escaping, cyclic, duplicated or partially observed filesystem state",
)


@dataclass(frozen=True)
class NamespaceDeclaration:
    id: str
    kind: str
    root: str
    components: tuple[str, ...]
    physical_namespace: str


@dataclass(frozen=True)
class RootDeclaration:
    id: str
    namespace: str
    path: str
    components: tuple[str, ...]
    kind: str
    lifecycle: str
    owner_uid: int
    owner_gid: int
    mode: int
    access: AccessRequirement


@dataclass(frozen=True)
class AccessRequirement:
    """Effective POSIX access observed for the runtime identity."""

    uid: int
    gids: tuple[int, ...]
    read: bool
    write: bool
    traverse: bool


@dataclass(frozen=True)
class MountDeclaration:
    id: str
    source_root: str
    target_namespace: str
    target_path: str
    target_components: tuple[str, ...]
    mode: str


@dataclass(frozen=True)
class AliasDeclaration:
    id: str
    root: str
    namespace: str
    path: str
    components: tuple[str, ...]


@dataclass(frozen=True)
class SymlinkDeclaration:
    id: str
    namespace: str
    path: str
    components: tuple[str, ...]
    target: str
    target_components: tuple[str, ...]


@dataclass(frozen=True)
class ExecutableDeclaration:
    id: str
    namespace: str
    path: str
    components: tuple[str, ...]


@dataclass(frozen=True)
class NestedRootAllowance:
    parent: str
    child: str
    reason: str


@dataclass(frozen=True)
class _FilesystemDeclarations:
    """Normalised filesystem declarations used by local and live validation."""

    namespaces: tuple[NamespaceDeclaration, ...]
    roots: tuple[RootDeclaration, ...]
    mounts: tuple[MountDeclaration, ...]
    aliases: tuple[AliasDeclaration, ...]
    symlinks: tuple[SymlinkDeclaration, ...]
    allowed_nested_roots: tuple[NestedRootAllowance, ...]
    required_executables: tuple[ExecutableDeclaration, ...]


def _finding(source: Path, pointer: str, code: str, message: str, fix: str) -> ContractFinding:
    return ContractFinding(source=source, pointer=pointer, code=code, message=message, fix=fix)


def _pointer_part(value: object) -> str:
    return str(value).replace("~", "~0").replace("/", "~1")


def _valid_id(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _path(
    value: object,
    *,
    source: Path,
    pointer: str,
    findings: list[ContractFinding],
) -> tuple[str, tuple[str, ...]] | None:
    components = absolute_posix_components(value)
    malformed_wildcard = components is not None and any(
        ("{" in component or "}" in component) and not is_path_identity_segment(component)
        for component in components
    )
    if components is None or malformed_wildcard:
        findings.append(
            _finding(
                source,
                pointer,
                "invalid-posix-path",
                "filesystem path must be absolute POSIX and identity wildcards must occupy one component",
                "use an absolute path without '..', backslashes or partial wildcard components",
            )
        )
        return None
    return cast(str, value), components


def _mapping_section(
    value: object,
    *,
    source: Path,
    pointer: str,
    findings: list[ContractFinding],
) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        findings.append(
            _finding(
                source,
                pointer,
                "invalid-filesystem-section",
                "filesystem section must be a mapping",
                "declare the section as a mapping keyed by stable identifiers",
            )
        )
        return {}
    return cast(Mapping[str, object], value)


def _sequence_section(
    value: object,
    *,
    source: Path,
    pointer: str,
    findings: list[ContractFinding],
) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        findings.append(
            _finding(
                source,
                pointer,
                "invalid-filesystem-section",
                "filesystem section must be a list",
                "declare the section as a list of uniquely identified records",
            )
        )
        return ()
    return cast(Sequence[object], value)


def _unknown_fields(
    record: Mapping[str, object],
    allowed: frozenset[str],
    *,
    source: Path,
    pointer: str,
    findings: list[ContractFinding],
) -> bool:
    unknown = sorted(set(record) - allowed)
    if not unknown:
        return False
    findings.append(
        _finding(
            source,
            pointer,
            "unknown-filesystem-field",
            f"filesystem declaration contains unknown fields: {', '.join(unknown)}",
            "remove unknown fields or use the versioned runtime-contract schema",
        )
    )
    return True


def _record_id(
    record: object,
    *,
    source: Path,
    pointer: str,
    seen: set[str],
    findings: list[ContractFinding],
) -> tuple[str, Mapping[str, object]] | None:
    if not isinstance(record, Mapping) or not _valid_id(record.get("id")):
        findings.append(
            _finding(
                source,
                pointer,
                "invalid-filesystem-record",
                "filesystem record requires a non-empty string id",
                "declare a mapping with a stable non-empty id",
            )
        )
        return None
    identifier = cast(str, record["id"])
    if identifier in seen:
        findings.append(
            _finding(
                source,
                f"{pointer}/id",
                "duplicate-filesystem-id",
                f"filesystem id {identifier!r} is declared more than once",
                "keep each filesystem id exactly once",
            )
        )
        return None
    seen.add(identifier)
    return identifier, cast(Mapping[str, object], record)


def _parse_namespaces(
    filesystem: Mapping[str, object], source: Path, findings: list[ContractFinding]
) -> tuple[NamespaceDeclaration, ...]:
    records = _mapping_section(
        filesystem.get("namespaces"), source=source, pointer="/filesystem/namespaces", findings=findings
    )
    parsed: list[NamespaceDeclaration] = []
    for identifier, raw in records.items():
        pointer = f"/filesystem/namespaces/{_pointer_part(identifier)}"
        if not _valid_id(identifier) or not isinstance(raw, Mapping):
            findings.append(
                _finding(
                    source,
                    pointer,
                    "invalid-namespace",
                    "namespace requires a non-empty name and mapping declaration",
                    "declare kind and root for the named namespace",
                )
            )
            continue
        _unknown_fields(
            raw,
            frozenset({"kind", "root", "physical_namespace"}),
            source=source,
            pointer=pointer,
            findings=findings,
        )
        kind = raw.get("kind")
        root = _path(raw.get("root"), source=source, pointer=f"{pointer}/root", findings=findings)
        physical_namespace = raw.get("physical_namespace", identifier)
        if not isinstance(kind, str) or kind not in _NAMESPACE_KINDS:
            findings.append(
                _finding(
                    source,
                    f"{pointer}/kind",
                    "invalid-namespace-kind",
                    "namespace kind must be host, container or profile",
                    "set kind to the runtime boundary represented by this namespace",
                )
            )
        if not _valid_id(physical_namespace):
            findings.append(
                _finding(
                    source,
                    f"{pointer}/physical_namespace",
                    "invalid-physical-namespace",
                    "physical_namespace must name one declared namespace",
                    "reference the namespace that owns this physical filesystem",
                )
            )
        if (
            root is not None
            and isinstance(kind, str)
            and kind in _NAMESPACE_KINDS
            and _valid_id(physical_namespace)
        ):
            parsed.append(
                NamespaceDeclaration(
                    identifier,
                    kind,
                    root[0],
                    root[1],
                    cast(str, physical_namespace),
                )
            )

    by_id = {item.id: item for item in parsed}
    normalised: list[NamespaceDeclaration] = []
    for item in parsed:
        current = item.id
        visited: set[str] = set()
        representative = item.id
        while True:
            if current in visited:
                findings.append(
                    _finding(
                        source,
                        f"/filesystem/namespaces/{_pointer_part(item.id)}/physical_namespace",
                        "physical-namespace-cycle",
                        f"physical namespace chain for {item.id!r} is cyclic",
                        "point each shared namespace at one acyclic physical namespace owner",
                    )
                )
                break
            visited.add(current)
            declaration = by_id.get(current)
            if declaration is None:
                findings.append(
                    _finding(
                        source,
                        f"/filesystem/namespaces/{_pointer_part(item.id)}/physical_namespace",
                        "undefined-physical-namespace",
                        f"namespace {item.id!r} references undefined physical namespace {current!r}",
                        "reference one declared namespace as the physical filesystem owner",
                    )
                )
                break
            target = declaration.physical_namespace
            if target == current:
                representative = current
                break
            current = target
        normalised.append(
            NamespaceDeclaration(item.id, item.kind, item.root, item.components, representative)
        )
    return tuple(normalised)


def _access_requirement(
    value: object,
    *,
    source: Path,
    pointer: str,
    findings: list[ContractFinding],
) -> AccessRequirement | None:
    if not isinstance(value, Mapping) or set(value) != {"uid", "gids", "read", "write", "traverse"}:
        findings.append(
            _finding(
                source,
                pointer,
                "invalid-root-access",
                "root access must contain exactly uid, gids, read, write and traverse",
                "record the runtime identity and each required effective access result",
            )
        )
        return None
    uid = value.get("uid")
    gids = value.get("gids")
    access_flags = tuple(value.get(field) for field in ("read", "write", "traverse"))
    if (
        not is_integer_identity(uid)
        or not isinstance(gids, Sequence)
        or isinstance(gids, (str, bytes))
        or any(not is_integer_identity(gid) for gid in gids)
        or list(gids) != sorted(set(cast(Sequence[int], gids)))
        or any(type(flag) is not bool for flag in access_flags)
    ):
        findings.append(
            _finding(
                source,
                pointer,
                "invalid-root-access",
                "root access requires a numeric uid, sorted unique numeric gids, and boolean read/write/traverse fields",
                "record the exact runtime identity and effective access as canonical JSON values",
            )
        )
        return None
    return AccessRequirement(
        cast(int, uid),
        tuple(cast(Sequence[int], gids)),
        cast(bool, access_flags[0]),
        cast(bool, access_flags[1]),
        cast(bool, access_flags[2]),
    )


def _parse_roots(
    filesystem: Mapping[str, object],
    namespaces: Mapping[str, NamespaceDeclaration],
    source: Path,
    findings: list[ContractFinding],
) -> tuple[RootDeclaration, ...]:
    records = _mapping_section(
        filesystem.get("roots"), source=source, pointer="/filesystem/roots", findings=findings
    )
    parsed: list[RootDeclaration] = []
    for identifier, raw in records.items():
        pointer = f"/filesystem/roots/{_pointer_part(identifier)}"
        if not _valid_id(identifier) or not isinstance(raw, Mapping):
            findings.append(
                _finding(
                    source,
                    pointer,
                    "invalid-root",
                    "root requires a non-empty name and mapping declaration",
                    "declare namespace, path, kind and lifecycle for the named root",
                )
            )
            continue
        _unknown_fields(
            raw,
            frozenset({"namespace", "path", "kind", "lifecycle", "owner_uid", "owner_gid", "mode", "access"}),
            source=source,
            pointer=pointer,
            findings=findings,
        )
        namespace = raw.get("namespace")
        path = _path(raw.get("path"), source=source, pointer=f"{pointer}/path", findings=findings)
        kind = raw.get("kind")
        lifecycle = raw.get("lifecycle")
        owner_uid = raw.get("owner_uid")
        owner_gid = raw.get("owner_gid")
        mode = raw.get("mode")
        access = _access_requirement(
            raw.get("access"), source=source, pointer=f"{pointer}/access", findings=findings
        )
        if not isinstance(namespace, str) or namespace not in namespaces:
            findings.append(
                _finding(
                    source,
                    f"{pointer}/namespace",
                    "undefined-namespace",
                    f"root references undefined namespace {namespace!r}",
                    "reference one declared filesystem namespace",
                )
            )
        if not isinstance(kind, str) or kind not in _ROOT_KINDS:
            findings.append(
                _finding(
                    source,
                    f"{pointer}/kind",
                    "invalid-root-kind",
                    "root kind must be directory or file",
                    "set kind to the filesystem object the root identifies",
                )
            )
        if not _valid_id(lifecycle):
            findings.append(
                _finding(
                    source,
                    f"{pointer}/lifecycle",
                    "invalid-lifecycle",
                    "root lifecycle must be a non-empty string",
                    "name the root's lifecycle classification",
                )
            )
        if not is_integer_identity(owner_uid):
            findings.append(
                _finding(
                    source,
                    f"{pointer}/owner_uid",
                    "invalid-root-owner-uid",
                    "root owner_uid must be a non-negative integer, not a boolean",
                    "record the expected numeric owner UID",
                )
            )
        if not is_integer_identity(owner_gid):
            findings.append(
                _finding(
                    source,
                    f"{pointer}/owner_gid",
                    "invalid-root-owner-gid",
                    "root owner_gid must be a non-negative integer, not a boolean",
                    "record the expected numeric owner GID",
                )
            )
        if type(mode) is not int or not 0 <= mode <= 0o7777:
            findings.append(
                _finding(
                    source,
                    f"{pointer}/mode",
                    "invalid-root-mode",
                    "root mode must be an integer between 0 and 0o7777, not a boolean",
                    "record the expected POSIX mode as a bounded integer",
                )
            )
        if path is not None and isinstance(namespace, str) and namespace in namespaces:
            boundary = namespaces[namespace]
            if not is_component_pattern_prefix(boundary.components, path[1]):
                findings.append(
                    _finding(
                        source,
                        f"{pointer}/path",
                        "namespace-escape",
                        f"root path {path[0]!r} escapes namespace {namespace!r} root {boundary.root!r}",
                        "move the path beneath its declared namespace root",
                    )
                )
        if (
            path is not None
            and isinstance(namespace, str)
            and namespace in namespaces
            and isinstance(kind, str)
            and kind in _ROOT_KINDS
            and _valid_id(lifecycle)
            and is_integer_identity(owner_uid)
            and is_integer_identity(owner_gid)
            and type(mode) is int
            and 0 <= mode <= 0o7777
            and access is not None
        ):
            parsed.append(
                RootDeclaration(
                    identifier,
                    namespace,
                    path[0],
                    path[1],
                    kind,
                    cast(str, lifecycle),
                    cast(int, owner_uid),
                    cast(int, owner_gid),
                    mode,
                    access,
                )
            )
    return tuple(parsed)


def _parse_mounts(
    filesystem: Mapping[str, object],
    namespaces: Mapping[str, NamespaceDeclaration],
    roots: Mapping[str, RootDeclaration],
    source: Path,
    findings: list[ContractFinding],
) -> tuple[MountDeclaration, ...]:
    records = _sequence_section(
        filesystem.get("mounts"), source=source, pointer="/filesystem/mounts", findings=findings
    )
    parsed: list[MountDeclaration] = []
    seen: set[str] = set()
    destinations: list[tuple[str, tuple[str, ...]]] = []
    for index, raw in enumerate(records):
        pointer = f"/filesystem/mounts/{index}"
        identified = _record_id(raw, source=source, pointer=pointer, seen=seen, findings=findings)
        if identified is None:
            continue
        identifier, record = identified
        _unknown_fields(
            record,
            frozenset({"id", "source_root", "target_namespace", "target_path", "mode"}),
            source=source,
            pointer=pointer,
            findings=findings,
        )
        source_root = record.get("source_root")
        namespace = record.get("target_namespace")
        target = _path(
            record.get("target_path"), source=source, pointer=f"{pointer}/target_path", findings=findings
        )
        mode = record.get("mode")
        valid = True
        if not isinstance(source_root, str) or source_root not in roots:
            valid = False
            findings.append(
                _finding(
                    source,
                    f"{pointer}/source_root",
                    "undefined-root",
                    f"mount references undefined source root {source_root!r}",
                    "reference one declared filesystem root",
                )
            )
        if not isinstance(namespace, str) or namespace not in namespaces:
            valid = False
            findings.append(
                _finding(
                    source,
                    f"{pointer}/target_namespace",
                    "undefined-namespace",
                    f"mount references undefined target namespace {namespace!r}",
                    "reference one declared filesystem namespace",
                )
            )
        if not isinstance(mode, str) or mode not in _MOUNT_MODES:
            valid = False
            findings.append(
                _finding(
                    source,
                    f"{pointer}/mode",
                    "invalid-mount-mode",
                    "mount mode must be ro or rw",
                    "declare the mount's effective read-only or read-write mode",
                )
            )
        if target is not None and isinstance(namespace, str) and namespace in namespaces:
            boundary = namespaces[namespace]
            if not is_component_pattern_prefix(boundary.components, target[1]):
                valid = False
                findings.append(
                    _finding(
                        source,
                        f"{pointer}/target_path",
                        "namespace-escape",
                        f"mount target {target[0]!r} escapes namespace {namespace!r} root {boundary.root!r}",
                        "move the mount target beneath its declared namespace root",
                    )
                )
            physical_namespace = boundary.physical_namespace
            destination = (physical_namespace, target[1])
            if any(
                existing_namespace == physical_namespace
                and len(existing_components) == len(target[1])
                and component_pattern_paths_overlap(existing_components, target[1])
                for existing_namespace, existing_components in destinations
            ):
                valid = False
                findings.append(
                    _finding(
                        source,
                        f"{pointer}/target_path",
                        "duplicate-mount-destination",
                        f"mount destination {target[0]!r} is declared more than once in namespace {namespace!r}",
                        "keep exactly one mount for each namespace destination",
                    )
                )
            destinations.append(destination)
        if valid and target is not None:
            parsed.append(
                MountDeclaration(
                    identifier,
                    cast(str, source_root),
                    cast(str, namespace),
                    target[0],
                    target[1],
                    cast(str, mode),
                )
            )
    return tuple(parsed)


def _parse_aliases(
    filesystem: Mapping[str, object],
    namespaces: Mapping[str, NamespaceDeclaration],
    roots: Mapping[str, RootDeclaration],
    source: Path,
    findings: list[ContractFinding],
) -> tuple[AliasDeclaration, ...]:
    records = _sequence_section(
        filesystem.get("aliases"), source=source, pointer="/filesystem/aliases", findings=findings
    )
    parsed: list[AliasDeclaration] = []
    seen: set[str] = set()
    destinations: set[tuple[str, tuple[str, ...]]] = set()
    for index, raw in enumerate(records):
        pointer = f"/filesystem/aliases/{index}"
        identified = _record_id(raw, source=source, pointer=pointer, seen=seen, findings=findings)
        if identified is None:
            continue
        identifier, record = identified
        _unknown_fields(
            record,
            frozenset({"id", "root", "namespace", "path"}),
            source=source,
            pointer=pointer,
            findings=findings,
        )
        root_id = record.get("root")
        namespace = record.get("namespace")
        path = _path(record.get("path"), source=source, pointer=f"{pointer}/path", findings=findings)
        valid = True
        root = roots.get(root_id) if isinstance(root_id, str) else None
        if root is None:
            valid = False
            findings.append(
                _finding(
                    source,
                    f"{pointer}/root",
                    "undefined-root",
                    f"alias references undefined root {root_id!r}",
                    "reference one declared canonical root",
                )
            )
        if not isinstance(namespace, str) or namespace not in namespaces:
            valid = False
            findings.append(
                _finding(
                    source,
                    f"{pointer}/namespace",
                    "undefined-namespace",
                    f"alias references undefined namespace {namespace!r}",
                    "reference one declared filesystem namespace",
                )
            )
        if (
            root is not None
            and path is not None
            and (namespace != root.namespace or path[1] != root.components)
        ):
            valid = False
            findings.append(
                _finding(
                    source,
                    pointer,
                    "alias-disagreement",
                    f"alias {identifier!r} does not identify canonical root {root.id!r}",
                    "set alias namespace and path exactly to the canonical root",
                )
            )
        if path is not None and isinstance(namespace, str):
            destination = (namespace, path[1])
            if destination in destinations:
                valid = False
                findings.append(
                    _finding(
                        source,
                        f"{pointer}/path",
                        "duplicate-alias-destination",
                        f"alias destination {path[0]!r} is declared more than once",
                        "keep one alias for each namespace path",
                    )
                )
            destinations.add(destination)
        if valid and path is not None:
            parsed.append(
                AliasDeclaration(identifier, cast(str, root_id), cast(str, namespace), path[0], path[1])
            )
    return tuple(parsed)


def _parse_symlinks(
    filesystem: Mapping[str, object],
    namespaces: Mapping[str, NamespaceDeclaration],
    source: Path,
    findings: list[ContractFinding],
) -> tuple[SymlinkDeclaration, ...]:
    records = _sequence_section(
        filesystem.get("symlinks"), source=source, pointer="/filesystem/symlinks", findings=findings
    )
    if len(records) > _MAX_SYMLINK_DECLARATIONS:
        findings.append(
            _finding(
                source,
                "/filesystem/symlinks",
                "filesystem-work-limit",
                f"symlink declarations exceed the {_MAX_SYMLINK_DECLARATIONS}-record validation limit",
                "split the runtime boundary or reduce its declared symlink surface",
            )
        )
        return ()
    parsed: list[SymlinkDeclaration] = []
    seen: set[str] = set()
    sources: list[tuple[str, tuple[str, ...]]] = []
    for index, raw in enumerate(records):
        pointer = f"/filesystem/symlinks/{index}"
        identified = _record_id(raw, source=source, pointer=pointer, seen=seen, findings=findings)
        if identified is None:
            continue
        identifier, record = identified
        _unknown_fields(
            record,
            frozenset({"id", "namespace", "path", "target"}),
            source=source,
            pointer=pointer,
            findings=findings,
        )
        namespace = record.get("namespace")
        path = _path(record.get("path"), source=source, pointer=f"{pointer}/path", findings=findings)
        target = _path(record.get("target"), source=source, pointer=f"{pointer}/target", findings=findings)
        valid = True
        boundary = namespaces.get(namespace) if isinstance(namespace, str) else None
        if boundary is None:
            valid = False
            findings.append(
                _finding(
                    source,
                    f"{pointer}/namespace",
                    "undefined-namespace",
                    f"symlink references undefined namespace {namespace!r}",
                    "reference one declared filesystem namespace",
                )
            )
        for field, parsed_path in (("path", path), ("target", target)):
            if (
                boundary is not None
                and parsed_path is not None
                and not is_component_pattern_prefix(boundary.components, parsed_path[1])
            ):
                valid = False
                findings.append(
                    _finding(
                        source,
                        f"{pointer}/{field}",
                        "symlink-escape",
                        f"symlink {field} {parsed_path[0]!r} escapes namespace root {boundary.root!r}",
                        "keep both symlink path and target inside their declared namespace",
                    )
                )
        if path is not None and boundary is not None:
            physical_namespace = boundary.physical_namespace
            source_key = (physical_namespace, path[1])
            if any(
                existing_namespace == physical_namespace
                and len(existing_components) == len(path[1])
                and component_pattern_paths_overlap(existing_components, path[1])
                for existing_namespace, existing_components in sources
            ):
                valid = False
                findings.append(
                    _finding(
                        source,
                        f"{pointer}/path",
                        "duplicate-symlink-source",
                        f"symlink source {path[0]!r} is declared more than once",
                        "keep one symlink declaration for each source path",
                    )
                )
            sources.append(source_key)
        if valid and path is not None and target is not None:
            parsed.append(
                SymlinkDeclaration(
                    identifier,
                    cast(str, namespace),
                    path[0],
                    path[1],
                    target[0],
                    target[1],
                )
            )
    return tuple(parsed)


def _parse_allowances(
    filesystem: Mapping[str, object],
    roots: Mapping[str, RootDeclaration],
    source: Path,
    findings: list[ContractFinding],
) -> tuple[NestedRootAllowance, ...]:
    records = _sequence_section(
        filesystem.get("allowed_nested_roots"),
        source=source,
        pointer="/filesystem/allowed_nested_roots",
        findings=findings,
    )
    parsed: list[NestedRootAllowance] = []
    seen: set[tuple[str, str]] = set()
    for index, raw in enumerate(records):
        pointer = f"/filesystem/allowed_nested_roots/{index}"
        if not isinstance(raw, Mapping):
            findings.append(
                _finding(
                    source,
                    pointer,
                    "invalid-nested-root-allowance",
                    "nested-root allowance must be a mapping",
                    "declare parent, child and a non-empty reason",
                )
            )
            continue
        _unknown_fields(
            raw,
            frozenset({"parent", "child", "reason"}),
            source=source,
            pointer=pointer,
            findings=findings,
        )
        parent_id = raw.get("parent")
        child_id = raw.get("child")
        reason = raw.get("reason")
        parent = roots.get(parent_id) if isinstance(parent_id, str) else None
        child = roots.get(child_id) if isinstance(child_id, str) else None
        valid = True
        if parent is None or child is None:
            valid = False
            findings.append(
                _finding(
                    source,
                    pointer,
                    "undefined-root",
                    "nested-root allowance references an undefined parent or child root",
                    "reference two declared roots",
                )
            )
        if not _valid_id(reason):
            valid = False
            findings.append(
                _finding(
                    source,
                    f"{pointer}/reason",
                    "missing-overlap-reason",
                    "intentional nested roots require a named reason",
                    "state why this exact parent and child overlap is required",
                )
            )
        pair = (str(parent_id), str(child_id))
        if pair in seen:
            valid = False
            findings.append(
                _finding(
                    source,
                    pointer,
                    "duplicate-nested-root-allowance",
                    "nested-root allowance is declared more than once",
                    "keep one reasoned allowance for the root pair",
                )
            )
        seen.add(pair)
        if (
            parent is not None
            and child is not None
            and (
                len(parent.components) >= len(child.components)
                or not is_component_pattern_prefix(parent.components, child.components)
            )
        ):
            valid = False
            findings.append(
                _finding(
                    source,
                    pointer,
                    "invalid-nested-root-allowance",
                    "allowance parent does not physically contain its child",
                    "remove the allowance or name the actual parent and child roots",
                )
            )
        if valid:
            parsed.append(NestedRootAllowance(cast(str, parent_id), cast(str, child_id), cast(str, reason)))
    return tuple(parsed)


def _parse_executables(
    filesystem: Mapping[str, object],
    namespaces: Mapping[str, NamespaceDeclaration],
    source: Path,
    findings: list[ContractFinding],
) -> tuple[ExecutableDeclaration, ...]:
    records = _sequence_section(
        filesystem.get("required_executables"),
        source=source,
        pointer="/filesystem/required_executables",
        findings=findings,
    )
    parsed: list[ExecutableDeclaration] = []
    seen: set[str] = set()
    destinations: list[tuple[str, tuple[str, ...]]] = []
    for index, raw in enumerate(records):
        pointer = f"/filesystem/required_executables/{index}"
        identified = _record_id(raw, source=source, pointer=pointer, seen=seen, findings=findings)
        if identified is None:
            continue
        identifier, record = identified
        _unknown_fields(
            record,
            frozenset({"id", "namespace", "path"}),
            source=source,
            pointer=pointer,
            findings=findings,
        )
        namespace = record.get("namespace")
        path = _path(record.get("path"), source=source, pointer=f"{pointer}/path", findings=findings)
        valid = True
        boundary = namespaces.get(namespace) if isinstance(namespace, str) else None
        if boundary is None:
            valid = False
            findings.append(
                _finding(
                    source,
                    f"{pointer}/namespace",
                    "undefined-namespace",
                    f"executable references undefined namespace {namespace!r}",
                    "reference one declared filesystem namespace",
                )
            )
        if (
            boundary is not None
            and path is not None
            and not is_component_pattern_prefix(boundary.components, path[1])
        ):
            valid = False
            findings.append(
                _finding(
                    source,
                    f"{pointer}/path",
                    "namespace-escape",
                    f"executable path {path[0]!r} escapes namespace root {boundary.root!r}",
                    "move the executable beneath its declared namespace root",
                )
            )
        if path is not None and boundary is not None:
            physical_namespace = boundary.physical_namespace
            destination = (physical_namespace, path[1])
            if any(
                existing_namespace == physical_namespace
                and len(existing_components) == len(path[1])
                and component_pattern_paths_overlap(existing_components, path[1])
                for existing_namespace, existing_components in destinations
            ):
                valid = False
                findings.append(
                    _finding(
                        source,
                        f"{pointer}/path",
                        "duplicate-executable",
                        f"required executable {path[0]!r} is declared more than once",
                        "keep one declaration for each required executable path",
                    )
                )
            destinations.append(destination)
        if valid and path is not None:
            parsed.append(ExecutableDeclaration(identifier, cast(str, namespace), path[0], path[1]))
    return tuple(parsed)


def _root_overlap_findings(contract: _FilesystemDeclarations, *, source: Path) -> list[ContractFinding]:
    findings: list[ContractFinding] = []
    allowed = {(item.parent, item.child) for item in contract.allowed_nested_roots}
    physical_namespaces = {item.id: item.physical_namespace for item in contract.namespaces}
    for left, right in combinations(contract.roots, 2):
        if physical_namespaces[left.namespace] != physical_namespaces[right.namespace]:
            continue
        if not component_pattern_paths_overlap(left.components, right.components):
            continue
        if len(left.components) == len(right.components):
            findings.append(
                _finding(
                    source,
                    "/filesystem/roots",
                    "duplicate-root-path",
                    f"roots {left.id!r} and {right.id!r} can resolve to the same physical path",
                    "keep one canonical root or make the physical paths disjoint",
                )
            )
            continue
        parent, child = (left, right) if len(left.components) < len(right.components) else (right, left)
        if parent.kind == "file":
            findings.append(
                _finding(
                    source,
                    f"/filesystem/roots/{_pointer_part(parent.id)}",
                    "file-root-contains-path",
                    f"file root {parent.path!r} cannot contain nested root {child.path!r}",
                    "declare the parent as a directory or move the child root",
                )
            )
        elif (parent.id, child.id) not in allowed:
            findings.append(
                _finding(
                    source,
                    "/filesystem/allowed_nested_roots",
                    "nested-root-overlap",
                    f"root {parent.path!r} physically contains {child.path!r} without a named allowance",
                    "add an allowance naming this exact parent and child with a non-empty reason",
                )
            )
    return findings


def _mount_target_findings(contract: _FilesystemDeclarations, *, source: Path) -> list[ContractFinding]:
    """Reject mount targets below regular-file roots in one physical namespace."""
    physical_namespaces = {item.id: item.physical_namespace for item in contract.namespaces}
    findings: list[ContractFinding] = []
    for mount in contract.mounts:
        target_physical_namespace = physical_namespaces[mount.target_namespace]
        for root in contract.roots:
            if (
                root.kind != "file"
                or physical_namespaces[root.namespace] != target_physical_namespace
                or len(root.components) >= len(mount.target_components)
                or not is_component_pattern_prefix(root.components, mount.target_components)
            ):
                continue
            findings.append(
                _finding(
                    source,
                    f"/filesystem/mounts/{_pointer_part(mount.id)}/target_path",
                    "file-root-contains-path",
                    f"file root {root.path!r} cannot contain mount target {mount.target_path!r}",
                    "move the mount target outside the file root or declare a directory root",
                )
            )
    return findings


@dataclass(frozen=True)
class _SymlinkResolutionState:
    path: int
    bindings: PathPatternBindings


class _SymlinkWorkLimit(Exception):
    """A deterministic resolver resource limit was reached before allocation."""


class _SymlinkPaths:
    """Intern exact component/tail pairs so DFS states share their path suffixes.

    Node zero is the empty absolute path. A node's integer identity represents
    its complete path exactly, without relying on a lossy hash for cycle checks.
    Component work counts prefix materialisation, binding and interning passes;
    counters and the node table are shared by every start in one validation.
    """

    def __init__(self) -> None:
        self._nodes: list[tuple[str, int, int]] = [("", 0, 0)]
        self._index: dict[tuple[str, int], int] = {}
        self._states = 0
        self._component_work = 0

    def length(self, path: int) -> int:
        return self._nodes[path][2]

    def check_length(self, length: int) -> None:
        if length > _MAX_SYMLINK_PATH_COMPONENTS:
            raise _SymlinkWorkLimit(
                f"symlink resolution exceeded its {_MAX_SYMLINK_PATH_COMPONENTS}-component path limit"
            )

    def charge_work(self, components: int) -> None:
        if components > _MAX_SYMLINK_COMPONENT_WORK - self._component_work:
            raise _SymlinkWorkLimit(
                f"symlink resolution exceeded its {_MAX_SYMLINK_COMPONENT_WORK}-component work budget"
            )
        self._component_work += components

    def prepend(self, components: tuple[str, ...], suffix: int = 0) -> int:
        self.check_length(len(components) + self.length(suffix))
        self.charge_work(len(components))
        for component in reversed(components):
            key = (component, suffix)
            node = self._index.get(key)
            if node is None:
                if len(self._nodes) - 1 >= _MAX_SYMLINK_PATH_NODES:
                    raise _SymlinkWorkLimit(
                        f"symlink resolution exceeded its {_MAX_SYMLINK_PATH_NODES}-node retained-path budget"
                    )
                node = len(self._nodes)
                self._nodes.append((component, suffix, self.length(suffix) + 1))
                self._index[key] = node
            suffix = node
        return suffix

    def split(self, path: int, length: int) -> tuple[tuple[str, ...], int] | None:
        if length > self.length(path):
            return None
        self.charge_work(length)
        components: list[str] = []
        for _ in range(length):
            component, path, _ = self._nodes[path]
            components.append(component)
        return tuple(components), path

    def bind(self, path: int, bindings: PathPatternBindings) -> int:
        split = self.split(path, self.length(path))
        if split is None:
            raise ValueError("a path must contain its own length")
        self.charge_work(len(split[0]))
        return self.prepend(bindings.resolve_path(split[0]))

    def state(
        self, components: tuple[str, ...], suffix: int, bindings: PathPatternBindings
    ) -> _SymlinkResolutionState:
        self.check_length(len(components) + self.length(suffix))
        if self._states >= _MAX_SYMLINK_RESOLUTION_STATES:
            raise _SymlinkWorkLimit(
                f"symlink resolution exceeded its {_MAX_SYMLINK_RESOLUTION_STATES}-state budget"
            )
        self._states += 1
        return _SymlinkResolutionState(self.prepend(components, suffix), bindings)


def _shorter_symlink_covers_branch(
    prefix: tuple[str, ...],
    bindings: PathPatternBindings,
    candidates: Sequence[SymlinkDeclaration],
    paths: _SymlinkPaths,
) -> bool:
    for shorter in candidates:
        if len(shorter.components) >= len(prefix):
            continue
        paths.charge_work(len(shorter.components))
        if bindings.match_prefix(shorter.components, prefix) == bindings:
            return True
    return False


def _symlink_successors(
    state: _SymlinkResolutionState, candidates: Sequence[SymlinkDeclaration], paths: _SymlinkPaths
) -> list[_SymlinkResolutionState]:
    successors: list[_SymlinkResolutionState] = []
    for candidate in candidates:
        split = paths.split(state.path, len(candidate.components))
        if split is None:
            continue
        prefix, suffix = split
        matched = state.bindings.match_prefix(candidate.components, prefix)
        if matched is None:
            continue
        # A shorter source wins only if it matches this entire binding branch.
        # Partial matches leave other identities free to use the longer source.
        if _shorter_symlink_covers_branch(prefix, matched, candidates, paths):
            continue
        paths.check_length(len(candidate.target_components) + paths.length(suffix))
        paths.charge_work(len(candidate.target_components))
        target = matched.resolve_path(candidate.target_components)
        if matched != state.bindings:
            suffix = paths.bind(suffix, matched)
        successors.append(paths.state(target, suffix, matched))
    return successors


def _symlink_is_cyclic(
    start: SymlinkDeclaration, candidates: Sequence[SymlinkDeclaration], paths: _SymlinkPaths
) -> bool:
    pending = [(paths.state(start.target_components, 0, PathPatternBindings()), True)]
    active: set[_SymlinkResolutionState] = set()
    while pending:
        state, entering = pending.pop()
        if not entering:
            active.remove(state)
            continue
        if state in active:
            return True
        active.add(state)
        pending.append((state, False))
        pending.extend((successor, True) for successor in _symlink_successors(state, candidates, paths))
    return False


def _symlink_cycle_findings(contract: _FilesystemDeclarations, *, source: Path) -> list[ContractFinding]:
    physical_namespaces = {item.id: item.physical_namespace for item in contract.namespaces}
    links_by_namespace: dict[str, list[SymlinkDeclaration]] = {}
    for item in contract.symlinks:
        physical_namespace = physical_namespaces[item.namespace]
        links_by_namespace.setdefault(physical_namespace, []).append(item)

    findings: list[ContractFinding] = []
    paths = _SymlinkPaths()
    for start in contract.symlinks:
        physical_namespace = physical_namespaces[start.namespace]
        candidates = links_by_namespace[physical_namespace]
        try:
            cyclic = _symlink_is_cyclic(start, candidates, paths)
        except _SymlinkWorkLimit as error:
            findings.append(
                _finding(
                    source,
                    "/filesystem/symlinks",
                    "filesystem-work-limit",
                    str(error),
                    "reduce path size, ambiguous wildcard matches or chained symlink declarations",
                )
            )
            break
        if cyclic:
            findings.append(
                _finding(
                    source,
                    "/filesystem/symlinks",
                    "symlink-cycle",
                    f"symlink chain beginning at {start.path!r} does not terminate",
                    "point the symlink chain at a non-symlink target inside the namespace",
                )
            )
    return findings


def _symlink_target_findings(contract: _FilesystemDeclarations, *, source: Path) -> list[ContractFinding]:
    physical_namespaces = {item.id: item.physical_namespace for item in contract.namespaces}
    declared_targets = [
        *((physical_namespaces[item.namespace], item.components) for item in contract.roots),
        *((physical_namespaces[item.namespace], item.components) for item in contract.aliases),
        *((physical_namespaces[item.namespace], item.components) for item in contract.symlinks),
    ]
    return [
        _finding(
            source,
            f"/filesystem/symlinks/{_pointer_part(item.id)}/target",
            "undefined-symlink-target",
            f"symlink target {item.target!r} is not a declared root, alias or symlink source",
            "declare the target path in this namespace or correct the symlink target",
        )
        for item in contract.symlinks
        if not any(
            target_namespace == physical_namespaces[item.namespace]
            and len(target_components) == len(item.target_components)
            and is_component_pattern_prefix(target_components, item.target_components)
            for target_namespace, target_components in declared_targets
        )
    ]


def _parse_contract(
    documents: ContractDocuments,
) -> tuple[_FilesystemDeclarations | None, tuple[ContractFinding, ...]]:
    source = documents.contract_path
    filesystem_value = documents.contract.get("filesystem")
    if not isinstance(filesystem_value, Mapping):
        return None, (
            _finding(
                source,
                "/filesystem",
                "missing-filesystem-contract",
                "selected runtime contract requires a filesystem mapping",
                "declare namespaces, roots, mounts, aliases, symlinks and required executables",
            ),
        )
    filesystem = cast(Mapping[str, object], filesystem_value)
    findings: list[ContractFinding] = []
    _unknown_fields(
        filesystem,
        frozenset(
            {
                "namespaces",
                "roots",
                "mounts",
                "aliases",
                "symlinks",
                "allowed_nested_roots",
                "required_executables",
            }
        ),
        source=source,
        pointer="/filesystem",
        findings=findings,
    )
    namespaces = _parse_namespaces(filesystem, source, findings)
    namespace_map = {item.id: item for item in namespaces}
    roots = _parse_roots(filesystem, namespace_map, source, findings)
    root_map = {item.id: item for item in roots}
    mounts = _parse_mounts(filesystem, namespace_map, root_map, source, findings)
    aliases = _parse_aliases(filesystem, namespace_map, root_map, source, findings)
    symlinks = _parse_symlinks(filesystem, namespace_map, source, findings)
    allowances = _parse_allowances(filesystem, root_map, source, findings)
    executables = _parse_executables(filesystem, namespace_map, source, findings)
    contract = _FilesystemDeclarations(
        namespaces,
        roots,
        mounts,
        aliases,
        symlinks,
        allowances,
        executables,
    )
    findings.extend(_root_overlap_findings(contract, source=source))
    findings.extend(_mount_target_findings(contract, source=source))
    findings.extend(_symlink_target_findings(contract, source=source))
    findings.extend(_symlink_cycle_findings(contract, source=source))
    return contract, sort_findings(findings)


def _observation_records(
    value: object,
    *,
    source: Path,
    pointer: str,
    kind: str,
) -> tuple[dict[str, Mapping[str, object]], list[ContractFinding]]:
    findings: list[ContractFinding] = []
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return {}, [
            _finding(
                source,
                pointer,
                f"missing-{kind}-observations",
                f"filesystem evidence requires a {kind} observation list",
                f"collect one complete observation for every declared {kind}",
            )
        ]
    records: dict[str, Mapping[str, object]] = {}
    for index, raw in enumerate(value):
        record_pointer = f"{pointer}/{index}"
        if not isinstance(raw, Mapping) or not _valid_id(raw.get("id")):
            findings.append(
                _finding(
                    source,
                    record_pointer,
                    f"invalid-{kind}-observation",
                    f"{kind} observation requires a non-empty id",
                    "record the declared id and all required observed fields",
                )
            )
            continue
        identifier = cast(str, raw["id"])
        if identifier in records:
            findings.append(
                _finding(
                    source,
                    f"{record_pointer}/id",
                    f"duplicate-{kind}-observation",
                    f"{kind} observation {identifier!r} is recorded more than once",
                    "record each declared filesystem item exactly once",
                )
            )
            continue
        records[identifier] = cast(Mapping[str, object], raw)
    return records, findings


def _compare_observations(
    *,
    kind: str,
    collection: str,
    declarations: Mapping[str, Mapping[str, object]],
    observations: object,
    source: Path,
) -> list[ContractFinding]:
    records, findings = _observation_records(
        observations,
        source=source,
        pointer=f"/filesystem/{collection}",
        kind=kind,
    )
    for identifier, expected in declarations.items():
        actual = records.get(identifier)
        if actual is None:
            findings.append(
                _finding(
                    source,
                    f"/filesystem/{collection}",
                    f"missing-{kind}-observation",
                    f"declared {kind} {identifier!r} has no live observation",
                    "collect exactly one complete observation for every declaration",
                )
            )
            continue
        unknown_fields = sorted(set(actual) - set(expected))
        if unknown_fields:
            findings.append(
                _finding(
                    source,
                    f"/filesystem/{collection}/{_pointer_part(identifier)}",
                    f"{kind}-observation-unknown-field",
                    f"live {kind} observation contains unknown fields: {', '.join(unknown_fields)}",
                    "remove fields outside the versioned filesystem observation contract",
                )
            )
        mismatched = [
            field
            for field, value in expected.items()
            if field not in actual
            or actual[field] != value
            or (type(value) is bool and type(actual[field]) is not bool)
        ]
        if mismatched:
            findings.append(
                _finding(
                    source,
                    f"/filesystem/{collection}/{_pointer_part(identifier)}",
                    f"{kind}-observation-mismatch",
                    f"live {kind} observation disagrees on: {', '.join(sorted(mismatched))}",
                    "collect the complete live state and correct the declaration or target",
                )
            )
    for identifier in sorted(set(records) - set(declarations)):
        findings.append(
            _finding(
                source,
                f"/filesystem/{collection}/{_pointer_part(identifier)}",
                f"unexpected-{kind}-observation",
                f"live {kind} observation {identifier!r} has no declaration",
                "remove the observation or add the missing declaration",
            )
        )
    return findings


def _observation_findings(
    contract: _FilesystemDeclarations,
    documents: ContractDocuments,
) -> list[ContractFinding]:
    if documents.evidence is None:
        return []
    source = documents.evidence_path or documents.contract_path
    observed = documents.evidence.get("filesystem")
    if not isinstance(observed, Mapping):
        return [
            _finding(
                source,
                "/filesystem",
                "missing-filesystem-observations",
                "configured evidence requires a filesystem observation mapping",
                "collect roots, mounts, aliases, symlinks and executables from the live target",
            )
        ]
    observations = cast(Mapping[str, object], observed)
    allowed_collections = frozenset({"roots", "mounts", "aliases", "symlinks", "executables"})
    roots = {
        item.id: {
            "id": item.id,
            "namespace": item.namespace,
            "path": item.path,
            "kind": item.kind,
            "lifecycle": item.lifecycle,
            "owner_uid": item.owner_uid,
            "owner_gid": item.owner_gid,
            "mode": item.mode,
            "access": {
                "uid": item.access.uid,
                "gids": list(item.access.gids),
                "read": item.access.read,
                "write": item.access.write,
                "traverse": item.access.traverse,
            },
            "exists": True,
        }
        for item in contract.roots
    }
    mounts = {
        item.id: {
            "id": item.id,
            "source_root": item.source_root,
            "target_namespace": item.target_namespace,
            "target_path": item.target_path,
            "mode": item.mode,
            "mounted": True,
        }
        for item in contract.mounts
    }
    aliases = {
        item.id: {
            "id": item.id,
            "root": item.root,
            "namespace": item.namespace,
            "path": item.path,
            "resolved_path": next(root.path for root in contract.roots if root.id == item.root),
            "exists": True,
        }
        for item in contract.aliases
    }
    symlinks = {
        item.id: {
            "id": item.id,
            "namespace": item.namespace,
            "path": item.path,
            "target": item.target,
            "exists": True,
        }
        for item in contract.symlinks
    }
    executables = {
        item.id: {
            "id": item.id,
            "namespace": item.namespace,
            "path": item.path,
            "exists": True,
            "executable": True,
        }
        for item in contract.required_executables
    }
    findings = [
        _finding(
            source,
            f"/filesystem/{_pointer_part(collection)}",
            "unknown-filesystem-observation-collection",
            f"filesystem evidence contains unknown observation collection {collection!r}",
            "remove collections outside the versioned filesystem evidence contract",
        )
        for collection in sorted(set(observations) - allowed_collections)
    ]
    for kind, declarations in (
        ("root", roots),
        ("mount", mounts),
        ("alias", aliases),
        ("symlink", symlinks),
        ("executable", executables),
    ):
        collection = {
            "root": "roots",
            "mount": "mounts",
            "alias": "aliases",
            "symlink": "symlinks",
            "executable": "executables",
        }[kind]
        findings.extend(
            _compare_observations(
                kind=kind,
                collection=collection,
                declarations=declarations,
                observations=observations.get(collection),
                source=source,
            )
        )
    return findings


def validate_filesystem_contract(documents: ContractDocuments) -> tuple[ContractFinding, ...]:
    """Validate declarations and any explicitly configured live observation."""
    contract, findings = _parse_contract(documents)
    if contract is None:
        return findings
    return sort_findings((*findings, *_observation_findings(contract, documents)))


class RuntimeFilesystemContract(RuntimeContractRule):
    """Opt-in hard-adoption rule for runtime filesystem contracts."""

    name = "runtime-filesystem-contract"
    remediation = REMEDIATION

    def __init__(self, config: Mapping[str, object], *, repo_root: Path | None = None) -> None:
        super().__init__(config, repo_root=repo_root)
        self._evidence_contract = RuntimeEvidenceContract(config, repo_root=repo_root)

    def validate_configuration(self) -> tuple[ContractFinding, ...]:
        if "evidence_file" not in self.config:
            return ()
        return self._evidence_contract.validate_configuration()

    def validate_documents(self, documents: ContractDocuments) -> tuple[ContractFinding, ...]:
        filesystem_findings = validate_filesystem_contract(documents)
        if documents.evidence is None:
            return filesystem_findings
        evidence_findings = validate_runtime_evidence(
            documents,
            expected_identity=self._evidence_contract.expected_identity,
            required_checks=self._evidence_contract.required_checks,
            now=datetime.now(UTC),
            max_age_seconds=self._evidence_contract.max_age_seconds,
        )
        return sort_findings((*filesystem_findings, *evidence_findings))


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> RuntimeFilesystemContract:
    """Bind the CORE filesystem check to a consumer contract configuration."""
    return cast(RuntimeFilesystemContract, RuntimeFilesystemContract.from_config(config, repo_root=repo_root))


def main(argv: list[str] | None = None) -> int:
    """Run one configured filesystem contract directly from the command line."""
    parser = argparse.ArgumentParser(prog=RuntimeFilesystemContract.name)
    parser.add_argument(
        "--establish-baseline",
        action="store_true",
        help="validate the configured contract and reject baseline establishment on any finding",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repository root containing the configured contract (default: current working directory)",
    )
    parser.add_argument(
        "--contract-file", help="repo-relative runtime contract registry or selected contract"
    )
    parser.add_argument("--environment", help="selected environment key")
    parser.add_argument("--target", help="selected target key")
    parser.add_argument("--evidence-file", help="repo-relative runtime evidence receipt")
    parser.add_argument("--expected-source-sha")
    parser.add_argument("--expected-image-digest")
    parser.add_argument("--expected-host-id")
    parser.add_argument("--expected-runtime-user")
    parser.add_argument("--expected-deployment-id")
    parser.add_argument("--expected-configuration-identity")
    parser.add_argument("--expected-run-id", type=int)
    parser.add_argument("--expected-attempt-id", type=int)
    parser.add_argument("--required-check", action="append", default=[])
    parser.add_argument("--max-age-seconds", type=int, default=300)
    args = parser.parse_args(argv)

    config: dict[str, object] = {}
    supplied_selection = (args.environment, args.target)
    if args.contract_file is None:
        if any(supplied_selection) or args.evidence_file is not None:
            parser.error("--environment, --target and --evidence-file require --contract-file")
    else:
        if not all(supplied_selection):
            parser.error("--contract-file requires both --environment and --target")
        config = {
            "contract_file": args.contract_file,
            "environment": args.environment,
            "target": args.target,
        }
        if args.evidence_file is not None:
            config.update(
                {
                    "evidence_file": args.evidence_file,
                    "expected_source_sha": args.expected_source_sha,
                    "expected_image_digest": args.expected_image_digest,
                    "expected_host_id": args.expected_host_id,
                    "expected_runtime_user": args.expected_runtime_user,
                    "expected_deployment_id": args.expected_deployment_id,
                    "expected_configuration_identity": args.expected_configuration_identity,
                    "expected_run_id": args.expected_run_id,
                    "expected_attempt_id": args.expected_attempt_id,
                    "required_checks": args.required_check,
                    "max_age_seconds": args.max_age_seconds,
                }
            )

    rule = RuntimeFilesystemContract.from_config(config, repo_root=args.repo_root)
    if args.establish_baseline:
        path = rule.establish_baseline()
        print(f"established baseline: {path}")
        return 0
    return rule.run()


if __name__ == "__main__":
    import sys

    sys.exit(main())


__all__ = [
    "RuntimeFilesystemContract",
    "build",
    "main",
    "validate_filesystem_contract",
]
