"""CORE check: pattern_chokepoint — a pattern confined to a single chokepoint.

Some properties belong in exactly ONE place. When a decision (e.g. "is this
write or read?", "which collection does this route to?") is intrinsic to data
and should be derived at a single boundary, letting the deciding token leak to
other call sites recreates the bug it was meant to prevent: a flag you can pass
at N sites is a flag you can forget at one (see the neo4j read/write-session
incident — the write-ness was threaded as a ``write=`` kwarg every caller had to
remember, until it was derived once at ``client.cypher``).

This rule flags any in-scope file — OUTSIDE the configured semantic chokepoint
locations — that matches a configured regex ``pattern``. The
chokepoint file(s) where the pattern legitimately lives are listed in
``chokepoint_files``; everywhere else the pattern is forbidden. A consumer with no
``patterns`` configured flags nothing — NO pattern is baked in.

Typical config (a consumer's ``[tool.tc_fitness.core_checks.<name>]`` block):

    name = "cypher-write-mode-chokepoint"
    roots = ["kairix"]
    patterns = ["default_access_mode\\\\s*=", "_is_write_query"]
    chokepoint_files = ["kairix/knowledge/graph/client.py"]
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

REMEDIATION = _remediation(
    fix=(
        "the matched token belongs only at its single chokepoint — derive the "
        "property there and call the chokepoint instead of re-introducing the "
        "token here. If a new file is a legitimate part of the chokepoint, add "
        "it to this rule's chokepoint_files config with a one-line rationale."
    ),
    nxt="re-run this check to confirm the pattern is confined to its chokepoint.",
    run="python -m tc_fitness.core_checks.pattern_chokepoint",
    passing="rows = client.cypher(query, params)  # write-ness derived inside cypher()",
    forbidden='session = driver.session(default_access_mode="WRITE")  # outside the chokepoint',
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_file_matches_any_pattern__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_matches_any_pattern__mutmut)
def file_matches_any_pattern(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, text) for p in patterns)


def x_file_matches_any_pattern__mutmut_orig(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, text) for p in patterns)


def x_file_matches_any_pattern__mutmut_1(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if patterns:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, text) for p in patterns)


def x_file_matches_any_pattern__mutmut_2(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return True
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, text) for p in patterns)


def x_file_matches_any_pattern__mutmut_3(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = None
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, text) for p in patterns)


def x_file_matches_any_pattern__mutmut_4(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding=None)
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, text) for p in patterns)


def x_file_matches_any_pattern__mutmut_5(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="XXutf-8XX")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, text) for p in patterns)


def x_file_matches_any_pattern__mutmut_6(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="UTF-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, text) for p in patterns)


def x_file_matches_any_pattern__mutmut_7(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return True
    return any(re.search(p, text) for p in patterns)


def x_file_matches_any_pattern__mutmut_8(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(None)


def x_file_matches_any_pattern__mutmut_9(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(None, text) for p in patterns)


def x_file_matches_any_pattern__mutmut_10(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, None) for p in patterns)


def x_file_matches_any_pattern__mutmut_11(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(text) for p in patterns)


def x_file_matches_any_pattern__mutmut_12(path: Path, *, patterns: tuple[str, ...]) -> bool:
    """True iff ``path``'s text matches any of the regex ``patterns``.

    Pure helper (the detection core) so tests can assert on it directly. A
    non-UTF-8 / unreadable file returns False; an empty ``patterns`` tuple flags
    nothing. Patterns are compiled per call — checks run once, so this is not a
    hot path.
    """
    if not patterns:
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(re.search(p, ) for p in patterns)

mutants_x_file_matches_any_pattern__mutmut['_mutmut_orig'] = x_file_matches_any_pattern__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_1'] = x_file_matches_any_pattern__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_2'] = x_file_matches_any_pattern__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_3'] = x_file_matches_any_pattern__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_4'] = x_file_matches_any_pattern__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_5'] = x_file_matches_any_pattern__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_6'] = x_file_matches_any_pattern__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_7'] = x_file_matches_any_pattern__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_8'] = x_file_matches_any_pattern__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_9'] = x_file_matches_any_pattern__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_10'] = x_file_matches_any_pattern__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_11'] = x_file_matches_any_pattern__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_matches_any_pattern__mutmut['x_file_matches_any_pattern__mutmut_12'] = x_file_matches_any_pattern__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPatternChokepointǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class PatternChokepoint(FitnessRule):
    """Flags configured patterns outside their semantic chokepoint files."""

    name = "pattern-chokepoint"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Regexes whose match outside the chokepoint is a violation. No default:
    #: a consumer with none configured flags nothing.
    patterns: tuple[str, ...] = ()
    chokepoint_files: frozenset[str] = frozenset()

    @classmethod
    @_mutmut_mutated(mutants_xǁPatternChokepointǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = None
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, )
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = None
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get(None)
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("XXpatternsXX")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("PATTERNS")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = None
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(None)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = None
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get(None, [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", None)
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get([])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", )
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("XXchokepoint_filesXX", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("CHOKEPOINT_FILES", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) and any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(None):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError(None)
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("XXchokepoint_files must be a list of repository-relative pathsXX")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("CHOKEPOINT_FILES MUST BE A LIST OF REPOSITORY-RELATIVE PATHS")
        rule.chokepoint_files = frozenset(chokepoints)
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = None
        return rule

    @classmethod
    def xǁPatternChokepointǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PatternChokepoint:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PatternChokepoint)  # noqa: S101  # narrowing for mypy
        patterns = config.get("patterns")
        if patterns is not None:
            rule.patterns = tuple(patterns)
        chokepoints = config.get("chokepoint_files", [])
        if not isinstance(chokepoints, list) or any(not isinstance(path, str) for path in chokepoints):
            raise ValueError("chokepoint_files must be a list of repository-relative paths")
        rule.chokepoint_files = frozenset(None)
        return rule

    @_mutmut_mutated(mutants_xǁPatternChokepointǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        if self._repo_relative(path).as_posix() in self.chokepoint_files:
            return False
        return file_matches_any_pattern(path, patterns=self.patterns)

    def xǁPatternChokepointǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        if self._repo_relative(path).as_posix() in self.chokepoint_files:
            return False
        return file_matches_any_pattern(path, patterns=self.patterns)

    def xǁPatternChokepointǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        if self._repo_relative(None).as_posix() in self.chokepoint_files:
            return False
        return file_matches_any_pattern(path, patterns=self.patterns)

    def xǁPatternChokepointǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        if self._repo_relative(path).as_posix() not in self.chokepoint_files:
            return False
        return file_matches_any_pattern(path, patterns=self.patterns)

    def xǁPatternChokepointǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        if self._repo_relative(path).as_posix() in self.chokepoint_files:
            return True
        return file_matches_any_pattern(path, patterns=self.patterns)

    def xǁPatternChokepointǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        if self._repo_relative(path).as_posix() in self.chokepoint_files:
            return False
        return file_matches_any_pattern(None, patterns=self.patterns)

    def xǁPatternChokepointǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        if self._repo_relative(path).as_posix() in self.chokepoint_files:
            return False
        return file_matches_any_pattern(path, patterns=None)

    def xǁPatternChokepointǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        if self._repo_relative(path).as_posix() in self.chokepoint_files:
            return False
        return file_matches_any_pattern(patterns=self.patterns)

    def xǁPatternChokepointǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        if self._repo_relative(path).as_posix() in self.chokepoint_files:
            return False
        return file_matches_any_pattern(path, )

mutants_xǁPatternChokepointǁfrom_config__mutmut['_mutmut_orig'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_1'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_2'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_3'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_4'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_5'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_6'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_7'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_8'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_9'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_10'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_11'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_12'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_13'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_14'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_15'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_16'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_17'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_18'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_19'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_20'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_21'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_22'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_23'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_24'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_25'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_26'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_27'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfrom_config__mutmut['xǁPatternChokepointǁfrom_config__mutmut_28'] = PatternChokepoint.xǁPatternChokepointǁfrom_config__mutmut_28 # type: ignore # mutmut generated

mutants_xǁPatternChokepointǁfile_has_violation__mutmut['_mutmut_orig'] = PatternChokepoint.xǁPatternChokepointǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfile_has_violation__mutmut['xǁPatternChokepointǁfile_has_violation__mutmut_1'] = PatternChokepoint.xǁPatternChokepointǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfile_has_violation__mutmut['xǁPatternChokepointǁfile_has_violation__mutmut_2'] = PatternChokepoint.xǁPatternChokepointǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfile_has_violation__mutmut['xǁPatternChokepointǁfile_has_violation__mutmut_3'] = PatternChokepoint.xǁPatternChokepointǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfile_has_violation__mutmut['xǁPatternChokepointǁfile_has_violation__mutmut_4'] = PatternChokepoint.xǁPatternChokepointǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfile_has_violation__mutmut['xǁPatternChokepointǁfile_has_violation__mutmut_5'] = PatternChokepoint.xǁPatternChokepointǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfile_has_violation__mutmut['xǁPatternChokepointǁfile_has_violation__mutmut_6'] = PatternChokepoint.xǁPatternChokepointǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPatternChokepointǁfile_has_violation__mutmut['xǁPatternChokepointǁfile_has_violation__mutmut_7'] = PatternChokepoint.xǁPatternChokepointǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PatternChokepoint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PatternChokepoint.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PatternChokepoint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PatternChokepoint.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PatternChokepoint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PatternChokepoint.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PatternChokepoint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PatternChokepoint.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PatternChokepoint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PatternChokepoint.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PatternChokepoint:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PatternChokepoint.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PatternChokepoint, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PatternChokepoint, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PatternChokepoint, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PatternChokepoint, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
