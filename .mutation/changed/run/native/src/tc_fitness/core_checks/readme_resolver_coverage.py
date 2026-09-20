"""CORE check: readme_resolver_coverage — every top-level directory has a resolver.

A repo is navigable when each top-level directory carries a resolver README that
tells a reader what belongs there and what does not. This rule flags any
top-level directory (under the configured scan roots) that is MISSING the
resolver file, so the "where does X live?" affordance stays current as new
top-level domains land.

The violation is an ABSENCE: a scanned directory lacking the resolver file. The
rule enumerates the immediate child directories of each configured root (default
the repo root itself) and flags those without the marker, unless the directory
name is a fixed cache/tooling directory outside the authored information
architecture domain.

Ported from tc-agent-zone ``scripts/checks/repo_ia.py`` (the IA1
``check_top_level_readmes`` gate, FEAT-145) and re-expressed as a configurable,
repo-agnostic rule. The donor hardcoded a fixed exempt set and the ``README.md``
name; here the roots and resolver filename are config:

* ``roots`` — prefixes whose immediate child dirs must each carry the resolver
  (default ``("",)`` — the repo root, i.e. top-level directories).
* ``resolver_file`` — the marker filename a directory must contain.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The resolver marker every scanned directory must carry. Overridable.
DEFAULT_RESOLVER_FILE = "README.md"

#: Cache/tooling directory names that carry no information architecture and are
#: skipped. This is part of the rule definition, not consumer config.
DEFAULT_EXEMPT_DIRS: frozenset[str] = frozenset(
    {
        ".git",
        ".github",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        "node_modules",
        ".venv",
        "logs",
        "htmlcov",
    }
)

REMEDIATION = _remediation(
    fix=(
        "add a resolver README to the directory explaining what belongs there "
        "and what does not, so the 'where does X live?' affordance stays "
        "current."
    ),
    nxt="re-run this check to confirm the directory now resolves.",
    run="python -m tc_fitness.core_checks.readme_resolver_coverage",
    passing="platform/README.md",
    forbidden="platform/   (no README.md)",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_directory_missing_resolver__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_directory_missing_resolver__mutmut)
def directory_missing_resolver(directory: Path, *, resolver_file: str) -> bool:
    """True iff ``directory`` lacks the ``resolver_file`` marker.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return not (directory / resolver_file).is_file()


def x_directory_missing_resolver__mutmut_orig(directory: Path, *, resolver_file: str) -> bool:
    """True iff ``directory`` lacks the ``resolver_file`` marker.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return not (directory / resolver_file).is_file()


def x_directory_missing_resolver__mutmut_1(directory: Path, *, resolver_file: str) -> bool:
    """True iff ``directory`` lacks the ``resolver_file`` marker.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return (directory / resolver_file).is_file()


def x_directory_missing_resolver__mutmut_2(directory: Path, *, resolver_file: str) -> bool:
    """True iff ``directory`` lacks the ``resolver_file`` marker.

    Pure helper (the detection core) so tests can assert on it directly.
    """
    return not (directory * resolver_file).is_file()

mutants_x_directory_missing_resolver__mutmut['_mutmut_orig'] = x_directory_missing_resolver__mutmut_orig # type: ignore # mutmut generated
mutants_x_directory_missing_resolver__mutmut['x_directory_missing_resolver__mutmut_1'] = x_directory_missing_resolver__mutmut_1 # type: ignore # mutmut generated
mutants_x_directory_missing_resolver__mutmut['x_directory_missing_resolver__mutmut_2'] = x_directory_missing_resolver__mutmut_2 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁReadmeResolverCoverageǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁReadmeResolverCoverageǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class ReadmeResolverCoverage(FitnessRule):
    """Flags top-level directories missing a resolver README."""

    name = "readme-resolver-coverage"
    remediation = REMEDIATION
    extensions = ()

    #: Default scan root is the repo root itself ("" prefix), i.e. its
    #: top-level directories. A consumer may point at sub-trees instead.
    #: (No re-annotation — ``roots`` is the base ClassVar; we only set the value.)
    roots = ("",)
    resolver_file: str = DEFAULT_RESOLVER_FILE

    @classmethod
    @_mutmut_mutated(mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("resolver_file")
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("resolver_file")
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = None
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("resolver_file")
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("resolver_file")
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("resolver_file")
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("resolver_file")
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, )
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("resolver_file")
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = None
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get(None)
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("XXresolver_fileXX")
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("RESOLVER_FILE")
        if resolver_file is not None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("resolver_file")
        if resolver_file is None:
            rule.resolver_file = str(resolver_file)
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("resolver_file")
        if resolver_file is not None:
            rule.resolver_file = None
        return rule

    @classmethod
    def xǁReadmeResolverCoverageǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ReadmeResolverCoverage:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ReadmeResolverCoverage)  # noqa: S101  # narrowing for mypy
        resolver_file = config.get("resolver_file")
        if resolver_file is not None:
            rule.resolver_file = str(None)
        return rule

    @_mutmut_mutated(mutants_xǁReadmeResolverCoverageǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        # Scope is the enumerated directories; every enumerated entry is scoped.
        return True

    def xǁReadmeResolverCoverageǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        # Scope is the enumerated directories; every enumerated entry is scoped.
        return True

    def xǁReadmeResolverCoverageǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        # Scope is the enumerated directories; every enumerated entry is scoped.
        return False

    @_mutmut_mutated(mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = None
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_2(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = None
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_3(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root * root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_4(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_5(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                break
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_6(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(None):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_7(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_8(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    break
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_9(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS and child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_10(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name not in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_11(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith(None):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_12(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("XX.XX"):
                    continue
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_13(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    break
                out.append(child)
        return out

    def xǁReadmeResolverCoverageǁenumerate_files__mutmut_14(self) -> list[Path]:
        """Enumerate the immediate child directories of each configured root.

        These are the directories that must each carry a resolver — the rule's
        "files" are directories, and ``file_has_violation`` checks for an
        ABSENT marker inside each.
        """
        out: list[Path] = []
        for root in self._roots:
            base = self._repo_root / root if root else self._repo_root
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir()):
                if not child.is_dir():
                    continue
                if child.name in DEFAULT_EXEMPT_DIRS or child.name.startswith("."):
                    continue
                out.append(None)
        return out

    @_mutmut_mutated(mutants_xǁReadmeResolverCoverageǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return directory_missing_resolver(path, resolver_file=self.resolver_file)

    def xǁReadmeResolverCoverageǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return directory_missing_resolver(path, resolver_file=self.resolver_file)

    def xǁReadmeResolverCoverageǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return directory_missing_resolver(None, resolver_file=self.resolver_file)

    def xǁReadmeResolverCoverageǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return directory_missing_resolver(path, resolver_file=None)

    def xǁReadmeResolverCoverageǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return directory_missing_resolver(resolver_file=self.resolver_file)

    def xǁReadmeResolverCoverageǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return directory_missing_resolver(path, )

mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['_mutmut_orig'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_1'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_2'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_3'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_4'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_5'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_6'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_7'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_8'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_9'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_10'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_11'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfrom_config__mutmut['xǁReadmeResolverCoverageǁfrom_config__mutmut_12'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfrom_config__mutmut_12 # type: ignore # mutmut generated

mutants_xǁReadmeResolverCoverageǁis_in_scope__mutmut['_mutmut_orig'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁis_in_scope__mutmut['xǁReadmeResolverCoverageǁis_in_scope__mutmut_1'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁis_in_scope__mutmut_1 # type: ignore # mutmut generated

mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['_mutmut_orig'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_1'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_2'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_3'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_3 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_4'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_4 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_5'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_5 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_6'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_6 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_7'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_7 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_8'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_8 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_9'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_9 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_10'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_10 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_11'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_11 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_12'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_12 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_13'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_13 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁenumerate_files__mutmut['xǁReadmeResolverCoverageǁenumerate_files__mutmut_14'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁenumerate_files__mutmut_14 # type: ignore # mutmut generated

mutants_xǁReadmeResolverCoverageǁfile_has_violation__mutmut['_mutmut_orig'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfile_has_violation__mutmut['xǁReadmeResolverCoverageǁfile_has_violation__mutmut_1'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfile_has_violation__mutmut['xǁReadmeResolverCoverageǁfile_has_violation__mutmut_2'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfile_has_violation__mutmut['xǁReadmeResolverCoverageǁfile_has_violation__mutmut_3'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁReadmeResolverCoverageǁfile_has_violation__mutmut['xǁReadmeResolverCoverageǁfile_has_violation__mutmut_4'] = ReadmeResolverCoverage.xǁReadmeResolverCoverageǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ReadmeResolverCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ReadmeResolverCoverage.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ReadmeResolverCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ReadmeResolverCoverage.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ReadmeResolverCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ReadmeResolverCoverage.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ReadmeResolverCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ReadmeResolverCoverage.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ReadmeResolverCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ReadmeResolverCoverage.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ReadmeResolverCoverage:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ReadmeResolverCoverage.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ReadmeResolverCoverage, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ReadmeResolverCoverage, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ReadmeResolverCoverage, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ReadmeResolverCoverage, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
