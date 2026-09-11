"""CORE check for component-aware runtime filesystem contracts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any, cast

from tc_fitness.core_checks import run_core_check
from tc_fitness.core_checks._runtime_contracts import (
    ContractDocuments,
    ContractFinding,
    RuntimeContractRule,
    absolute_posix_components,
    component_pattern_paths_overlap,
    is_component_pattern_prefix,
    is_path_identity_segment,
    sort_findings,
)
from tc_fitness.lib import remediation as _remediation

_NAMESPACE_KINDS = frozenset({"host", "container", "profile"})
_ROOT_KINDS = frozenset({"directory", "file"})
_MOUNT_MODES = frozenset({"ro", "rw"})

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


@dataclass(frozen=True)
class RootDeclaration:
    id: str
    namespace: str
    path: str
    components: tuple[str, ...]
    kind: str
    lifecycle: str


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
        _unknown_fields(raw, frozenset({"kind", "root"}), source=source, pointer=pointer, findings=findings)
        kind = raw.get("kind")
        root = _path(raw.get("root"), source=source, pointer=f"{pointer}/root", findings=findings)
        if kind not in _NAMESPACE_KINDS:
            findings.append(
                _finding(
                    source,
                    f"{pointer}/kind",
                    "invalid-namespace-kind",
                    "namespace kind must be host, container or profile",
                    "set kind to the runtime boundary represented by this namespace",
                )
            )
        if root is not None and kind in _NAMESPACE_KINDS:
            parsed.append(NamespaceDeclaration(identifier, cast(str, kind), root[0], root[1]))
    return tuple(parsed)


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
            frozenset({"namespace", "path", "kind", "lifecycle"}),
            source=source,
            pointer=pointer,
            findings=findings,
        )
        namespace = raw.get("namespace")
        path = _path(raw.get("path"), source=source, pointer=f"{pointer}/path", findings=findings)
        kind = raw.get("kind")
        lifecycle = raw.get("lifecycle")
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
        if kind not in _ROOT_KINDS:
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
            and kind in _ROOT_KINDS
            and _valid_id(lifecycle)
        ):
            parsed.append(
                RootDeclaration(
                    identifier,
                    namespace,
                    path[0],
                    path[1],
                    cast(str, kind),
                    cast(str, lifecycle),
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
    destinations: set[tuple[str, tuple[str, ...]]] = set()
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
        if mode not in _MOUNT_MODES:
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
            destination = (namespace, target[1])
            if destination in destinations:
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
            destinations.add(destination)
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
    parsed: list[SymlinkDeclaration] = []
    seen: set[str] = set()
    sources: set[tuple[str, tuple[str, ...]]] = set()
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
        if path is not None and isinstance(namespace, str):
            source_key = (namespace, path[1])
            if source_key in sources:
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
            sources.add(source_key)
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
    destinations: set[tuple[str, tuple[str, ...]]] = set()
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
        if path is not None and isinstance(namespace, str):
            destination = (namespace, path[1])
            if destination in destinations:
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
            destinations.add(destination)
        if valid and path is not None:
            parsed.append(ExecutableDeclaration(identifier, cast(str, namespace), path[0], path[1]))
    return tuple(parsed)


def _root_overlap_findings(contract: _FilesystemDeclarations, *, source: Path) -> list[ContractFinding]:
    findings: list[ContractFinding] = []
    allowed = {(item.parent, item.child) for item in contract.allowed_nested_roots}
    for left, right in combinations(contract.roots, 2):
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


def _symlink_cycle_findings(contract: _FilesystemDeclarations, *, source: Path) -> list[ContractFinding]:
    by_source = {(item.namespace, item.components): item for item in contract.symlinks}
    findings: list[ContractFinding] = []
    reported: set[str] = set()
    for start in contract.symlinks:
        active: set[tuple[str, tuple[str, ...]]] = set()
        current: SymlinkDeclaration | None = start
        while current is not None:
            key = (current.namespace, current.components)
            if key in active:
                if start.id not in reported:
                    findings.append(
                        _finding(
                            source,
                            "/filesystem/symlinks",
                            "symlink-cycle",
                            f"symlink chain beginning at {start.path!r} repeats a source node",
                            "point the symlink chain at a non-symlink target inside the namespace",
                        )
                    )
                    reported.add(start.id)
                break
            active.add(key)
            current = by_source.get((current.namespace, current.target_components))
    return findings


def _symlink_target_findings(contract: _FilesystemDeclarations, *, source: Path) -> list[ContractFinding]:
    declared_targets = {
        *((item.namespace, item.components) for item in contract.roots),
        *((item.namespace, item.components) for item in contract.aliases),
        *((item.namespace, item.components) for item in contract.symlinks),
    }
    return [
        _finding(
            source,
            f"/filesystem/symlinks/{_pointer_part(item.id)}/target",
            "undefined-symlink-target",
            f"symlink target {item.target!r} is not a declared root, alias or symlink source",
            "declare the target path in this namespace or correct the symlink target",
        )
        for item in contract.symlinks
        if (item.namespace, item.target_components) not in declared_targets
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
        mismatched = [field for field, value in expected.items() if actual.get(field) != value]
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
    roots = {
        item.id: {
            "id": item.id,
            "namespace": item.namespace,
            "path": item.path,
            "kind": item.kind,
            "lifecycle": item.lifecycle,
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
    findings: list[ContractFinding] = []
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

    def validate_documents(self, documents: ContractDocuments) -> tuple[ContractFinding, ...]:
        return validate_filesystem_contract(documents)


def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> RuntimeFilesystemContract:
    """Bind the CORE filesystem check to a consumer contract configuration."""
    return cast(RuntimeFilesystemContract, RuntimeFilesystemContract.from_config(config, repo_root=repo_root))


def main(argv: list[str] | None = None) -> int:
    """Run the filesystem contract check through the shared CORE boundary."""
    return run_core_check(RuntimeFilesystemContract, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())


__all__ = [
    "RuntimeFilesystemContract",
    "build",
    "main",
    "validate_filesystem_contract",
]
