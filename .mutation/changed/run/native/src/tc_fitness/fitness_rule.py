"""FitnessRule ABC — the repo-agnostic, config-driven base for a CORE check.

Promoted from kairix's ``scripts/checks/_fitness_rule.py`` (ADR-026 Track B)
into the shared engine and made REPO-AGNOSTIC: every repo-specific knob
(scan roots and file extensions) is a class
attribute or constructor argument the CONSUMER supplies — the engine bakes in
no ``kairix`` / ``taz`` identity. A concrete CORE check is a small subclass:

.. code-block:: python

    class NoDuplicateString(FitnessRule):
        name = "no-duplicate-string"          # → finding and output identity
        remediation = REMEDIATION
        # roots / extensions come from CONFIG (see below)

        def file_has_violation(self, path: Path) -> bool:
            ...

The base class inherits everything that does NOT vary per rule: enumerating
in-scope files, applying the scope predicate, and hard-gating every violation.

Config injection
----------------
A CORE check module ships a subclass whose *behavioural* attributes default to
empty / repo-neutral values, then a consumer binds it from its
``[tool.tc_fitness]`` catalogue entry by passing config to
:meth:`from_config`. The two surfaces:

* **Class attributes** — a CORE check sets ``name`` + ``remediation`` (the
  parts intrinsic to the rule) and leaves ``roots`` / ``extensions`` at their
  repo-neutral defaults.
* **``from_config(config, repo_root=...)``** — overrides ``roots`` /
  ``extensions`` / ``name`` from the consumer's config dict
  (sourced from its catalogue entry), returning a ready-to-run instance.

The low-level functional helpers (:func:`tc_fitness.gate`,
:func:`tc_fitness.python_files`) remain canonical; this ABC collapses the
boilerplate around them. Checks needing custom enumeration override
:meth:`enumerate_files`; checks with a non-path scope override
:meth:`is_in_scope`.
"""

from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod
from collections.abc import Mapping
from pathlib import Path
from typing import Any, ClassVar

from tc_fitness.lib import REPO_ROOT, gate

#: Wall-clock ceiling for the ``git ls-files`` enumeration subprocess. A tracked
#: listing on any real tree returns in well under a second; the bound only guards
#: against a wedged git process, after which enumeration falls back to a walk.
_GIT_LS_FILES_TIMEOUT_S = 30

_REMOVED_SUPPRESSION_OPTIONS = frozenset(
    {
        "allowed_names",
        "allow_missing_current",
        "baseline_ok",
        "cutover_ref",
        "excluded_parts",
        "excluded_segments",
        "exempt_dirs",
        "exempt_extensions",
        "exempt_files",
        "exempt_keys",
        "exempt_prefixes",
        "exempt_roots",
        "exempt_segments",
        "exempt_specifiers",
        "informational_marker",
        "skip_dir_segments",
        "skip_parts",
        "test_file_regex",
        "warn_only",
    }
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁFitnessRuleǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁFitnessRuleǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁFitnessRuleǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁFitnessRuleǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut: MutantDict = {}  # type: ignore
mutants_xǁFitnessRuleǁ_repo_relative__mutmut: MutantDict = {}  # type: ignore
mutants_xǁFitnessRuleǁcollect_violations__mutmut: MutantDict = {}  # type: ignore
mutants_xǁFitnessRuleǁrun__mutmut: MutantDict = {}  # type: ignore


class FitnessRule(ABC):
    """A repo-agnostic, config-driven fitness rule.

    Class attributes (required on a concrete subclass):
        name: canonical check name used in findings and output.
        remediation: the ``fix:`` / ``next:`` / ``run:`` remediation block
            (build it with :func:`tc_fitness.remediation`).

    Class attributes (config — repo-neutral defaults, overridden per consumer):
        roots: repo-relative directories to scan. Default ``()`` — a CORE
            check ships NO repo paths; the consumer supplies them via config.
        extensions: filename extensions in scope. Default ``(".py",)``.

    Concrete method (required):
        :meth:`file_has_violation`: truthy when the file violates the rule.

    Optional overrides:
        :meth:`is_in_scope` — customise the scope predicate.
        :meth:`enumerate_files` — customise file enumeration.
    """

    name: ClassVar[str]
    remediation: ClassVar[str]
    # Repo-NEUTRAL defaults: a CORE check ships no repo paths. The consumer's
    # catalogue entry supplies roots via from_config().
    roots: ClassVar[tuple[str, ...]] = ()
    extensions: ClassVar[tuple[str, ...]] = (".py",)

    @_mutmut_mutated(mutants_xǁFitnessRuleǁ__init____mutmut)
    def __init__(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = roots if roots is not None else self.roots
        self._extensions: tuple[str, ...] = extensions if extensions is not None else self.extensions
        self._name: str = name if name is not None else self.name

    def xǁFitnessRuleǁ__init____mutmut_orig(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = roots if roots is not None else self.roots
        self._extensions: tuple[str, ...] = extensions if extensions is not None else self.extensions
        self._name: str = name if name is not None else self.name

    def xǁFitnessRuleǁ__init____mutmut_1(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = None
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = roots if roots is not None else self.roots
        self._extensions: tuple[str, ...] = extensions if extensions is not None else self.extensions
        self._name: str = name if name is not None else self.name

    def xǁFitnessRuleǁ__init____mutmut_2(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = roots if roots is not None else self.roots
        self._extensions: tuple[str, ...] = extensions if extensions is not None else self.extensions
        self._name: str = name if name is not None else self.name

    def xǁFitnessRuleǁ__init____mutmut_3(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = None
        self._roots: tuple[str, ...] = roots if roots is not None else self.roots
        self._extensions: tuple[str, ...] = extensions if extensions is not None else self.extensions
        self._name: str = name if name is not None else self.name

    def xǁFitnessRuleǁ__init____mutmut_4(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = None
        self._extensions: tuple[str, ...] = extensions if extensions is not None else self.extensions
        self._name: str = name if name is not None else self.name

    def xǁFitnessRuleǁ__init____mutmut_5(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = roots if roots is None else self.roots
        self._extensions: tuple[str, ...] = extensions if extensions is not None else self.extensions
        self._name: str = name if name is not None else self.name

    def xǁFitnessRuleǁ__init____mutmut_6(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = roots if roots is not None else self.roots
        self._extensions: tuple[str, ...] = None
        self._name: str = name if name is not None else self.name

    def xǁFitnessRuleǁ__init____mutmut_7(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = roots if roots is not None else self.roots
        self._extensions: tuple[str, ...] = extensions if extensions is None else self.extensions
        self._name: str = name if name is not None else self.name

    def xǁFitnessRuleǁ__init____mutmut_8(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = roots if roots is not None else self.roots
        self._extensions: tuple[str, ...] = extensions if extensions is not None else self.extensions
        self._name: str = None

    def xǁFitnessRuleǁ__init____mutmut_9(
        self,
        repo_root: Path | None = None,
        *,
        roots: tuple[str, ...] | None = None,
        extensions: tuple[str, ...] | None = None,
        name: str | None = None,
    ) -> None:
        """Construct a rule instance, overriding class-level config per call.

        ``repo_root`` overrides the default :data:`tc_fitness.REPO_ROOT` (tests
        pass a ``tmp_path`` for isolation). The keyword config overrides
        (``roots`` / ``extensions`` / ``name``) let a
        consumer bind the shared CORE check to its own paths without
        subclassing; ``None`` keeps the class attribute.
        """
        # Resolve the root so symlinked roots (e.g. macOS /tmp → /private/tmp)
        # match the resolved enumerated paths in _repo_relative; an unresolved
        # root would make relative_to() raise and silently fall back to the
        # absolute path, which then fails every is_in_scope() prefix test.
        raw_root = repo_root if repo_root is not None else REPO_ROOT
        self._repo_root: Path = raw_root.resolve()
        self._roots: tuple[str, ...] = roots if roots is not None else self.roots
        self._extensions: tuple[str, ...] = extensions if extensions is not None else self.extensions
        self._name: str = name if name is None else self.name

    @classmethod
    @_mutmut_mutated(mutants_xǁFitnessRuleǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = None
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get(None)
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("XXrootsXX")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("ROOTS")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = None
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get(None)
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("XXextensionsXX")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("EXTENSIONS")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = None
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(None)
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS | set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(None))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(None)
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(None)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{'XX, XX'.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=None,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=None,
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(None) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(None) if extensions is not None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is None else None,
            name=config.get("name"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get(None),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("XXnameXX"),
        )

    @classmethod
    def xǁFitnessRuleǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> FitnessRule:
        """Build an instance from a consumer's ``[tool.tc_fitness]`` config dict.

        Recognised keys (all optional — each falls back to the class attribute):

        * ``roots`` — list of repo-relative scan-root prefixes.
        * ``extensions`` — list of in-scope filename extensions.
        * ``name`` — override the canonical check name.

        Unknown keys are ignored (a consumer may carry rule-specific knobs the
        subclass reads itself). Repo-agnostic: the engine never inspects the
        VALUES for repo identity.
        """
        roots = config.get("roots")
        extensions = config.get("extensions")
        removed = sorted(_REMOVED_SUPPRESSION_OPTIONS & set(config))
        if removed:
            raise ValueError(f"{', '.join(removed)} is not supported: fitness findings cannot be suppressed")
        return cls(
            repo_root=repo_root,
            roots=tuple(roots) if roots is not None else None,
            extensions=tuple(extensions) if extensions is not None else None,
            name=config.get("NAME"),
        )

    @abstractmethod
    def file_has_violation(self, path: Path) -> bool:
        """Return True when the file at ``path`` violates this rule."""

    @_mutmut_mutated(mutants_xǁFitnessRuleǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        """Default scope predicate: under a configured root AND a matching ext.

        When ``roots`` is empty the predicate matches on extension alone, so a
        consumer that drives enumeration entirely from config still scopes
        correctly. Override for non-path scopes (single-file scans, ``.feature``
        files).
        """
        ext_ok = rel.endswith(self._extensions)
        if not self._roots:
            return ext_ok
        return ext_ok and any(rel.startswith(prefix) for prefix in self._roots)

    def xǁFitnessRuleǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        """Default scope predicate: under a configured root AND a matching ext.

        When ``roots`` is empty the predicate matches on extension alone, so a
        consumer that drives enumeration entirely from config still scopes
        correctly. Override for non-path scopes (single-file scans, ``.feature``
        files).
        """
        ext_ok = rel.endswith(self._extensions)
        if not self._roots:
            return ext_ok
        return ext_ok and any(rel.startswith(prefix) for prefix in self._roots)

    def xǁFitnessRuleǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        """Default scope predicate: under a configured root AND a matching ext.

        When ``roots`` is empty the predicate matches on extension alone, so a
        consumer that drives enumeration entirely from config still scopes
        correctly. Override for non-path scopes (single-file scans, ``.feature``
        files).
        """
        ext_ok = None
        if not self._roots:
            return ext_ok
        return ext_ok and any(rel.startswith(prefix) for prefix in self._roots)

    def xǁFitnessRuleǁis_in_scope__mutmut_2(self, rel: str) -> bool:
        """Default scope predicate: under a configured root AND a matching ext.

        When ``roots`` is empty the predicate matches on extension alone, so a
        consumer that drives enumeration entirely from config still scopes
        correctly. Override for non-path scopes (single-file scans, ``.feature``
        files).
        """
        ext_ok = rel.endswith(None)
        if not self._roots:
            return ext_ok
        return ext_ok and any(rel.startswith(prefix) for prefix in self._roots)

    def xǁFitnessRuleǁis_in_scope__mutmut_3(self, rel: str) -> bool:
        """Default scope predicate: under a configured root AND a matching ext.

        When ``roots`` is empty the predicate matches on extension alone, so a
        consumer that drives enumeration entirely from config still scopes
        correctly. Override for non-path scopes (single-file scans, ``.feature``
        files).
        """
        ext_ok = rel.endswith(self._extensions)
        if self._roots:
            return ext_ok
        return ext_ok and any(rel.startswith(prefix) for prefix in self._roots)

    def xǁFitnessRuleǁis_in_scope__mutmut_4(self, rel: str) -> bool:
        """Default scope predicate: under a configured root AND a matching ext.

        When ``roots`` is empty the predicate matches on extension alone, so a
        consumer that drives enumeration entirely from config still scopes
        correctly. Override for non-path scopes (single-file scans, ``.feature``
        files).
        """
        ext_ok = rel.endswith(self._extensions)
        if not self._roots:
            return ext_ok
        return ext_ok or any(rel.startswith(prefix) for prefix in self._roots)

    def xǁFitnessRuleǁis_in_scope__mutmut_5(self, rel: str) -> bool:
        """Default scope predicate: under a configured root AND a matching ext.

        When ``roots`` is empty the predicate matches on extension alone, so a
        consumer that drives enumeration entirely from config still scopes
        correctly. Override for non-path scopes (single-file scans, ``.feature``
        files).
        """
        ext_ok = rel.endswith(self._extensions)
        if not self._roots:
            return ext_ok
        return ext_ok and any(None)

    def xǁFitnessRuleǁis_in_scope__mutmut_6(self, rel: str) -> bool:
        """Default scope predicate: under a configured root AND a matching ext.

        When ``roots`` is empty the predicate matches on extension alone, so a
        consumer that drives enumeration entirely from config still scopes
        correctly. Override for non-path scopes (single-file scans, ``.feature``
        files).
        """
        ext_ok = rel.endswith(self._extensions)
        if not self._roots:
            return ext_ok
        return ext_ok and any(rel.startswith(None) for prefix in self._roots)

    @_mutmut_mutated(mutants_xǁFitnessRuleǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Default enumeration: the git-tracked, in-scope files under the repo root.

        Empty ``roots`` enumerate NOTHING by default: with no configured scan
        root the default enumeration yields ``[]``, so a check run against the
        class-default config (``_roots == ()``) scans no files. A check that
        means to scan by extension alone must configure a root (e.g. ``roots``
        with an empty-prefix entry, which :meth:`is_in_scope` matches on every
        path) or override :meth:`enumerate_files`. The ``is_in_scope``
        "empty roots match on extension alone" rule is the scope PREDICATE, not
        the default enumeration.

        With a configured root, enumerates from ``git ls-files`` — exactly the
        set a fresh checkout materialises — so untracked and ``.gitignore``-d
        build/vendor residue (pnpm ``node_modules/.ignored`` trash, vendored test
        fixtures) is never scanned. This keeps a local run's verdict identical to
        CI's, which only ever sees tracked files. Returns absolute paths, filtered
        by :meth:`is_in_scope`.

        Fallback: when the repo root is not a git working tree (e.g. an unpacked
        source tarball) or ``git`` is unavailable, :meth:`_walk_working_tree`
        rglob-walks the configured roots, skipping ``__pycache__`` and any
        ``node_modules`` segment so vendor residue cannot trip a non-git scan
        either.

        Override for custom enumeration (Gherkin parsing, single-file scans).
        """
        if not self._roots:
            return []
        tracked = self._git_tracked_files()
        if tracked is not None:
            return [self._repo_root / rel for rel in tracked if self.is_in_scope(rel)]
        return self._walk_working_tree()

    def xǁFitnessRuleǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Default enumeration: the git-tracked, in-scope files under the repo root.

        Empty ``roots`` enumerate NOTHING by default: with no configured scan
        root the default enumeration yields ``[]``, so a check run against the
        class-default config (``_roots == ()``) scans no files. A check that
        means to scan by extension alone must configure a root (e.g. ``roots``
        with an empty-prefix entry, which :meth:`is_in_scope` matches on every
        path) or override :meth:`enumerate_files`. The ``is_in_scope``
        "empty roots match on extension alone" rule is the scope PREDICATE, not
        the default enumeration.

        With a configured root, enumerates from ``git ls-files`` — exactly the
        set a fresh checkout materialises — so untracked and ``.gitignore``-d
        build/vendor residue (pnpm ``node_modules/.ignored`` trash, vendored test
        fixtures) is never scanned. This keeps a local run's verdict identical to
        CI's, which only ever sees tracked files. Returns absolute paths, filtered
        by :meth:`is_in_scope`.

        Fallback: when the repo root is not a git working tree (e.g. an unpacked
        source tarball) or ``git`` is unavailable, :meth:`_walk_working_tree`
        rglob-walks the configured roots, skipping ``__pycache__`` and any
        ``node_modules`` segment so vendor residue cannot trip a non-git scan
        either.

        Override for custom enumeration (Gherkin parsing, single-file scans).
        """
        if not self._roots:
            return []
        tracked = self._git_tracked_files()
        if tracked is not None:
            return [self._repo_root / rel for rel in tracked if self.is_in_scope(rel)]
        return self._walk_working_tree()

    def xǁFitnessRuleǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Default enumeration: the git-tracked, in-scope files under the repo root.

        Empty ``roots`` enumerate NOTHING by default: with no configured scan
        root the default enumeration yields ``[]``, so a check run against the
        class-default config (``_roots == ()``) scans no files. A check that
        means to scan by extension alone must configure a root (e.g. ``roots``
        with an empty-prefix entry, which :meth:`is_in_scope` matches on every
        path) or override :meth:`enumerate_files`. The ``is_in_scope``
        "empty roots match on extension alone" rule is the scope PREDICATE, not
        the default enumeration.

        With a configured root, enumerates from ``git ls-files`` — exactly the
        set a fresh checkout materialises — so untracked and ``.gitignore``-d
        build/vendor residue (pnpm ``node_modules/.ignored`` trash, vendored test
        fixtures) is never scanned. This keeps a local run's verdict identical to
        CI's, which only ever sees tracked files. Returns absolute paths, filtered
        by :meth:`is_in_scope`.

        Fallback: when the repo root is not a git working tree (e.g. an unpacked
        source tarball) or ``git`` is unavailable, :meth:`_walk_working_tree`
        rglob-walks the configured roots, skipping ``__pycache__`` and any
        ``node_modules`` segment so vendor residue cannot trip a non-git scan
        either.

        Override for custom enumeration (Gherkin parsing, single-file scans).
        """
        if self._roots:
            return []
        tracked = self._git_tracked_files()
        if tracked is not None:
            return [self._repo_root / rel for rel in tracked if self.is_in_scope(rel)]
        return self._walk_working_tree()

    def xǁFitnessRuleǁenumerate_files__mutmut_2(self) -> list[Path]:
        """Default enumeration: the git-tracked, in-scope files under the repo root.

        Empty ``roots`` enumerate NOTHING by default: with no configured scan
        root the default enumeration yields ``[]``, so a check run against the
        class-default config (``_roots == ()``) scans no files. A check that
        means to scan by extension alone must configure a root (e.g. ``roots``
        with an empty-prefix entry, which :meth:`is_in_scope` matches on every
        path) or override :meth:`enumerate_files`. The ``is_in_scope``
        "empty roots match on extension alone" rule is the scope PREDICATE, not
        the default enumeration.

        With a configured root, enumerates from ``git ls-files`` — exactly the
        set a fresh checkout materialises — so untracked and ``.gitignore``-d
        build/vendor residue (pnpm ``node_modules/.ignored`` trash, vendored test
        fixtures) is never scanned. This keeps a local run's verdict identical to
        CI's, which only ever sees tracked files. Returns absolute paths, filtered
        by :meth:`is_in_scope`.

        Fallback: when the repo root is not a git working tree (e.g. an unpacked
        source tarball) or ``git`` is unavailable, :meth:`_walk_working_tree`
        rglob-walks the configured roots, skipping ``__pycache__`` and any
        ``node_modules`` segment so vendor residue cannot trip a non-git scan
        either.

        Override for custom enumeration (Gherkin parsing, single-file scans).
        """
        if not self._roots:
            return []
        tracked = None
        if tracked is not None:
            return [self._repo_root / rel for rel in tracked if self.is_in_scope(rel)]
        return self._walk_working_tree()

    def xǁFitnessRuleǁenumerate_files__mutmut_3(self) -> list[Path]:
        """Default enumeration: the git-tracked, in-scope files under the repo root.

        Empty ``roots`` enumerate NOTHING by default: with no configured scan
        root the default enumeration yields ``[]``, so a check run against the
        class-default config (``_roots == ()``) scans no files. A check that
        means to scan by extension alone must configure a root (e.g. ``roots``
        with an empty-prefix entry, which :meth:`is_in_scope` matches on every
        path) or override :meth:`enumerate_files`. The ``is_in_scope``
        "empty roots match on extension alone" rule is the scope PREDICATE, not
        the default enumeration.

        With a configured root, enumerates from ``git ls-files`` — exactly the
        set a fresh checkout materialises — so untracked and ``.gitignore``-d
        build/vendor residue (pnpm ``node_modules/.ignored`` trash, vendored test
        fixtures) is never scanned. This keeps a local run's verdict identical to
        CI's, which only ever sees tracked files. Returns absolute paths, filtered
        by :meth:`is_in_scope`.

        Fallback: when the repo root is not a git working tree (e.g. an unpacked
        source tarball) or ``git`` is unavailable, :meth:`_walk_working_tree`
        rglob-walks the configured roots, skipping ``__pycache__`` and any
        ``node_modules`` segment so vendor residue cannot trip a non-git scan
        either.

        Override for custom enumeration (Gherkin parsing, single-file scans).
        """
        if not self._roots:
            return []
        tracked = self._git_tracked_files()
        if tracked is None:
            return [self._repo_root / rel for rel in tracked if self.is_in_scope(rel)]
        return self._walk_working_tree()

    def xǁFitnessRuleǁenumerate_files__mutmut_4(self) -> list[Path]:
        """Default enumeration: the git-tracked, in-scope files under the repo root.

        Empty ``roots`` enumerate NOTHING by default: with no configured scan
        root the default enumeration yields ``[]``, so a check run against the
        class-default config (``_roots == ()``) scans no files. A check that
        means to scan by extension alone must configure a root (e.g. ``roots``
        with an empty-prefix entry, which :meth:`is_in_scope` matches on every
        path) or override :meth:`enumerate_files`. The ``is_in_scope``
        "empty roots match on extension alone" rule is the scope PREDICATE, not
        the default enumeration.

        With a configured root, enumerates from ``git ls-files`` — exactly the
        set a fresh checkout materialises — so untracked and ``.gitignore``-d
        build/vendor residue (pnpm ``node_modules/.ignored`` trash, vendored test
        fixtures) is never scanned. This keeps a local run's verdict identical to
        CI's, which only ever sees tracked files. Returns absolute paths, filtered
        by :meth:`is_in_scope`.

        Fallback: when the repo root is not a git working tree (e.g. an unpacked
        source tarball) or ``git`` is unavailable, :meth:`_walk_working_tree`
        rglob-walks the configured roots, skipping ``__pycache__`` and any
        ``node_modules`` segment so vendor residue cannot trip a non-git scan
        either.

        Override for custom enumeration (Gherkin parsing, single-file scans).
        """
        if not self._roots:
            return []
        tracked = self._git_tracked_files()
        if tracked is not None:
            return [self._repo_root * rel for rel in tracked if self.is_in_scope(rel)]
        return self._walk_working_tree()

    def xǁFitnessRuleǁenumerate_files__mutmut_5(self) -> list[Path]:
        """Default enumeration: the git-tracked, in-scope files under the repo root.

        Empty ``roots`` enumerate NOTHING by default: with no configured scan
        root the default enumeration yields ``[]``, so a check run against the
        class-default config (``_roots == ()``) scans no files. A check that
        means to scan by extension alone must configure a root (e.g. ``roots``
        with an empty-prefix entry, which :meth:`is_in_scope` matches on every
        path) or override :meth:`enumerate_files`. The ``is_in_scope``
        "empty roots match on extension alone" rule is the scope PREDICATE, not
        the default enumeration.

        With a configured root, enumerates from ``git ls-files`` — exactly the
        set a fresh checkout materialises — so untracked and ``.gitignore``-d
        build/vendor residue (pnpm ``node_modules/.ignored`` trash, vendored test
        fixtures) is never scanned. This keeps a local run's verdict identical to
        CI's, which only ever sees tracked files. Returns absolute paths, filtered
        by :meth:`is_in_scope`.

        Fallback: when the repo root is not a git working tree (e.g. an unpacked
        source tarball) or ``git`` is unavailable, :meth:`_walk_working_tree`
        rglob-walks the configured roots, skipping ``__pycache__`` and any
        ``node_modules`` segment so vendor residue cannot trip a non-git scan
        either.

        Override for custom enumeration (Gherkin parsing, single-file scans).
        """
        if not self._roots:
            return []
        tracked = self._git_tracked_files()
        if tracked is not None:
            return [self._repo_root / rel for rel in tracked if self.is_in_scope(None)]
        return self._walk_working_tree()

    @_mutmut_mutated(mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut)
    def _git_tracked_files(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_orig(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_1(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = None
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_2(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                None,
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_3(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=None,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_4(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=None,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_5(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=None,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_6(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_7(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_8(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_9(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_10(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["XXgitXX", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_11(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["GIT", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_12(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "XX-CXX", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_13(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-c", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_14(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(None), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_15(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "XXls-filesXX", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_16(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "LS-FILES", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_17(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "XX-zXX"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_18(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-Z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_19(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=False,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_20(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=False,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_21(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode(None, "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_22(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", None) for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_23(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_24(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", ) for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_25(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("XXutf-8XX", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_26(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("UTF-8", "surrogateescape") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_27(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "XXsurrogateescapeXX") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_28(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "SURROGATEESCAPE") for rel in result.stdout.split(b"\x00") if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_29(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(None) if rel]

    def xǁFitnessRuleǁ_git_tracked_files__mutmut_30(self) -> list[str] | None:
        """Repo-relative paths of every git-tracked file, or ``None`` off-git.

        Runs ``git -C <repo_root> ls-files -z`` and returns the NUL-split,
        repo-relative tracked paths. Returns ``None`` — the signal to fall back
        to a working-tree walk — when the repo root is not a git working tree
        (``git`` exits non-zero) or ``git`` is unavailable / wedged. argv0 is the
        fixed literal ``git`` and ``shell`` is never used; the only variable is
        the repo-root path.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._repo_root), "ls-files", "-z"],
                check=True,
                capture_output=True,
                timeout=_GIT_LS_FILES_TIMEOUT_S,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        return [rel.decode("utf-8", "surrogateescape") for rel in result.stdout.split(b"XX\x00XX") if rel]

    @_mutmut_mutated(mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut)
    def _walk_working_tree(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_orig(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_1(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = None
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_2(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = None
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_3(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root * root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_4(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_5(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                break
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_6(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob(None):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_7(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("XX*XX"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_8(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_9(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    break
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_10(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts and "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_11(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "XX__pycache__XX" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_12(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__PYCACHE__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_13(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" not in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_14(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "XXnode_modulesXX" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_15(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "NODE_MODULES" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_16(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" not in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_17(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    break
                if path.name.endswith(self._extensions):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_18(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(None):
                    out.append(path)
        return out

    def xǁFitnessRuleǁ_walk_working_tree__mutmut_19(self) -> list[Path]:
        """Off-git fallback: rglob each configured root, skipping vendor residue.

        Skips ``__pycache__`` and any ``node_modules`` segment so untracked
        vendor residue cannot trip a scan that has no git tree to filter by.
        Returns absolute paths.
        """
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.exists():
                continue
            for path in root_path.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or "node_modules" in path.parts:
                    continue
                if path.name.endswith(self._extensions):
                    out.append(None)
        return out

    @_mutmut_mutated(mutants_xǁFitnessRuleǁ_repo_relative__mutmut)
    def _repo_relative(self, path: Path) -> Path:
        """Repo-relative path; tolerates absolute or already-relative inputs."""
        if path.is_absolute():
            try:
                return path.resolve().relative_to(self._repo_root)
            except ValueError:
                pass
        return path

    def xǁFitnessRuleǁ_repo_relative__mutmut_orig(self, path: Path) -> Path:
        """Repo-relative path; tolerates absolute or already-relative inputs."""
        if path.is_absolute():
            try:
                return path.resolve().relative_to(self._repo_root)
            except ValueError:
                pass
        return path

    def xǁFitnessRuleǁ_repo_relative__mutmut_1(self, path: Path) -> Path:
        """Repo-relative path; tolerates absolute or already-relative inputs."""
        if path.is_absolute():
            try:
                return path.resolve().relative_to(None)
            except ValueError:
                pass
        return path

    @_mutmut_mutated(mutants_xǁFitnessRuleǁcollect_violations__mutmut)
    def collect_violations(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = str(rel_path)
            if not self.is_in_scope(rel):
                continue
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_orig(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = str(rel_path)
            if not self.is_in_scope(rel):
                continue
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_1(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = None
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = str(rel_path)
            if not self.is_in_scope(rel):
                continue
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_2(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = None
            rel = str(rel_path)
            if not self.is_in_scope(rel):
                continue
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_3(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(None)
            rel = str(rel_path)
            if not self.is_in_scope(rel):
                continue
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_4(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = None
            if not self.is_in_scope(rel):
                continue
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_5(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = str(None)
            if not self.is_in_scope(rel):
                continue
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_6(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = str(rel_path)
            if self.is_in_scope(rel):
                continue
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_7(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = str(rel_path)
            if not self.is_in_scope(None):
                continue
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_8(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = str(rel_path)
            if not self.is_in_scope(rel):
                break
            if self.file_has_violation(path):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_9(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = str(rel_path)
            if not self.is_in_scope(rel):
                continue
            if self.file_has_violation(None):
                out.add(rel_path)
        return out

    def xǁFitnessRuleǁcollect_violations__mutmut_10(self) -> set[Path]:
        """Walk in-scope files; return the repo-relative paths that violate.

        Out-of-scope files are skipped. Every returned path is a hard finding.
        """
        out: set[Path] = set()
        for path in self.enumerate_files():
            rel_path = self._repo_relative(path)
            rel = str(rel_path)
            if not self.is_in_scope(rel):
                continue
            if self.file_has_violation(path):
                out.add(None)
        return out

    @_mutmut_mutated(mutants_xǁFitnessRuleǁrun__mutmut)
    def run(self) -> int:
        """Return ``1`` when any current violation exists, otherwise ``0``."""
        return gate(
            self._name,
            self.collect_violations(),
            self.remediation,
            repo_root=self._repo_root,
        )

    def xǁFitnessRuleǁrun__mutmut_orig(self) -> int:
        """Return ``1`` when any current violation exists, otherwise ``0``."""
        return gate(
            self._name,
            self.collect_violations(),
            self.remediation,
            repo_root=self._repo_root,
        )

    def xǁFitnessRuleǁrun__mutmut_1(self) -> int:
        """Return ``1`` when any current violation exists, otherwise ``0``."""
        return gate(
            None,
            self.collect_violations(),
            self.remediation,
            repo_root=self._repo_root,
        )

    def xǁFitnessRuleǁrun__mutmut_2(self) -> int:
        """Return ``1`` when any current violation exists, otherwise ``0``."""
        return gate(
            self._name,
            None,
            self.remediation,
            repo_root=self._repo_root,
        )

    def xǁFitnessRuleǁrun__mutmut_3(self) -> int:
        """Return ``1`` when any current violation exists, otherwise ``0``."""
        return gate(
            self._name,
            self.collect_violations(),
            None,
            repo_root=self._repo_root,
        )

    def xǁFitnessRuleǁrun__mutmut_4(self) -> int:
        """Return ``1`` when any current violation exists, otherwise ``0``."""
        return gate(
            self._name,
            self.collect_violations(),
            self.remediation,
            repo_root=None,
        )

    def xǁFitnessRuleǁrun__mutmut_5(self) -> int:
        """Return ``1`` when any current violation exists, otherwise ``0``."""
        return gate(
            self.collect_violations(),
            self.remediation,
            repo_root=self._repo_root,
        )

    def xǁFitnessRuleǁrun__mutmut_6(self) -> int:
        """Return ``1`` when any current violation exists, otherwise ``0``."""
        return gate(
            self._name,
            self.remediation,
            repo_root=self._repo_root,
        )

    def xǁFitnessRuleǁrun__mutmut_7(self) -> int:
        """Return ``1`` when any current violation exists, otherwise ``0``."""
        return gate(
            self._name,
            self.collect_violations(),
            repo_root=self._repo_root,
        )

    def xǁFitnessRuleǁrun__mutmut_8(self) -> int:
        """Return ``1`` when any current violation exists, otherwise ``0``."""
        return gate(
            self._name,
            self.collect_violations(),
            self.remediation,
            )

mutants_xǁFitnessRuleǁ__init____mutmut['_mutmut_orig'] = FitnessRule.xǁFitnessRuleǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ__init____mutmut['xǁFitnessRuleǁ__init____mutmut_1'] = FitnessRule.xǁFitnessRuleǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ__init____mutmut['xǁFitnessRuleǁ__init____mutmut_2'] = FitnessRule.xǁFitnessRuleǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ__init____mutmut['xǁFitnessRuleǁ__init____mutmut_3'] = FitnessRule.xǁFitnessRuleǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ__init____mutmut['xǁFitnessRuleǁ__init____mutmut_4'] = FitnessRule.xǁFitnessRuleǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ__init____mutmut['xǁFitnessRuleǁ__init____mutmut_5'] = FitnessRule.xǁFitnessRuleǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ__init____mutmut['xǁFitnessRuleǁ__init____mutmut_6'] = FitnessRule.xǁFitnessRuleǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ__init____mutmut['xǁFitnessRuleǁ__init____mutmut_7'] = FitnessRule.xǁFitnessRuleǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ__init____mutmut['xǁFitnessRuleǁ__init____mutmut_8'] = FitnessRule.xǁFitnessRuleǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ__init____mutmut['xǁFitnessRuleǁ__init____mutmut_9'] = FitnessRule.xǁFitnessRuleǁ__init____mutmut_9 # type: ignore # mutmut generated

mutants_xǁFitnessRuleǁfrom_config__mutmut['_mutmut_orig'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_1'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_2'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_3'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_4'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_5'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_6'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_7'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_8'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_9'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_10'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_11'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_12'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_13'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_14'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_15'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_16'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_17'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_18'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_19'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_20'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_21'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_22'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_23'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_24'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_25'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_26'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_27'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_28'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_29'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁfrom_config__mutmut['xǁFitnessRuleǁfrom_config__mutmut_30'] = FitnessRule.xǁFitnessRuleǁfrom_config__mutmut_30 # type: ignore # mutmut generated

mutants_xǁFitnessRuleǁis_in_scope__mutmut['_mutmut_orig'] = FitnessRule.xǁFitnessRuleǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁis_in_scope__mutmut['xǁFitnessRuleǁis_in_scope__mutmut_1'] = FitnessRule.xǁFitnessRuleǁis_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁis_in_scope__mutmut['xǁFitnessRuleǁis_in_scope__mutmut_2'] = FitnessRule.xǁFitnessRuleǁis_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁis_in_scope__mutmut['xǁFitnessRuleǁis_in_scope__mutmut_3'] = FitnessRule.xǁFitnessRuleǁis_in_scope__mutmut_3 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁis_in_scope__mutmut['xǁFitnessRuleǁis_in_scope__mutmut_4'] = FitnessRule.xǁFitnessRuleǁis_in_scope__mutmut_4 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁis_in_scope__mutmut['xǁFitnessRuleǁis_in_scope__mutmut_5'] = FitnessRule.xǁFitnessRuleǁis_in_scope__mutmut_5 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁis_in_scope__mutmut['xǁFitnessRuleǁis_in_scope__mutmut_6'] = FitnessRule.xǁFitnessRuleǁis_in_scope__mutmut_6 # type: ignore # mutmut generated

mutants_xǁFitnessRuleǁenumerate_files__mutmut['_mutmut_orig'] = FitnessRule.xǁFitnessRuleǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁenumerate_files__mutmut['xǁFitnessRuleǁenumerate_files__mutmut_1'] = FitnessRule.xǁFitnessRuleǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁenumerate_files__mutmut['xǁFitnessRuleǁenumerate_files__mutmut_2'] = FitnessRule.xǁFitnessRuleǁenumerate_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁenumerate_files__mutmut['xǁFitnessRuleǁenumerate_files__mutmut_3'] = FitnessRule.xǁFitnessRuleǁenumerate_files__mutmut_3 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁenumerate_files__mutmut['xǁFitnessRuleǁenumerate_files__mutmut_4'] = FitnessRule.xǁFitnessRuleǁenumerate_files__mutmut_4 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁenumerate_files__mutmut['xǁFitnessRuleǁenumerate_files__mutmut_5'] = FitnessRule.xǁFitnessRuleǁenumerate_files__mutmut_5 # type: ignore # mutmut generated

mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['_mutmut_orig'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_1'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_2'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_3'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_3 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_4'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_4 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_5'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_5 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_6'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_6 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_7'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_7 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_8'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_8 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_9'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_9 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_10'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_10 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_11'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_11 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_12'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_12 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_13'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_13 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_14'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_14 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_15'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_15 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_16'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_16 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_17'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_17 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_18'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_18 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_19'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_19 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_20'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_20 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_21'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_21 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_22'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_22 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_23'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_23 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_24'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_24 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_25'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_25 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_26'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_26 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_27'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_27 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_28'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_28 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_29'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_29 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_git_tracked_files__mutmut['xǁFitnessRuleǁ_git_tracked_files__mutmut_30'] = FitnessRule.xǁFitnessRuleǁ_git_tracked_files__mutmut_30 # type: ignore # mutmut generated

mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['_mutmut_orig'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_orig # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_1'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_1 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_2'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_2 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_3'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_3 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_4'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_4 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_5'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_5 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_6'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_6 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_7'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_7 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_8'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_8 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_9'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_9 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_10'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_10 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_11'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_11 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_12'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_12 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_13'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_13 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_14'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_14 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_15'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_15 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_16'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_16 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_17'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_17 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_18'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_18 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_walk_working_tree__mutmut['xǁFitnessRuleǁ_walk_working_tree__mutmut_19'] = FitnessRule.xǁFitnessRuleǁ_walk_working_tree__mutmut_19 # type: ignore # mutmut generated

mutants_xǁFitnessRuleǁ_repo_relative__mutmut['_mutmut_orig'] = FitnessRule.xǁFitnessRuleǁ_repo_relative__mutmut_orig # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁ_repo_relative__mutmut['xǁFitnessRuleǁ_repo_relative__mutmut_1'] = FitnessRule.xǁFitnessRuleǁ_repo_relative__mutmut_1 # type: ignore # mutmut generated

mutants_xǁFitnessRuleǁcollect_violations__mutmut['_mutmut_orig'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_orig # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁcollect_violations__mutmut['xǁFitnessRuleǁcollect_violations__mutmut_1'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_1 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁcollect_violations__mutmut['xǁFitnessRuleǁcollect_violations__mutmut_2'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_2 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁcollect_violations__mutmut['xǁFitnessRuleǁcollect_violations__mutmut_3'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_3 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁcollect_violations__mutmut['xǁFitnessRuleǁcollect_violations__mutmut_4'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_4 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁcollect_violations__mutmut['xǁFitnessRuleǁcollect_violations__mutmut_5'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_5 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁcollect_violations__mutmut['xǁFitnessRuleǁcollect_violations__mutmut_6'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_6 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁcollect_violations__mutmut['xǁFitnessRuleǁcollect_violations__mutmut_7'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_7 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁcollect_violations__mutmut['xǁFitnessRuleǁcollect_violations__mutmut_8'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_8 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁcollect_violations__mutmut['xǁFitnessRuleǁcollect_violations__mutmut_9'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_9 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁcollect_violations__mutmut['xǁFitnessRuleǁcollect_violations__mutmut_10'] = FitnessRule.xǁFitnessRuleǁcollect_violations__mutmut_10 # type: ignore # mutmut generated

mutants_xǁFitnessRuleǁrun__mutmut['_mutmut_orig'] = FitnessRule.xǁFitnessRuleǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁrun__mutmut['xǁFitnessRuleǁrun__mutmut_1'] = FitnessRule.xǁFitnessRuleǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁrun__mutmut['xǁFitnessRuleǁrun__mutmut_2'] = FitnessRule.xǁFitnessRuleǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁrun__mutmut['xǁFitnessRuleǁrun__mutmut_3'] = FitnessRule.xǁFitnessRuleǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁrun__mutmut['xǁFitnessRuleǁrun__mutmut_4'] = FitnessRule.xǁFitnessRuleǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁrun__mutmut['xǁFitnessRuleǁrun__mutmut_5'] = FitnessRule.xǁFitnessRuleǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁrun__mutmut['xǁFitnessRuleǁrun__mutmut_6'] = FitnessRule.xǁFitnessRuleǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁrun__mutmut['xǁFitnessRuleǁrun__mutmut_7'] = FitnessRule.xǁFitnessRuleǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁFitnessRuleǁrun__mutmut['xǁFitnessRuleǁrun__mutmut_8'] = FitnessRule.xǁFitnessRuleǁrun__mutmut_8 # type: ignore # mutmut generated


__all__ = ["FitnessRule"]
