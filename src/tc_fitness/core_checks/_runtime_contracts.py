"""Shared strict loading and protocol primitives for runtime contract checks.

The public helpers in this module deliberately use only the standard library
for JSON. YAML remains an optional input format and is imported only when a
consumer selects a ``.yaml`` or ``.yml`` registry.
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, ClassVar, TextIO, cast

from tc_fitness.fitness_rule import FitnessRule

CONTRACT_SCHEMA = "tc-fitness/runtime-contract/v1"
EVIDENCE_SCHEMA = "tc-fitness/runtime-evidence/v1"
_SHA256_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
_PATH_IDENTITY_SEGMENT_RE = re.compile(r"\{[A-Za-z][A-Za-z0-9_-]*\}\Z")
_MAX_DOCUMENT_DEPTH = 100
_MAX_ARRAY_INDEX_TEXT = str(sys.maxsize)

_INTEGER_FIELDS = frozenset(
    {
        "attempt_id",
        "gid",
        "primary_gid",
        "run_id",
        "sequence",
        "supplementary_gid",
        "uid",
    }
)


@dataclass(frozen=True)
class ContractFinding:
    """One deterministic, actionable runtime-contract defect."""

    source: Path
    pointer: str
    code: str
    message: str
    fix: str


@dataclass(frozen=True)
class ContractDocuments:
    """Strictly decoded contract and optional evidence with exact input bytes."""

    contract_path: Path
    contract: Mapping[str, object]
    contract_bytes: bytes
    evidence_path: Path | None
    evidence: Mapping[str, object] | None
    evidence_bytes: bytes | None


class _DuplicateKeyError(ValueError):
    def __init__(self, key: str) -> None:
        super().__init__(key)
        self.key = key


class _InvalidConstantError(ValueError):
    def __init__(self, value: str) -> None:
        super().__init__(value)
        self.value = value


def canonical_json_bytes(value: object) -> bytes:
    """Return UTF-8 canonical JSON bytes suitable for stable SHA-256 hashing."""
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def absolute_posix_components(value: object) -> tuple[str, ...] | None:
    """Return components for a safe absolute POSIX path, excluding the root."""
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        return None
    path = PurePosixPath(value)
    if not path.is_absolute() or ".." in path.parts:
        return None
    return tuple(part for part in path.parts if part != "/")


def is_component_prefix(parent: tuple[str, ...], child: tuple[str, ...]) -> bool:
    """Return whether ``parent`` contains ``child`` using path components."""
    return len(parent) <= len(child) and child[: len(parent)] == parent


def component_paths_overlap(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    """Return whether either absolute path contains the other."""
    return is_component_prefix(left, right) or is_component_prefix(right, left)


def is_path_identity_segment(component: str) -> bool:
    """Return whether one complete path component is an identity wildcard."""
    return _PATH_IDENTITY_SEGMENT_RE.fullmatch(component) is not None


@dataclass(frozen=True, order=True)
class _PathIdentity:
    name: str
    scope: int = 0
    rigid: bool = False


type _PathTerm = str | _PathIdentity


def _path_terms(components: tuple[str, ...], *, scope: int = 0, rigid: bool = False) -> tuple[_PathTerm, ...]:
    return tuple(
        _PathIdentity(component, scope, rigid) if is_path_identity_segment(component) else component
        for component in components
    )


@dataclass(frozen=True)
class PathPatternBindings:
    """Canonical equalities for named path identities, shared by all pattern operations.

    Bindings only become more specific. Every value is either a literal, a rigid
    universally quantified identity, or the smallest free identity in its class.
    Keeping this immutable state across rewrites prevents an identity from being
    rebound when it temporarily disappears from the path.
    """

    values: tuple[tuple[_PathIdentity, _PathTerm], ...] = ()

    def _equate(self, left: _PathTerm, right: _PathTerm) -> PathPatternBindings | None:
        bindings = dict(self.values)
        left = bindings.get(left, left) if isinstance(left, _PathIdentity) else left
        right = bindings.get(right, right) if isinstance(right, _PathIdentity) else right
        if left == right:
            return self
        left_free = isinstance(left, _PathIdentity) and not left.rigid
        right_free = isinstance(right, _PathIdentity) and not right.rigid
        if not left_free and not right_free:
            return None
        if not left_free or (right_free and cast(_PathIdentity, left) < cast(_PathIdentity, right)):
            left, right = right, left
        variable = cast(_PathIdentity, left)
        bindings = {key: right if value == variable else value for key, value in bindings.items()}
        bindings[variable] = right
        return PathPatternBindings(tuple(sorted(bindings.items())))

    def _match(
        self, source: tuple[_PathTerm, ...], path: tuple[_PathTerm, ...]
    ) -> PathPatternBindings | None:
        if len(source) > len(path):
            return None
        matched = self
        for left, right in zip(source, path[: len(source)], strict=True):
            refined = matched._equate(left, right)
            if refined is None:
                return None
            matched = refined
        return matched

    def match_prefix(self, source: tuple[str, ...], path: tuple[str, ...]) -> PathPatternBindings | None:
        """Refine one resolution branch under its existing named identities."""
        return self._match(_path_terms(source), _path_terms(path[: len(source)]))

    def resolve_path(self, path: tuple[str, ...]) -> tuple[str, ...]:
        """Apply canonical bindings to a source, target, or preserved suffix."""
        bindings = dict(self.values)
        result: list[str] = []
        for term in _path_terms(path):
            resolved = bindings.get(term, term) if isinstance(term, _PathIdentity) else term
            result.append(resolved.name if isinstance(resolved, _PathIdentity) else resolved)
        return tuple(result)


def is_component_pattern_prefix(parent: tuple[str, ...], child: tuple[str, ...]) -> bool:
    """Return whether every path matched by ``child`` is contained by ``parent``."""
    # Rigid child identities cannot be assigned a literal or equated with a
    # different identity: success therefore proves coverage for every binding.
    return (
        PathPatternBindings()._match(_path_terms(parent), _path_terms(child, scope=1, rigid=True)) is not None
    )


def component_pattern_paths_overlap(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    """Return whether two component patterns can identify nested physical paths."""
    common_length = min(len(left), len(right))
    # Declarations denote sets of physical paths. Their bindings are independent
    # of one another; each repeated identity within a declaration stays equal.
    return (
        PathPatternBindings()._match(
            _path_terms(left[:common_length]), _path_terms(right[:common_length], scope=1)
        )
        is not None
    )


def is_integer_identity(value: object) -> bool:
    """Return whether a UID/GID/sequence identity is a non-negative JSON integer."""
    return type(value) is int and value >= 0


def is_sha256_digest(value: object) -> bool:
    """Return whether ``value`` is the canonical digest wire representation."""
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None


def _finding(source: Path, pointer: str, code: str, message: str, fix: str) -> ContractFinding:
    return ContractFinding(source=source, pointer=pointer, code=code, message=message, fix=fix)


def sort_findings(findings: Sequence[ContractFinding]) -> tuple[ContractFinding, ...]:
    """Return findings in a byte-stable diagnostic order."""
    return tuple(sorted(findings, key=lambda item: (str(item.source), item.pointer, item.code, item.message)))


def render_findings(findings: Sequence[ContractFinding], *, stream: TextIO | None = None) -> None:
    """Render secret-safe findings with the required actionable footer."""
    output = stream if stream is not None else sys.stderr
    for finding in sort_findings(findings):
        print(f"{finding.source}:{finding.pointer}: {finding.code}: {finding.message}", file=output)
        print(f"fix: {finding.fix}", file=output)
        print("next: correct the declared contract or collected evidence, then verify again.", file=output)
        print("run: tc-fitness-runtime-contract verify-evidence --help", file=output)


def finding_payload(finding: ContractFinding) -> dict[str, str]:
    """Convert a finding to its canonical, secret-safe command result shape."""
    return {
        "code": finding.code,
        "fix": finding.fix,
        "message": finding.message,
        "next": "correct the declared contract or collected evidence, then verify again",
        "pointer": finding.pointer,
        "run": "tc-fitness-runtime-contract verify-evidence --help",
        "source": str(finding.source),
    }


def _reject_constant(value: str) -> object:
    raise _InvalidConstantError(value)


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(key)
        result[key] = value
    return result


def _json_pointer_part(value: object) -> str:
    return str(value).replace("~", "~0").replace("/", "~1")


def _shape_findings(
    value: object,
    *,
    source: Path,
    pointer: str = "",
    depth: int = 0,
    active: set[int] | None = None,
    seen: set[int] | None = None,
) -> list[ContractFinding]:
    if depth > _MAX_DOCUMENT_DEPTH:
        return [
            _finding(
                source,
                pointer or "/",
                "document-too-deep",
                f"document nesting exceeds the {_MAX_DOCUMENT_DEPTH}-level safety limit",
                "flatten the document structure below the supported depth",
            )
        ]
    findings: list[ContractFinding] = []
    if isinstance(value, (Mapping, list)):
        active_nodes = active if active is not None else set()
        seen_nodes = seen if seen is not None else set()
        identity = id(value)
        if identity in active_nodes:
            return [
                _finding(
                    source,
                    pointer or "/",
                    "cyclic-document",
                    "document aliases form a recursive cycle that canonical JSON cannot represent",
                    "remove the cyclic YAML alias and declare an acyclic value",
                )
            ]
        if identity in seen_nodes:
            return [
                _finding(
                    source,
                    pointer or "/",
                    "repeated-container-alias",
                    "document aliases reuse a mapping or list and can expand without a safe bound",
                    "replace repeated YAML container aliases with explicit values",
                )
            ]
        seen_nodes.add(identity)
        active_nodes.add(identity)
        try:
            if isinstance(value, Mapping):
                for index, (key, child) in enumerate(value.items()):
                    if not isinstance(key, str):
                        child_pointer = f"{pointer}/<non-string-key-{index}>"
                        findings.append(
                            _finding(
                                source,
                                child_pointer,
                                "non-string-key",
                                f"mapping key has type {type(key).__name__}; canonical mappings require strings",
                                "quote the mapping key so it is a string",
                            )
                        )
                    else:
                        child_pointer = f"{pointer}/{_json_pointer_part(key)}"
                        if key in _INTEGER_FIELDS and not is_integer_identity(child):
                            findings.append(
                                _finding(
                                    source,
                                    child_pointer,
                                    "integer-id",
                                    f"{key} must be an integer and booleans are not integer identities",
                                    f"set {key} to a JSON integer",
                                )
                            )
                    findings.extend(
                        _shape_findings(
                            child,
                            source=source,
                            pointer=child_pointer,
                            depth=depth + 1,
                            active=active_nodes,
                            seen=seen_nodes,
                        )
                    )
            else:
                for index, child in enumerate(value):
                    findings.extend(
                        _shape_findings(
                            child,
                            source=source,
                            pointer=f"{pointer}/{index}",
                            depth=depth + 1,
                            active=active_nodes,
                            seen=seen_nodes,
                        )
                    )
        finally:
            active_nodes.remove(identity)
    elif isinstance(value, float) and not math.isfinite(value):
        findings.append(
            _finding(
                source,
                pointer or "/",
                "invalid-number",
                "non-finite numbers are not valid runtime contract values",
                "replace the value with a finite JSON number",
            )
        )
    return findings


def _load_strict_json(
    raw: bytes, *, source: Path
) -> tuple[Mapping[str, object] | None, tuple[ContractFinding, ...]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return None, (
            _finding(
                source,
                "/",
                "invalid-utf8",
                f"document is not UTF-8 at byte {exc.start}",
                "encode the document as UTF-8",
            ),
        )
    try:
        value = json.loads(text, object_pairs_hook=_strict_object, parse_constant=_reject_constant)
    except _DuplicateKeyError as exc:
        return None, (
            _finding(
                source,
                f"/{_json_pointer_part(exc.key)}",
                "duplicate-key",
                f"duplicate object key {exc.key!r} is ambiguous",
                "remove the duplicate key and keep one authoritative value",
            ),
        )
    except _InvalidConstantError as exc:
        return None, (
            _finding(
                source,
                "/",
                "invalid-json-constant",
                f"JSON constant {exc.value!r} is not permitted",
                "replace NaN or infinity with a finite JSON value",
            ),
        )
    except RecursionError:
        return None, (
            _finding(
                source,
                "/",
                "document-too-deep",
                "JSON nesting exceeds the parser safety limit",
                "flatten the document structure below the supported depth",
            ),
        )
    except json.JSONDecodeError as exc:
        return None, (
            _finding(
                source,
                "/",
                "invalid-json",
                f"invalid JSON at line {exc.lineno}, column {exc.colno}",
                "correct the JSON syntax",
            ),
        )
    if not isinstance(value, Mapping):
        return None, (
            _finding(
                source,
                "/",
                "wrong-document-shape",
                "document root must be an object",
                "write a top-level mapping",
            ),
        )
    return cast(Mapping[str, object], value), sort_findings(_shape_findings(value, source=source))


def _load_strict_yaml(
    raw: bytes, *, source: Path
) -> tuple[Mapping[str, object] | None, tuple[ContractFinding, ...]]:
    try:
        import yaml
    except ImportError:
        return None, (
            _finding(
                source,
                "/",
                "yaml-dependency-missing",
                "YAML contract selected but the optional PyYAML dependency is not installed",
                "install three-cubes-fitness[yaml] or use a JSON contract",
            ),
        )

    class _StrictSafeLoader(yaml.SafeLoader):  # type: ignore[misc]
        pass

    def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[object, object]:
        loader.flatten_mapping(node)
        result: dict[object, object] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in result:
                raise _DuplicateKeyError(str(key))
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    _StrictSafeLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping,
    )
    try:
        text = raw.decode("utf-8")
        loader = _StrictSafeLoader(text)
        try:
            value = loader.get_single_data()
        finally:
            loader.dispose()
    except UnicodeDecodeError as exc:
        return None, (
            _finding(
                source,
                "/",
                "invalid-utf8",
                f"document is not UTF-8 at byte {exc.start}",
                "encode the document as UTF-8",
            ),
        )
    except _DuplicateKeyError as exc:
        return None, (
            _finding(
                source,
                f"/{_json_pointer_part(exc.key)}",
                "duplicate-key",
                f"duplicate mapping key {exc.key!r} is ambiguous",
                "remove the duplicate key and keep one authoritative value",
            ),
        )
    except RecursionError:
        return None, (
            _finding(
                source,
                "/",
                "document-too-deep",
                "YAML nesting exceeds the parser safety limit",
                "flatten the document structure below the supported depth",
            ),
        )
    except (TypeError, yaml.YAMLError) as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f" at line {mark.line + 1}, column {mark.column + 1}" if mark is not None else ""
        return None, (
            _finding(source, "/", "invalid-yaml", f"invalid YAML{where}", "correct the YAML syntax"),
        )
    if not isinstance(value, Mapping):
        return None, (
            _finding(
                source,
                "/",
                "wrong-document-shape",
                "document root must be a mapping",
                "write a top-level mapping",
            ),
        )
    shape = _shape_findings(value, source=source)
    structure_is_invalid = any(
        finding.code in {"cyclic-document", "document-too-deep", "non-string-key", "repeated-container-alias"}
        for finding in shape
    )
    try:
        if not structure_is_invalid:
            canonical_json_bytes(value)
    except (RecursionError, TypeError, ValueError):
        shape.append(
            _finding(
                source,
                "/",
                "non-json-yaml",
                "YAML document contains a value that cannot be represented as canonical JSON",
                "use only JSON-compatible string keys and scalar values",
            )
        )
    return cast(Mapping[str, object], value), sort_findings(shape)


def load_runtime_document(
    path: Path,
    *,
    expected_schema: str | None,
) -> tuple[Mapping[str, object] | None, tuple[ContractFinding, ...], bytes | None]:
    """Read exact bytes and strictly decode one JSON or YAML protocol document."""
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return (
            None,
            (
                _finding(
                    path,
                    "/",
                    "missing-file",
                    "configured document does not exist",
                    "create the configured document or correct its path",
                ),
            ),
            None,
        )
    except (OSError, ValueError) as exc:
        reason = (exc.strerror or exc.__class__.__name__) if isinstance(exc, OSError) else "illegal path"
        return (
            None,
            (
                _finding(
                    path,
                    "/",
                    "unreadable-file",
                    f"configured document cannot be read: {reason}",
                    "use a legal path and make the configured document readable",
                ),
            ),
            None,
        )

    suffix = path.suffix.lower()
    if suffix == ".json":
        value, findings = _load_strict_json(raw, source=path)
    elif suffix in {".yaml", ".yml"}:
        value, findings = _load_strict_yaml(raw, source=path)
    else:
        return (
            None,
            (
                _finding(
                    path,
                    "/",
                    "unsupported-format",
                    f"unsupported document extension {suffix or '<none>'}",
                    "use a .json, .yaml or .yml file",
                ),
            ),
            raw,
        )

    found = list(findings)
    if expected_schema is not None and value is not None and value.get("schema") != expected_schema:
        found.append(
            _finding(
                path,
                "/schema",
                "wrong-schema",
                f"schema must be exactly {expected_schema!r}",
                f"set schema to {expected_schema!r}",
            )
        )
    if found:
        return None, sort_findings(found), raw
    return value, (), raw


def _safe_external_path(
    source: Path,
    configured: object,
    *,
    pointer: str,
) -> tuple[Path | None, tuple[ContractFinding, ...]]:
    if not isinstance(configured, str) or not configured.strip():
        return None, (
            _finding(
                source,
                pointer,
                "invalid-external-reference",
                "external reference file must be a non-empty repository-relative path",
                "set file to a repository-relative JSON or YAML path",
            ),
        )
    relative = PurePosixPath(configured)
    if relative.is_absolute() or ".." in relative.parts or "\\" in configured or "\x00" in configured:
        return None, (
            _finding(
                source,
                pointer,
                "unsafe-external-reference",
                "external reference file must stay beneath the contract directory",
                "use a relative path without '..', backslashes or NUL bytes",
            ),
        )
    root = source.resolve().parent
    try:
        candidate = (root / Path(*relative.parts)).resolve()
        candidate.relative_to(root)
    except (OSError, RuntimeError, ValueError):
        return None, (
            _finding(
                source,
                pointer,
                "unsafe-external-reference",
                "external reference resolves outside the contract directory or through an invalid symlink",
                "reference a readable file physically beneath the contract directory",
            ),
        )
    return candidate, ()


def _decode_json_pointer(
    pointer: object, *, source: Path, location: str
) -> tuple[tuple[str, ...] | None, tuple[ContractFinding, ...]]:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        return None, (
            _finding(
                source,
                location,
                "invalid-external-pointer",
                "external reference pointer must be an absolute JSON pointer",
                "set pointer to a slash-prefixed path such as /clusters",
            ),
        )
    decoded: list[str] = []
    for raw_part in pointer[1:].split("/"):
        index = 0
        part = ""
        while index < len(raw_part):
            if raw_part[index] != "~":
                part += raw_part[index]
                index += 1
                continue
            if index + 1 >= len(raw_part) or raw_part[index + 1] not in {"0", "1"}:
                return None, (
                    _finding(
                        source,
                        location,
                        "invalid-external-pointer",
                        "external reference pointer contains an invalid JSON pointer escape",
                        "escape '~' as '~0' and '/' as '~1' in pointer components",
                    ),
                )
            part += "~" if raw_part[index + 1] == "0" else "/"
            index += 2
        decoded.append(part)
    return tuple(decoded), ()


def _select_external_value(
    document: object,
    components: tuple[str, ...],
    *,
    source: Path,
    pointer: str,
) -> tuple[object | None, tuple[ContractFinding, ...]]:
    value = document
    for component in components:
        if isinstance(value, Mapping) and component in value:
            value = value[component]
            continue
        if isinstance(value, list) and component.isascii() and component.isdecimal():
            if (
                (len(component) > 1 and component.startswith("0"))
                or len(component) > len(_MAX_ARRAY_INDEX_TEXT)
                or (len(component) == len(_MAX_ARRAY_INDEX_TEXT) and component > _MAX_ARRAY_INDEX_TEXT)
            ):
                return None, (
                    _finding(
                        source,
                        pointer,
                        "invalid-external-pointer",
                        "external reference pointer contains a non-canonical or unbounded array index",
                        "use a canonical decimal array index without leading zeroes",
                    ),
                )
            index = int(component)
            if index < len(value):
                value = value[index]
                continue
        return None, (
            _finding(
                source,
                pointer,
                "external-pointer-missing",
                "external reference pointer does not select a value",
                "correct the pointer or add the selected value to the external registry",
            ),
        )
    return value, ()


def _load_external_references(
    declarations: object,
    *,
    source: Path,
    names: frozenset[str] | None = None,
) -> tuple[dict[str, object], tuple[ContractFinding, ...]]:
    if declarations is None:
        return {}, ()
    if not isinstance(declarations, Mapping):
        return {}, (
            _finding(
                source,
                "/external_references",
                "invalid-external-references",
                "external_references must be a mapping of names to file and pointer declarations",
                "declare each external reference beneath a unique mapping key",
            ),
        )

    loaded: dict[str, object] = {}
    findings: list[ContractFinding] = []
    for name, declaration in declarations.items():
        if names is not None and name not in names:
            continue
        location = f"/external_references/{_json_pointer_part(name)}"
        if not isinstance(name, str) or not name.strip() or not isinstance(declaration, Mapping):
            findings.append(
                _finding(
                    source,
                    location,
                    "invalid-external-reference",
                    "external reference requires a non-empty name and a mapping declaration",
                    "declare a named mapping with file and pointer fields",
                )
            )
            continue
        unknown = set(declaration) - {"file", "pointer"}
        if unknown or set(declaration) != {"file", "pointer"}:
            findings.append(
                _finding(
                    source,
                    location,
                    "invalid-external-reference",
                    "external reference declaration must contain exactly file and pointer",
                    "remove unknown fields and set both file and pointer",
                )
            )
            continue
        path, path_findings = _safe_external_path(
            source,
            declaration.get("file"),
            pointer=f"{location}/file",
        )
        components, pointer_findings = _decode_json_pointer(
            declaration.get("pointer"),
            source=source,
            location=f"{location}/pointer",
        )
        findings.extend((*path_findings, *pointer_findings))
        if path is None or components is None:
            continue
        document, document_findings, _ = load_runtime_document(path, expected_schema=None)
        findings.extend(document_findings)
        if document is None or document_findings:
            continue
        selected, selection_findings = _select_external_value(
            document,
            components,
            source=path,
            pointer=cast(str, declaration["pointer"]),
        )
        findings.extend(selection_findings)
        if not selection_findings:
            loaded[name] = selected
    return loaded, sort_findings(findings)


def _external_reference_names(value: object) -> frozenset[str]:
    """Return reference names reachable from one selected contract value."""
    names: set[str] = set()

    def visit(current: object) -> None:
        if isinstance(current, Mapping):
            if "$external_ref" in current:
                name = current.get("$external_ref")
                if isinstance(name, str) and name.strip():
                    names.add(name)
                return
            for child in current.values():
                visit(child)
        elif isinstance(current, list):
            for child in current:
                visit(child)

    visit(value)
    return frozenset(names)


def _replace_external_references(
    value: object,
    *,
    references: Mapping[str, object],
    source: Path,
    pointer: str = "",
) -> tuple[object, tuple[ContractFinding, ...]]:
    if isinstance(value, Mapping):
        if "$external_ref" in value:
            if set(value) != {"$external_ref"}:
                return value, (
                    _finding(
                        source,
                        pointer or "/",
                        "invalid-external-reference-use",
                        "$external_ref must be the only field in its placeholder mapping",
                        "move sibling fields outside the external reference placeholder",
                    ),
                )
            name = value.get("$external_ref")
            if not isinstance(name, str) or not name.strip() or name not in references:
                return value, (
                    _finding(
                        source,
                        f"{pointer}/$external_ref",
                        "undefined-external-reference",
                        f"external reference {name!r} is not declared or could not be loaded",
                        "declare the named external reference and correct all loading findings",
                    ),
                )
            return references[name], ()
        result: dict[str, object] = {}
        findings: list[ContractFinding] = []
        for key, child in value.items():
            child_pointer = f"{pointer}/{_json_pointer_part(key)}"
            replacement, child_findings = _replace_external_references(
                child,
                references=references,
                source=source,
                pointer=child_pointer,
            )
            result[str(key)] = replacement
            findings.extend(child_findings)
        return result, sort_findings(findings)
    if isinstance(value, list):
        result_list: list[object] = []
        findings = []
        for index, child in enumerate(value):
            replacement, child_findings = _replace_external_references(
                child,
                references=references,
                source=source,
                pointer=f"{pointer}/{index}",
            )
            result_list.append(replacement)
            findings.extend(child_findings)
        return result_list, sort_findings(findings)
    return value, ()


def _safe_config_path(
    repo_root: Path, configured: object, *, pointer: str
) -> tuple[Path | None, tuple[ContractFinding, ...]]:
    source = repo_root / "pyproject.toml"
    if not isinstance(configured, str) or not configured.strip():
        return None, (
            _finding(
                source,
                pointer,
                "missing-config",
                "configured file path must be a non-empty string",
                "set the file to a repo-relative JSON or YAML path",
            ),
        )
    relative = PurePosixPath(configured)
    if relative.is_absolute() or ".." in relative.parts or "\\" in configured or "\x00" in configured:
        return None, (
            _finding(
                source,
                pointer,
                "unsafe-config-path",
                "configured file path must stay beneath the repository root",
                "use a repo-relative path without '..' or backslashes",
            ),
        )
    root = repo_root.resolve()
    try:
        candidate = (root / Path(*relative.parts)).resolve()
    except (OSError, RuntimeError, ValueError):
        return None, (
            _finding(
                source,
                pointer,
                "unsafe-config-path",
                "configured file cannot be resolved safely beneath the repository root",
                "remove cyclic or invalid symlinks and use a repo-relative path",
            ),
        )
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, (
            _finding(
                source,
                pointer,
                "unsafe-config-path",
                "configured file resolves outside the repository root",
                "reference a file physically beneath the repository root",
            ),
        )
    return candidate, ()


def resolve_contract(
    registry: Mapping[str, object],
    *,
    environment: str | None,
    target: str | None,
    source: Path,
) -> tuple[Mapping[str, object] | None, tuple[ContractFinding, ...]]:
    """Resolve one environment and target, or accept an already-selected contract."""
    if "environments" not in registry:
        selected = dict(registry)
        for key, expected in (("environment", environment), ("target", target)):
            actual = selected.get(key)
            if expected is not None and actual not in (None, expected):
                return None, (
                    _finding(
                        source,
                        f"/{key}",
                        "selection-mismatch",
                        f"selected {key} does not match {expected!r}",
                        f"select {actual!r} or correct the document",
                    ),
                )
            if expected is not None:
                selected[key] = expected
        declarations = selected.pop("external_references", None)
    else:
        environments = registry.get("environments")
        if not isinstance(environments, Mapping):
            return None, (
                _finding(
                    source,
                    "/environments",
                    "invalid-environments",
                    "environments must be a mapping when the key is present",
                    "remove the key for a selected contract or declare an environment mapping",
                ),
            )

        if not isinstance(environment, str) or not environment or not isinstance(target, str) or not target:
            return None, (
                _finding(
                    source,
                    "/environments",
                    "missing-selection",
                    "a registry requires both environment and target selectors",
                    "supply non-empty environment and target values",
                ),
            )
        if not isinstance(environments.get(environment), Mapping):
            return None, (
                _finding(
                    source,
                    f"/environments/{_json_pointer_part(environment)}",
                    "unknown-environment",
                    f"environment {environment!r} is not declared",
                    "select a declared environment or add it to the registry",
                ),
            )
        environment_doc = cast(Mapping[str, object], environments[environment])
        targets = environment_doc.get("targets")
        if not isinstance(targets, Mapping) or not isinstance(targets.get(target), Mapping):
            return None, (
                _finding(
                    source,
                    f"/environments/{_json_pointer_part(environment)}/targets/{_json_pointer_part(target)}",
                    "unknown-target",
                    f"target {target!r} is not declared",
                    "select a declared target or add it to the registry",
                ),
            )
        selected_target = cast(Mapping[str, object], targets[target])
        selected = dict(selected_target)
        reserved = {"schema": CONTRACT_SCHEMA, "environment": environment, "target": target}
        for key, expected in reserved.items():
            if key in selected and selected[key] != expected:
                return None, (
                    _finding(
                        source,
                        f"/environments/{_json_pointer_part(environment)}/targets/{_json_pointer_part(target)}/{key}",
                        "selection-conflict",
                        f"target-local {key} conflicts with its registry identity",
                        f"remove the target-local {key} or set it to {expected!r}",
                    ),
                )
            selected[key] = expected
        declarations = registry.get("external_references")

    references, reference_findings = _load_external_references(
        declarations,
        source=source,
        names=_external_reference_names(selected),
    )
    resolved, use_findings = _replace_external_references(
        selected,
        references=references,
        source=source,
    )
    findings = sort_findings((*reference_findings, *use_findings))
    if findings or not isinstance(resolved, Mapping):
        return None, findings
    return cast(Mapping[str, object], resolved), ()


def load_contract_documents(
    config: Mapping[str, object],
    *,
    repo_root: Path,
    require_evidence: bool = False,
) -> tuple[ContractDocuments | None, tuple[ContractFinding, ...]]:
    """Load configured contract/evidence files without weakening empty adoption."""
    if not config:
        return None, ()

    contract_path, path_findings = _safe_config_path(
        repo_root, config.get("contract_file"), pointer="/contract_file"
    )
    if path_findings or contract_path is None:
        return None, path_findings
    registry, contract_findings, contract_bytes = load_runtime_document(
        contract_path, expected_schema=CONTRACT_SCHEMA
    )
    if contract_findings or registry is None or contract_bytes is None:
        return None, contract_findings
    contract, selection_findings = resolve_contract(
        registry,
        environment=cast(str | None, config.get("environment")),
        target=cast(str | None, config.get("target")),
        source=contract_path,
    )
    if selection_findings or contract is None:
        return None, selection_findings

    evidence_path: Path | None = None
    evidence: Mapping[str, object] | None = None
    evidence_bytes: bytes | None = None
    if require_evidence or "evidence_file" in config:
        evidence_path, evidence_path_findings = _safe_config_path(
            repo_root,
            config.get("evidence_file"),
            pointer="/evidence_file",
        )
        if evidence_path_findings or evidence_path is None:
            return None, evidence_path_findings
        evidence, evidence_findings, evidence_bytes = load_runtime_document(
            evidence_path,
            expected_schema=EVIDENCE_SCHEMA,
        )
        if evidence_findings or evidence is None or evidence_bytes is None:
            return None, evidence_findings

    return ContractDocuments(
        contract_path=contract_path,
        contract=contract,
        contract_bytes=contract_bytes,
        evidence_path=evidence_path,
        evidence=evidence,
        evidence_bytes=evidence_bytes,
    ), ()


class RuntimeContractRule(FitnessRule):
    """Hard-adoption base for contract checks: findings cannot be baselined."""

    name: ClassVar[str] = "runtime-contract"
    remediation: ClassVar[str] = (
        "fix: correct the runtime contract\nnext: verify again\nrun: tc-fitness-runtime-contract --help"
    )
    requires_evidence: ClassVar[bool] = False

    def __init__(self, config: Mapping[str, object], *, repo_root: Path | None = None) -> None:
        super().__init__(repo_root=repo_root)
        self.config = dict(config)
        self.active = bool(config)

    @classmethod
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> RuntimeContractRule:
        return cls(cast(Mapping[str, object], config), repo_root=repo_root)

    def file_has_violation(self, path: Path) -> bool:
        """Runtime contract rules validate documents rather than enumerated files."""
        return False

    def load_documents(self) -> ContractDocuments:
        """Return configured documents, raising only when called on invalid input."""
        documents, findings = load_contract_documents(
            self.config,
            repo_root=self._repo_root,
            require_evidence=self.requires_evidence,
        )
        if findings or documents is None:
            detail = "; ".join(f"{finding.code}: {finding.message}" for finding in findings)
            raise ValueError(detail or "runtime contract rule is not configured")
        return documents

    def validate_documents(self, documents: ContractDocuments) -> tuple[ContractFinding, ...]:
        """Subclasses implement their protocol-specific invariants."""
        return ()

    def validate_configuration(self) -> tuple[ContractFinding, ...]:
        """Subclasses may reject malformed values from their active config block."""
        return ()

    def collect_findings(self) -> tuple[ContractFinding, ...]:
        """Load and validate the configured documents once."""
        if not self.active:
            return ()
        config_findings = self.validate_configuration()
        documents, findings = load_contract_documents(
            self.config,
            repo_root=self._repo_root,
            require_evidence=self.requires_evidence,
        )
        if findings or documents is None:
            return sort_findings((*config_findings, *findings))
        return sort_findings((*config_findings, *self.validate_documents(documents)))

    def run(self) -> int:
        """Fail on every finding; intentionally bypass per-file baselines."""
        findings = self.collect_findings()
        if not findings:
            return 0
        render_findings(findings)
        return 1

    def establish_baseline(self) -> Path:
        """Validate active runtime documents and reject grandfathering defects."""
        findings = self.collect_findings()
        if findings:
            render_findings(findings)
            raise RuntimeError("runtime contract findings cannot establish a baseline")
        return super().establish_baseline()


__all__ = [
    "CONTRACT_SCHEMA",
    "EVIDENCE_SCHEMA",
    "ContractDocuments",
    "ContractFinding",
    "RuntimeContractRule",
    "absolute_posix_components",
    "canonical_json_bytes",
    "component_pattern_paths_overlap",
    "component_paths_overlap",
    "finding_payload",
    "is_component_pattern_prefix",
    "is_component_prefix",
    "is_integer_identity",
    "is_path_identity_segment",
    "is_sha256_digest",
    "load_contract_documents",
    "load_runtime_document",
    "render_findings",
    "resolve_contract",
    "sort_findings",
]
