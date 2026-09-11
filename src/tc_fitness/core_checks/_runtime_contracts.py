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
    if not isinstance(value, str) or not value or "\\" in value:
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


def _shape_findings(value: object, *, source: Path, pointer: str = "") -> list[ContractFinding]:
    findings: list[ContractFinding] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
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
            findings.extend(_shape_findings(child, source=source, pointer=child_pointer))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_shape_findings(child, source=source, pointer=f"{pointer}/{index}"))
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
    try:
        canonical_json_bytes(value)
    except (TypeError, ValueError):
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
    expected_schema: str,
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
    except OSError as exc:
        return (
            None,
            (
                _finding(
                    path,
                    "/",
                    "unreadable-file",
                    f"configured document cannot be read: {exc.strerror or exc.__class__.__name__}",
                    "make the configured document readable",
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
    if value is not None and value.get("schema") != expected_schema:
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
    if relative.is_absolute() or ".." in relative.parts or "\\" in configured:
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
    except (OSError, RuntimeError):
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
    environments = registry.get("environments")
    if environments is None:
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
        return selected, ()

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
    if not isinstance(environments, Mapping) or not isinstance(environments.get(environment), Mapping):
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
    return selected, ()


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

    def collect_findings(self) -> tuple[ContractFinding, ...]:
        """Load and validate the configured documents once."""
        if not self.active:
            return ()
        documents, findings = load_contract_documents(
            self.config,
            repo_root=self._repo_root,
            require_evidence=self.requires_evidence,
        )
        if findings or documents is None:
            return findings
        return self.validate_documents(documents)

    def run(self) -> int:
        """Fail on every finding; intentionally bypass per-file baselines."""
        findings = self.collect_findings()
        if not findings:
            return 0
        render_findings(findings)
        return 1


__all__ = [
    "CONTRACT_SCHEMA",
    "EVIDENCE_SCHEMA",
    "ContractDocuments",
    "ContractFinding",
    "RuntimeContractRule",
    "absolute_posix_components",
    "canonical_json_bytes",
    "component_paths_overlap",
    "finding_payload",
    "is_component_prefix",
    "is_integer_identity",
    "is_sha256_digest",
    "load_contract_documents",
    "load_runtime_document",
    "render_findings",
    "resolve_contract",
    "sort_findings",
]
