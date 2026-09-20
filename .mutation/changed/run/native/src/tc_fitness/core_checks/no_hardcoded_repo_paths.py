"""CORE check: no_hardcoded_repo_paths — no absolute checkout path baked in code.

A literal absolute checkout path (the directory a repo is cloned to on a build
host or VM) hardcoded in source or config breaks the moment the code runs
anywhere else: a different developer's machine, a container, a renamed host. The
sanctioned forms are a path resolved relative to the script
(``Path(__file__).resolve().parents[N]``) or an environment variable.

This rule flags any in-scope text file containing a configured NEEDLE substring
(the absolute path prefix the consumer wants banned). Markdown and other doc
extensions are exempt by default — they describe paths, they don't execute them.

Ported from tc-agent-zone ``scripts/checks/no_hardcoded_repo_paths.py`` and
re-expressed as a configurable, repo-agnostic rule: the banned NEEDLE, the scan
roots, the exempt extensions and the exempt prefixes ALL arrive from the
consumer's ``[tool.tc_fitness]`` config. The donor hardcoded its own
``/data/development/<repo>/`` literal; this module bakes in NONE — a consumer
with no ``needles`` configured flags nothing.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Doc extensions that describe paths rather than execute them. Domain-intrinsic
#: default and part of the rule definition, not consumer config.
DEFAULT_EXEMPT_EXTENSIONS: tuple[str, ...] = (".md",)

#: Any text extension is a candidate — a consumer scopes via ``extensions``.
#: The rule itself has no language; it is a substring search.
DEFAULT_EXTENSIONS: tuple[str, ...] = (".py", ".sh", ".yaml", ".yml", ".json", ".toml")

REMEDIATION = _remediation(
    fix=(
        "replace the hardcoded absolute checkout path with a path resolved "
        "relative to the script (Path(__file__).resolve().parents[N]) or an "
        "environment variable or explicit runtime input."
    ),
    nxt="re-run this check to confirm the hardcode is gone.",
    run="python -m tc_fitness.core_checks.no_hardcoded_repo_paths",
    passing="ROOT = Path(__file__).resolve().parents[2]",
    forbidden='ROOT = "/data/development/<repo>/"',
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_file_contains_needle__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_contains_needle__mutmut)
def file_contains_needle(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(needle in text for needle in needles)


def x_file_contains_needle__mutmut_orig(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(needle in text for needle in needles)


def x_file_contains_needle__mutmut_1(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if needles:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(needle in text for needle in needles)


def x_file_contains_needle__mutmut_2(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return True
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(needle in text for needle in needles)


def x_file_contains_needle__mutmut_3(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return False
    try:
        text = None
    except (OSError, UnicodeDecodeError):
        return False
    return any(needle in text for needle in needles)


def x_file_contains_needle__mutmut_4(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return False
    try:
        text = path.read_text(encoding=None)
    except (OSError, UnicodeDecodeError):
        return False
    return any(needle in text for needle in needles)


def x_file_contains_needle__mutmut_5(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return False
    try:
        text = path.read_text(encoding="XXutf-8XX")
    except (OSError, UnicodeDecodeError):
        return False
    return any(needle in text for needle in needles)


def x_file_contains_needle__mutmut_6(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return False
    try:
        text = path.read_text(encoding="UTF-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(needle in text for needle in needles)


def x_file_contains_needle__mutmut_7(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True
    return any(needle in text for needle in needles)


def x_file_contains_needle__mutmut_8(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(None)


def x_file_contains_needle__mutmut_9(
    path: Path,
    *,
    needles: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the banned ``needles`` substrings.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 file (binary) decodes to nothing of interest and returns False;
    an empty ``needles`` tuple flags nothing.
    """
    if not needles:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(needle not in text for needle in needles)

mutants_x_file_contains_needle__mutmut['_mutmut_orig'] = x_file_contains_needle__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_contains_needle__mutmut['x_file_contains_needle__mutmut_1'] = x_file_contains_needle__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_contains_needle__mutmut['x_file_contains_needle__mutmut_2'] = x_file_contains_needle__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_contains_needle__mutmut['x_file_contains_needle__mutmut_3'] = x_file_contains_needle__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_contains_needle__mutmut['x_file_contains_needle__mutmut_4'] = x_file_contains_needle__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_contains_needle__mutmut['x_file_contains_needle__mutmut_5'] = x_file_contains_needle__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_contains_needle__mutmut['x_file_contains_needle__mutmut_6'] = x_file_contains_needle__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_contains_needle__mutmut['x_file_contains_needle__mutmut_7'] = x_file_contains_needle__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_contains_needle__mutmut['x_file_contains_needle__mutmut_8'] = x_file_contains_needle__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_contains_needle__mutmut['x_file_contains_needle__mutmut_9'] = x_file_contains_needle__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoHardcodedRepoPathsǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoHardcodedRepoPaths(FitnessRule):
    """Flags files holding a banned absolute-checkout-path needle."""

    name = "no-hardcoded-repo-paths"
    remediation = REMEDIATION
    extensions = DEFAULT_EXTENSIONS

    #: The banned absolute-path substrings — the consumer's OWN checkout
    #: literals. No default: a consumer with none configured flags nothing.
    needles: tuple[str, ...] = ()

    @classmethod
    @_mutmut_mutated(mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = None
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, )
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = None
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get(None)
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("XXneedlesXX")
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("NEEDLES")
        if needles is not None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is None:
            rule.needles = tuple(needles)
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is not None:
            rule.needles = None
        return rule

    @classmethod
    def xǁNoHardcodedRepoPathsǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoHardcodedRepoPaths:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoHardcodedRepoPaths)  # noqa: S101  # narrowing for mypy
        needles = config.get("needles")
        if needles is not None:
            rule.needles = tuple(None)
        return rule

    @_mutmut_mutated(mutants_xǁNoHardcodedRepoPathsǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        if rel.endswith(DEFAULT_EXEMPT_EXTENSIONS):
            return False
        return super().is_in_scope(rel)

    def xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        if rel.endswith(DEFAULT_EXEMPT_EXTENSIONS):
            return False
        return super().is_in_scope(rel)

    def xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        if rel.endswith(None):
            return False
        return super().is_in_scope(rel)

    def xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_2(self, rel: str) -> bool:
        if rel.endswith(DEFAULT_EXEMPT_EXTENSIONS):
            return True
        return super().is_in_scope(rel)

    def xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_3(self, rel: str) -> bool:
        if rel.endswith(DEFAULT_EXEMPT_EXTENSIONS):
            return False
        return super().is_in_scope(None)

    @_mutmut_mutated(mutants_xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_contains_needle(path, needles=self.needles)

    def xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_contains_needle(path, needles=self.needles)

    def xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_contains_needle(None, needles=self.needles)

    def xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_contains_needle(path, needles=None)

    def xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_contains_needle(needles=self.needles)

    def xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_contains_needle(path, )

mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['_mutmut_orig'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_1'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_2'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_3'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_4'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_5'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_6'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_7'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_8'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_9'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_10'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_11'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfrom_config__mutmut['xǁNoHardcodedRepoPathsǁfrom_config__mutmut_12'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfrom_config__mutmut_12 # type: ignore # mutmut generated

mutants_xǁNoHardcodedRepoPathsǁis_in_scope__mutmut['_mutmut_orig'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁis_in_scope__mutmut['xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_1'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁis_in_scope__mutmut['xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_2'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁis_in_scope__mutmut['xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_3'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁis_in_scope__mutmut_3 # type: ignore # mutmut generated

mutants_xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut['_mutmut_orig'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut['xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_1'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut['xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_2'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut['xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_3'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut['xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_4'] = NoHardcodedRepoPaths.xǁNoHardcodedRepoPathsǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoHardcodedRepoPaths:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoHardcodedRepoPaths.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoHardcodedRepoPaths:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoHardcodedRepoPaths.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoHardcodedRepoPaths:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoHardcodedRepoPaths.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoHardcodedRepoPaths:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoHardcodedRepoPaths.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoHardcodedRepoPaths:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoHardcodedRepoPaths.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoHardcodedRepoPaths:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoHardcodedRepoPaths.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoHardcodedRepoPaths, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoHardcodedRepoPaths, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoHardcodedRepoPaths, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoHardcodedRepoPaths, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
