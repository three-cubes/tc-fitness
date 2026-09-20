"""CORE check: schema_conformance — every data file carries its required keys.

A family of data files (brand-token sheets, manifests, config fragments) shares
a contract: each MUST provide a set of required top-level keys. A file missing
one renders an unstyled component, a half-configured connector, or a crash at
load time. This rule proves the required key set is present in every file in
scope BEFORE anything consumes it.

The required key set is CONFIG (``required_keys``) the consumer supplies — the
repo-agnostic generalisation of a schema. The donor check derived the key set
from a TypeScript interface, which is repo-coupled; here the consumer declares
the keys (or points a follow-on check at a schema). Files are parsed as YAML
(a superset of JSON, so ``.json`` parses too); a file that is not a mapping, or
that omits a required key, is a violation.

Ported from tc-agent-zone ``scripts/checks/brand_tokens_schema_validate.py``
(ADR-022 D5) — re-expressed as a configurable, repo-agnostic rule. The scan
roots, the file extensions, and the required key set are all CONFIG; nothing
here names a repo, a directory, or a field.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: A schema with no declared required keys imposes no constraint — every file
#: is conformant. The consumer narrows this via ``required_keys``.
DEFAULT_REQUIRED_KEYS: tuple[str, ...] = ()

REMEDIATION = _remediation(
    fix=(
        "add the missing required key(s) to the data file so it carries the "
        "full contract every consumer of this file family depends on. The "
        "required key set is declared in this check's config block."
    ),
    nxt="re-run this check to confirm the file is conformant.",
    run="python -m tc_fitness.core_checks.schema_conformance",
    passing="every required key present at the top level of the mapping",
    forbidden="ship a data file missing a key its consumers read at load time",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__load_mapping__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__load_mapping__mutmut)
def _load_mapping(path: Path) -> dict[str, Any] | None:
    """Parse ``path`` as YAML/JSON; return the mapping, or None if not a mapping.

    A decode/parse error or a non-mapping document returns ``None`` — the rule
    treats a file it cannot read as a mapping as a violation (it cannot prove
    conformance). PyYAML is imported lazily to keep the parser's import cost out
    of callers that never bind this check; it is a required package dependency.
    """
    try:
        import yaml
    except ImportError:  # pragma: no cover - exercised only on hosts without PyYAML
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, UnicodeDecodeError):
        return None
    return loaded if isinstance(loaded, dict) else None


def x__load_mapping__mutmut_orig(path: Path) -> dict[str, Any] | None:
    """Parse ``path`` as YAML/JSON; return the mapping, or None if not a mapping.

    A decode/parse error or a non-mapping document returns ``None`` — the rule
    treats a file it cannot read as a mapping as a violation (it cannot prove
    conformance). PyYAML is imported lazily to keep the parser's import cost out
    of callers that never bind this check; it is a required package dependency.
    """
    try:
        import yaml
    except ImportError:  # pragma: no cover - exercised only on hosts without PyYAML
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, UnicodeDecodeError):
        return None
    return loaded if isinstance(loaded, dict) else None


def x__load_mapping__mutmut_1(path: Path) -> dict[str, Any] | None:
    """Parse ``path`` as YAML/JSON; return the mapping, or None if not a mapping.

    A decode/parse error or a non-mapping document returns ``None`` — the rule
    treats a file it cannot read as a mapping as a violation (it cannot prove
    conformance). PyYAML is imported lazily to keep the parser's import cost out
    of callers that never bind this check; it is a required package dependency.
    """
    try:
        import yaml
    except ImportError:  # pragma: no cover - exercised only on hosts without PyYAML
        return None
    try:
        loaded = None
    except (yaml.YAMLError, UnicodeDecodeError):
        return None
    return loaded if isinstance(loaded, dict) else None


def x__load_mapping__mutmut_2(path: Path) -> dict[str, Any] | None:
    """Parse ``path`` as YAML/JSON; return the mapping, or None if not a mapping.

    A decode/parse error or a non-mapping document returns ``None`` — the rule
    treats a file it cannot read as a mapping as a violation (it cannot prove
    conformance). PyYAML is imported lazily to keep the parser's import cost out
    of callers that never bind this check; it is a required package dependency.
    """
    try:
        import yaml
    except ImportError:  # pragma: no cover - exercised only on hosts without PyYAML
        return None
    try:
        loaded = yaml.safe_load(None)
    except (yaml.YAMLError, UnicodeDecodeError):
        return None
    return loaded if isinstance(loaded, dict) else None


def x__load_mapping__mutmut_3(path: Path) -> dict[str, Any] | None:
    """Parse ``path`` as YAML/JSON; return the mapping, or None if not a mapping.

    A decode/parse error or a non-mapping document returns ``None`` — the rule
    treats a file it cannot read as a mapping as a violation (it cannot prove
    conformance). PyYAML is imported lazily to keep the parser's import cost out
    of callers that never bind this check; it is a required package dependency.
    """
    try:
        import yaml
    except ImportError:  # pragma: no cover - exercised only on hosts without PyYAML
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding=None))
    except (yaml.YAMLError, UnicodeDecodeError):
        return None
    return loaded if isinstance(loaded, dict) else None


def x__load_mapping__mutmut_4(path: Path) -> dict[str, Any] | None:
    """Parse ``path`` as YAML/JSON; return the mapping, or None if not a mapping.

    A decode/parse error or a non-mapping document returns ``None`` — the rule
    treats a file it cannot read as a mapping as a violation (it cannot prove
    conformance). PyYAML is imported lazily to keep the parser's import cost out
    of callers that never bind this check; it is a required package dependency.
    """
    try:
        import yaml
    except ImportError:  # pragma: no cover - exercised only on hosts without PyYAML
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding="XXutf-8XX"))
    except (yaml.YAMLError, UnicodeDecodeError):
        return None
    return loaded if isinstance(loaded, dict) else None


def x__load_mapping__mutmut_5(path: Path) -> dict[str, Any] | None:
    """Parse ``path`` as YAML/JSON; return the mapping, or None if not a mapping.

    A decode/parse error or a non-mapping document returns ``None`` — the rule
    treats a file it cannot read as a mapping as a violation (it cannot prove
    conformance). PyYAML is imported lazily to keep the parser's import cost out
    of callers that never bind this check; it is a required package dependency.
    """
    try:
        import yaml
    except ImportError:  # pragma: no cover - exercised only on hosts without PyYAML
        return None
    try:
        loaded = yaml.safe_load(path.read_text(encoding="UTF-8"))
    except (yaml.YAMLError, UnicodeDecodeError):
        return None
    return loaded if isinstance(loaded, dict) else None

mutants_x__load_mapping__mutmut['_mutmut_orig'] = x__load_mapping__mutmut_orig # type: ignore # mutmut generated
mutants_x__load_mapping__mutmut['x__load_mapping__mutmut_1'] = x__load_mapping__mutmut_1 # type: ignore # mutmut generated
mutants_x__load_mapping__mutmut['x__load_mapping__mutmut_2'] = x__load_mapping__mutmut_2 # type: ignore # mutmut generated
mutants_x__load_mapping__mutmut['x__load_mapping__mutmut_3'] = x__load_mapping__mutmut_3 # type: ignore # mutmut generated
mutants_x__load_mapping__mutmut['x__load_mapping__mutmut_4'] = x__load_mapping__mutmut_4 # type: ignore # mutmut generated
mutants_x__load_mapping__mutmut['x__load_mapping__mutmut_5'] = x__load_mapping__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_missing_required_keys__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_missing_required_keys__mutmut)
def file_missing_required_keys(path: Path, *, required_keys: tuple[str, ...]) -> bool:
    """True iff ``path`` is not a mapping OR omits any of ``required_keys``.

    Pure helper (the detection core) so tests assert on it directly. With an
    empty ``required_keys`` every readable mapping is conformant; an unreadable
    or non-mapping file is always a violation (conformance is unprovable).
    """
    mapping = _load_mapping(path)
    if mapping is None:
        return True
    return any(key not in mapping for key in required_keys)


def x_file_missing_required_keys__mutmut_orig(path: Path, *, required_keys: tuple[str, ...]) -> bool:
    """True iff ``path`` is not a mapping OR omits any of ``required_keys``.

    Pure helper (the detection core) so tests assert on it directly. With an
    empty ``required_keys`` every readable mapping is conformant; an unreadable
    or non-mapping file is always a violation (conformance is unprovable).
    """
    mapping = _load_mapping(path)
    if mapping is None:
        return True
    return any(key not in mapping for key in required_keys)


def x_file_missing_required_keys__mutmut_1(path: Path, *, required_keys: tuple[str, ...]) -> bool:
    """True iff ``path`` is not a mapping OR omits any of ``required_keys``.

    Pure helper (the detection core) so tests assert on it directly. With an
    empty ``required_keys`` every readable mapping is conformant; an unreadable
    or non-mapping file is always a violation (conformance is unprovable).
    """
    mapping = None
    if mapping is None:
        return True
    return any(key not in mapping for key in required_keys)


def x_file_missing_required_keys__mutmut_2(path: Path, *, required_keys: tuple[str, ...]) -> bool:
    """True iff ``path`` is not a mapping OR omits any of ``required_keys``.

    Pure helper (the detection core) so tests assert on it directly. With an
    empty ``required_keys`` every readable mapping is conformant; an unreadable
    or non-mapping file is always a violation (conformance is unprovable).
    """
    mapping = _load_mapping(None)
    if mapping is None:
        return True
    return any(key not in mapping for key in required_keys)


def x_file_missing_required_keys__mutmut_3(path: Path, *, required_keys: tuple[str, ...]) -> bool:
    """True iff ``path`` is not a mapping OR omits any of ``required_keys``.

    Pure helper (the detection core) so tests assert on it directly. With an
    empty ``required_keys`` every readable mapping is conformant; an unreadable
    or non-mapping file is always a violation (conformance is unprovable).
    """
    mapping = _load_mapping(path)
    if mapping is not None:
        return True
    return any(key not in mapping for key in required_keys)


def x_file_missing_required_keys__mutmut_4(path: Path, *, required_keys: tuple[str, ...]) -> bool:
    """True iff ``path`` is not a mapping OR omits any of ``required_keys``.

    Pure helper (the detection core) so tests assert on it directly. With an
    empty ``required_keys`` every readable mapping is conformant; an unreadable
    or non-mapping file is always a violation (conformance is unprovable).
    """
    mapping = _load_mapping(path)
    if mapping is None:
        return False
    return any(key not in mapping for key in required_keys)


def x_file_missing_required_keys__mutmut_5(path: Path, *, required_keys: tuple[str, ...]) -> bool:
    """True iff ``path`` is not a mapping OR omits any of ``required_keys``.

    Pure helper (the detection core) so tests assert on it directly. With an
    empty ``required_keys`` every readable mapping is conformant; an unreadable
    or non-mapping file is always a violation (conformance is unprovable).
    """
    mapping = _load_mapping(path)
    if mapping is None:
        return True
    return any(None)


def x_file_missing_required_keys__mutmut_6(path: Path, *, required_keys: tuple[str, ...]) -> bool:
    """True iff ``path`` is not a mapping OR omits any of ``required_keys``.

    Pure helper (the detection core) so tests assert on it directly. With an
    empty ``required_keys`` every readable mapping is conformant; an unreadable
    or non-mapping file is always a violation (conformance is unprovable).
    """
    mapping = _load_mapping(path)
    if mapping is None:
        return True
    return any(key in mapping for key in required_keys)

mutants_x_file_missing_required_keys__mutmut['_mutmut_orig'] = x_file_missing_required_keys__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_missing_required_keys__mutmut['x_file_missing_required_keys__mutmut_1'] = x_file_missing_required_keys__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_missing_required_keys__mutmut['x_file_missing_required_keys__mutmut_2'] = x_file_missing_required_keys__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_missing_required_keys__mutmut['x_file_missing_required_keys__mutmut_3'] = x_file_missing_required_keys__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_missing_required_keys__mutmut['x_file_missing_required_keys__mutmut_4'] = x_file_missing_required_keys__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_missing_required_keys__mutmut['x_file_missing_required_keys__mutmut_5'] = x_file_missing_required_keys__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_missing_required_keys__mutmut['x_file_missing_required_keys__mutmut_6'] = x_file_missing_required_keys__mutmut_6 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁSchemaConformanceǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class SchemaConformance(FitnessRule):
    """Flags data files that omit a required schema key (ADR-022 D5 shape)."""

    name = "schema-conformance"
    remediation = REMEDIATION
    extensions = (".yaml", ".yml", ".json")

    #: Rule-specific knob — instance attr so ``from_config`` overrides it.
    required_keys: tuple[str, ...] = DEFAULT_REQUIRED_KEYS

    @classmethod
    @_mutmut_mutated(mutants_xǁSchemaConformanceǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = None
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, )
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = None
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get(None, DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", None)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get(DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", )
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("XXrequired_keysXX", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("REQUIRED_KEYS", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(keys)
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = None
        return rule

    @classmethod
    def xǁSchemaConformanceǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SchemaConformance:
        """Build from config, also reading the ``required_keys`` schema."""
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SchemaConformance)  # noqa: S101  # narrowing for mypy
        keys = config.get("required_keys", DEFAULT_REQUIRED_KEYS)
        rule.required_keys = tuple(None)
        return rule

    @_mutmut_mutated(mutants_xǁSchemaConformanceǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_missing_required_keys(path, required_keys=self.required_keys)

    def xǁSchemaConformanceǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_missing_required_keys(path, required_keys=self.required_keys)

    def xǁSchemaConformanceǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_missing_required_keys(None, required_keys=self.required_keys)

    def xǁSchemaConformanceǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_missing_required_keys(path, required_keys=None)

    def xǁSchemaConformanceǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_missing_required_keys(required_keys=self.required_keys)

    def xǁSchemaConformanceǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_missing_required_keys(path, )

mutants_xǁSchemaConformanceǁfrom_config__mutmut['_mutmut_orig'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_1'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_2'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_3'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_4'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_5'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_6'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_7'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_8'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_9'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_10'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_11'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_12'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_13'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfrom_config__mutmut['xǁSchemaConformanceǁfrom_config__mutmut_14'] = SchemaConformance.xǁSchemaConformanceǁfrom_config__mutmut_14 # type: ignore # mutmut generated

mutants_xǁSchemaConformanceǁfile_has_violation__mutmut['_mutmut_orig'] = SchemaConformance.xǁSchemaConformanceǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfile_has_violation__mutmut['xǁSchemaConformanceǁfile_has_violation__mutmut_1'] = SchemaConformance.xǁSchemaConformanceǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfile_has_violation__mutmut['xǁSchemaConformanceǁfile_has_violation__mutmut_2'] = SchemaConformance.xǁSchemaConformanceǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfile_has_violation__mutmut['xǁSchemaConformanceǁfile_has_violation__mutmut_3'] = SchemaConformance.xǁSchemaConformanceǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁSchemaConformanceǁfile_has_violation__mutmut['xǁSchemaConformanceǁfile_has_violation__mutmut_4'] = SchemaConformance.xǁSchemaConformanceǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> SchemaConformance:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SchemaConformance.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> SchemaConformance:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SchemaConformance.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> SchemaConformance:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SchemaConformance.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> SchemaConformance:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SchemaConformance.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> SchemaConformance:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SchemaConformance.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> SchemaConformance:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SchemaConformance.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SchemaConformance, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SchemaConformance, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SchemaConformance, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SchemaConformance, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
