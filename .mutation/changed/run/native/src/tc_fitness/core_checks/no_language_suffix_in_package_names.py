"""CORE check: no_language_suffix_in_package_names — names describe work, not tech.

A public package boundary (an MCP server, a shared library, a plugin, a service,
a published skill, a workspace package) must carry a name that describes the WORK
it performs. A language suffix (``-py``, ``-ts``, ``-js``, ``-rs``, …) leaks the
implementation choice into the agent-facing surface and couples the name to a
tech decision that may later change. This rule flags any boundary directory whose
immediate name ends in a forbidden language suffix.

The check inspects directory NAMES, never file content. It enumerates the
immediate child directories of each configured boundary root (and, for
marker-gated roots, only leaves carrying a marker file such as ``SKILL.md``) and
flags those ending in a forbidden suffix.

Ported from tc-agent-zone ``scripts/checks/no_language_suffix_in_package_names.py``
(ADR-029 D1+D5) and re-expressed as a configurable, repo-agnostic rule. The donor
hardcoded ``agentic/tools/mcp`` etc. and the SKILL.md marker; here:

* ``boundary_roots`` — prefixes whose immediate child dirs are boundaries.
* ``marker_roots`` — prefixes scanned at depth-2, gating each leaf on a marker.
* ``marker_file`` — the file a marker-root leaf must contain to count.
* ``forbidden_suffixes`` — the language suffixes to ban.

A consumer with no roots configured flags nothing.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Language suffixes that leak implementation into a name. Domain-intrinsic
#: default (ADR-029's own list), overridable via config.
DEFAULT_FORBIDDEN_SUFFIXES: tuple[str, ...] = (
    "-py",
    "-ts",
    "-js",
    "-rs",
    "-go",
    "-cpp",
    "-c",
    "-java",
    "-kt",
)

#: The file a marker-root leaf must carry to count as a published boundary.
DEFAULT_MARKER_FILE = "SKILL.md"

REMEDIATION = _remediation(
    fix=(
        "rename the directory so the name describes the work, not the language "
        "(move the language to a sub-path or drop it). Update every import, "
        "package manifest and workspace member that referenced the old name."
    ),
    nxt="re-run this check to confirm the rename cleared the suffix.",
    run="python -m tc_fitness.core_checks.no_language_suffix_in_package_names",
    passing="render-office-to-pdf/",
    forbidden="render-office-to-pdf-ts/",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__match_suffix__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__match_suffix__mutmut)
def _match_suffix(name: str, suffixes: tuple[str, ...]) -> str | None:
    """Return the forbidden suffix ``name`` ends with, or None."""
    for suffix in suffixes:
        if name.endswith(suffix):
            return suffix
    return None


def x__match_suffix__mutmut_orig(name: str, suffixes: tuple[str, ...]) -> str | None:
    """Return the forbidden suffix ``name`` ends with, or None."""
    for suffix in suffixes:
        if name.endswith(suffix):
            return suffix
    return None


def x__match_suffix__mutmut_1(name: str, suffixes: tuple[str, ...]) -> str | None:
    """Return the forbidden suffix ``name`` ends with, or None."""
    for suffix in suffixes:
        if name.endswith(None):
            return suffix
    return None

mutants_x__match_suffix__mutmut['_mutmut_orig'] = x__match_suffix__mutmut_orig # type: ignore # mutmut generated
mutants_x__match_suffix__mutmut['x__match_suffix__mutmut_1'] = x__match_suffix__mutmut_1 # type: ignore # mutmut generated
mutants_x_name_has_language_suffix__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_name_has_language_suffix__mutmut)
def name_has_language_suffix(name: str, *, suffixes: tuple[str, ...]) -> bool:
    """True iff directory ``name`` ends with a forbidden language suffix.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return _match_suffix(name, suffixes) is not None


def x_name_has_language_suffix__mutmut_orig(name: str, *, suffixes: tuple[str, ...]) -> bool:
    """True iff directory ``name`` ends with a forbidden language suffix.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return _match_suffix(name, suffixes) is not None


def x_name_has_language_suffix__mutmut_1(name: str, *, suffixes: tuple[str, ...]) -> bool:
    """True iff directory ``name`` ends with a forbidden language suffix.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return _match_suffix(None, suffixes) is not None


def x_name_has_language_suffix__mutmut_2(name: str, *, suffixes: tuple[str, ...]) -> bool:
    """True iff directory ``name`` ends with a forbidden language suffix.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return _match_suffix(name, None) is not None


def x_name_has_language_suffix__mutmut_3(name: str, *, suffixes: tuple[str, ...]) -> bool:
    """True iff directory ``name`` ends with a forbidden language suffix.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return _match_suffix(suffixes) is not None


def x_name_has_language_suffix__mutmut_4(name: str, *, suffixes: tuple[str, ...]) -> bool:
    """True iff directory ``name`` ends with a forbidden language suffix.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return _match_suffix(name, ) is not None


def x_name_has_language_suffix__mutmut_5(name: str, *, suffixes: tuple[str, ...]) -> bool:
    """True iff directory ``name`` ends with a forbidden language suffix.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return _match_suffix(name, suffixes) is None

mutants_x_name_has_language_suffix__mutmut['_mutmut_orig'] = x_name_has_language_suffix__mutmut_orig # type: ignore # mutmut generated
mutants_x_name_has_language_suffix__mutmut['x_name_has_language_suffix__mutmut_1'] = x_name_has_language_suffix__mutmut_1 # type: ignore # mutmut generated
mutants_x_name_has_language_suffix__mutmut['x_name_has_language_suffix__mutmut_2'] = x_name_has_language_suffix__mutmut_2 # type: ignore # mutmut generated
mutants_x_name_has_language_suffix__mutmut['x_name_has_language_suffix__mutmut_3'] = x_name_has_language_suffix__mutmut_3 # type: ignore # mutmut generated
mutants_x_name_has_language_suffix__mutmut['x_name_has_language_suffix__mutmut_4'] = x_name_has_language_suffix__mutmut_4 # type: ignore # mutmut generated
mutants_x_name_has_language_suffix__mutmut['x_name_has_language_suffix__mutmut_5'] = x_name_has_language_suffix__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoLanguageSuffixInPackageNamesǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoLanguageSuffixInPackageNames(FitnessRule):
    """Flags boundary directories whose name ends in a language suffix."""

    name = "no-language-suffix-in-package-names"
    remediation = REMEDIATION
    #: This rule scans directory names; the extension filter is unused (its
    #: scope is the boundary roots), so it accepts anything.
    extensions = ()

    boundary_roots: tuple[str, ...] = ()
    marker_roots: tuple[str, ...] = ()
    marker_file: str = DEFAULT_MARKER_FILE
    forbidden_suffixes: tuple[str, ...] = DEFAULT_FORBIDDEN_SUFFIXES

    @classmethod
    @_mutmut_mutated(mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = None
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, )
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = None
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get(None)
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("XXboundary_rootsXX")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("BOUNDARY_ROOTS")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = None
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(None)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = None
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get(None)
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("XXmarker_rootsXX")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("MARKER_ROOTS")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = None
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(None)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = None
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get(None)
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("XXmarker_fileXX")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("MARKER_FILE")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = None
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(None)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = None
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get(None)
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("XXforbidden_suffixesXX")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("FORBIDDEN_SUFFIXES")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_31(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is None:
            rule.forbidden_suffixes = tuple(suffixes)
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_32(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = None
        return rule

    @classmethod
    def xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_33(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoLanguageSuffixInPackageNames:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoLanguageSuffixInPackageNames)  # noqa: S101  # narrowing for mypy
        boundary = config.get("boundary_roots")
        if boundary is not None:
            rule.boundary_roots = tuple(boundary)
        markers = config.get("marker_roots")
        if markers is not None:
            rule.marker_roots = tuple(markers)
        marker_file = config.get("marker_file")
        if marker_file is not None:
            rule.marker_file = str(marker_file)
        suffixes = config.get("forbidden_suffixes")
        if suffixes is not None:
            rule.forbidden_suffixes = tuple(None)
        return rule

    @_mutmut_mutated(mutants_xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut)
    def _visible_child_dirs(self, parent: Path) -> list[Path]:
        return [c for c in sorted(parent.iterdir()) if c.is_dir() and not c.name.startswith(".")]

    def xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_orig(self, parent: Path) -> list[Path]:
        return [c for c in sorted(parent.iterdir()) if c.is_dir() and not c.name.startswith(".")]

    def xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_1(self, parent: Path) -> list[Path]:
        return [c for c in sorted(None) if c.is_dir() and not c.name.startswith(".")]

    def xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_2(self, parent: Path) -> list[Path]:
        return [c for c in sorted(parent.iterdir()) if c.is_dir() or not c.name.startswith(".")]

    def xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_3(self, parent: Path) -> list[Path]:
        return [c for c in sorted(parent.iterdir()) if c.is_dir() and c.name.startswith(".")]

    def xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_4(self, parent: Path) -> list[Path]:
        return [c for c in sorted(parent.iterdir()) if c.is_dir() and not c.name.startswith(None)]

    def xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_5(self, parent: Path) -> list[Path]:
        return [c for c in sorted(parent.iterdir()) if c.is_dir() and not c.name.startswith("XX.XX")]

    @_mutmut_mutated(mutants_xǁNoLanguageSuffixInPackageNamesǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        # Scope is the enumerated boundary directories themselves; every
        # enumerated entry is in scope.
        return True

    def xǁNoLanguageSuffixInPackageNamesǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        # Scope is the enumerated boundary directories themselves; every
        # enumerated entry is in scope.
        return True

    def xǁNoLanguageSuffixInPackageNamesǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        # Scope is the enumerated boundary directories themselves; every
        # enumerated entry is in scope.
        return False

    @_mutmut_mutated(mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = None
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_2(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = None
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_3(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root * boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_4(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_5(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(None)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_6(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(None)
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_7(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(None))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_8(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = None
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_9(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root * marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_10(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_11(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(None)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_12(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                break
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_13(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(None):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_14(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(None):
                    if (leaf / self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_15(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf * self.marker_file).is_file():
                        out.append(leaf)
        return out

    def xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_16(self) -> list[Path]:
        """Enumerate the boundary directories (depth-1 + marker-gated depth-2)."""
        out: list[Path] = []
        for boundary in self.boundary_roots:
            root = self._repo_root / boundary
            if not root.is_dir():
                out.append(root)
            else:
                out.extend(self._visible_child_dirs(root))
        for marker_root in self.marker_roots:
            root = self._repo_root / marker_root
            if not root.is_dir():
                out.append(root)
                continue
            for scope in self._visible_child_dirs(root):
                for leaf in self._visible_child_dirs(scope):
                    if (leaf / self.marker_file).is_file():
                        out.append(None)
        return out

    @_mutmut_mutated(mutants_xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        if not path.is_dir():
            return True
        return name_has_language_suffix(path.name, suffixes=self.forbidden_suffixes)

    def xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        if not path.is_dir():
            return True
        return name_has_language_suffix(path.name, suffixes=self.forbidden_suffixes)

    def xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        if path.is_dir():
            return True
        return name_has_language_suffix(path.name, suffixes=self.forbidden_suffixes)

    def xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        if not path.is_dir():
            return False
        return name_has_language_suffix(path.name, suffixes=self.forbidden_suffixes)

    def xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        if not path.is_dir():
            return True
        return name_has_language_suffix(None, suffixes=self.forbidden_suffixes)

    def xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        if not path.is_dir():
            return True
        return name_has_language_suffix(path.name, suffixes=None)

    def xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        if not path.is_dir():
            return True
        return name_has_language_suffix(suffixes=self.forbidden_suffixes)

    def xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        if not path.is_dir():
            return True
        return name_has_language_suffix(path.name, )

mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['_mutmut_orig'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_1'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_2'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_3'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_4'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_5'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_6'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_7'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_8'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_9'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_10'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_11'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_12'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_13'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_14'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_15'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_16'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_17'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_18'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_19'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_20'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_21'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_22'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_23'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_24'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_25'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_26'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_27'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_28'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_29'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_30'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_30 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_31'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_31 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_32'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_32 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut['xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_33'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfrom_config__mutmut_33 # type: ignore # mutmut generated

mutants_xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut['_mutmut_orig'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut['xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_1'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut['xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_2'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut['xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_3'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut['xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_4'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut['xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_5'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁ_visible_child_dirs__mutmut_5 # type: ignore # mutmut generated

mutants_xǁNoLanguageSuffixInPackageNamesǁis_in_scope__mutmut['_mutmut_orig'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁis_in_scope__mutmut['xǁNoLanguageSuffixInPackageNamesǁis_in_scope__mutmut_1'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁis_in_scope__mutmut_1 # type: ignore # mutmut generated

mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['_mutmut_orig'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_1'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_2'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_3'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_4'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_5'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_6'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_7'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_8'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_9'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_10'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_11'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_12'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_13'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_14'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_15'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut['xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_16'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁenumerate_files__mutmut_16 # type: ignore # mutmut generated

mutants_xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut['_mutmut_orig'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut['xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_1'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut['xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_2'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut['xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_3'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut['xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_4'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut['xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_5'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut['xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_6'] = NoLanguageSuffixInPackageNames.xǁNoLanguageSuffixInPackageNamesǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLanguageSuffixInPackageNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLanguageSuffixInPackageNames.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLanguageSuffixInPackageNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLanguageSuffixInPackageNames.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLanguageSuffixInPackageNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLanguageSuffixInPackageNames.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLanguageSuffixInPackageNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLanguageSuffixInPackageNames.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLanguageSuffixInPackageNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLanguageSuffixInPackageNames.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoLanguageSuffixInPackageNames:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoLanguageSuffixInPackageNames.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoLanguageSuffixInPackageNames, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoLanguageSuffixInPackageNames, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoLanguageSuffixInPackageNames, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoLanguageSuffixInPackageNames, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
