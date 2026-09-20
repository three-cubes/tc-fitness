"""CORE check: adr_number_unique — numbered decision records have unique numbers.

Architecture Decision Records (and any numbered-doc series) are cited by their
numeric prefix; a collision breaks navigation, citation, and every gate that
resolves a record by id. This rule scans the configured decision directory and
FAILS when two files share a number.

Built fresh for the v0.6.0 CORE set from tc-agent-zone
``scripts/checks/adr_number_unique.py`` and re-expressed as a configurable,
repo-agnostic rule. What was repo-specific — the directory the records live in
and the filename pattern that carries the number — is consumer config. The
engine ships a generic ``ADR-<NNN>-<slug>`` default pattern, overridable for
any numbered-doc convention.

This rule is a CROSS-FILE invariant (a number, not a file, is the unit of
violation), so it overrides :meth:`collect_violations` rather than implementing
a per-file predicate: a file is "in violation" when it shares its number with
another file.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Generic numbered-record default — captures the number in group 1. Overridable.
DEFAULT_RECORD_PATTERN = r"^ADR-(\d{3})-.+\.md$"
#: Directory the records live under, repo-relative. Consumer config in practice.
DEFAULT_RECORD_DIR = "docs/decisions"

REMEDIATION = _remediation(
    fix=(
        "renumber the newer file to the next free number, update its `id:` field "
        "and heading, and sweep every reference across the repo (both the "
        "file-path form and the bare-number form). Keep the older file's number."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.adr_number_unique",
    passing="docs/decisions/ADR-041-some-decision.md  (041 used by exactly one file)",
    forbidden="ADR-041-foo.md AND ADR-041-bar.md  (041 used by two files)",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_find_collisions__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_find_collisions__mutmut)
def find_collisions(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_orig(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_1(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = None
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_2(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(None)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_3(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_4(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(None):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_5(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_6(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            break
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_7(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = None
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_8(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(None)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_9(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(None)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_10(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(None)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_11(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(2)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_12(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(None) for num, paths in by_number.items() if len(paths) > 1}


def x_find_collisions__mutmut_13(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) >= 1}


def x_find_collisions__mutmut_14(
    record_dir: Path,
    *,
    pattern: re.Pattern[str],
) -> dict[str, list[Path]]:
    """Pure helper: map each number used >1 time to the files that use it.

    Returns only the colliding numbers (those with two or more files). The file
    list per number is sorted for stable output.
    """
    by_number: dict[str, list[Path]] = defaultdict(list)
    if not record_dir.is_dir():
        return {}
    for path in sorted(record_dir.iterdir()):
        if not path.is_file():
            continue
        match = pattern.match(path.name)
        if match:
            by_number[match.group(1)].append(path)
    return {num: sorted(paths) for num, paths in by_number.items() if len(paths) > 2}

mutants_x_find_collisions__mutmut['_mutmut_orig'] = x_find_collisions__mutmut_orig # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_1'] = x_find_collisions__mutmut_1 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_2'] = x_find_collisions__mutmut_2 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_3'] = x_find_collisions__mutmut_3 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_4'] = x_find_collisions__mutmut_4 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_5'] = x_find_collisions__mutmut_5 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_6'] = x_find_collisions__mutmut_6 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_7'] = x_find_collisions__mutmut_7 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_8'] = x_find_collisions__mutmut_8 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_9'] = x_find_collisions__mutmut_9 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_10'] = x_find_collisions__mutmut_10 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_11'] = x_find_collisions__mutmut_11 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_12'] = x_find_collisions__mutmut_12 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_13'] = x_find_collisions__mutmut_13 # type: ignore # mutmut generated
mutants_x_find_collisions__mutmut['x_find_collisions__mutmut_14'] = x_find_collisions__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAdrNumberUniqueǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut: MutantDict = {}  # type: ignore


class AdrNumberUnique(FitnessRule):
    """Flags numbered decision records that share a number (a cross-file invariant)."""

    name = "adr-number-unique"
    remediation = REMEDIATION
    extensions = (".md",)

    #: Rule-specific config (instance attrs; from_config overrides per consumer).
    record_dir: str = DEFAULT_RECORD_DIR
    record_pattern: re.Pattern[str] = re.compile(DEFAULT_RECORD_PATTERN)

    @classmethod
    @_mutmut_mutated(mutants_xǁAdrNumberUniqueǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = None
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, )
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = None
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(None)
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get(None, DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", None))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get(DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", ))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("XXrecord_dirXX", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("RECORD_DIR", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = None
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(None)
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(None))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get(None, DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", None)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get(DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("record_pattern", )))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("XXrecord_patternXX", DEFAULT_RECORD_PATTERN)))
        return rule

    @classmethod
    def xǁAdrNumberUniqueǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> AdrNumberUnique:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, AdrNumberUnique)  # noqa: S101  # narrowing for mypy
        rule.record_dir = str(config.get("record_dir", DEFAULT_RECORD_DIR))
        rule.record_pattern = re.compile(str(config.get("RECORD_PATTERN", DEFAULT_RECORD_PATTERN)))
        return rule

    @_mutmut_mutated(mutants_xǁAdrNumberUniqueǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        """Unused for this rule — collisions are cross-file (see collect_violations)."""
        return False

    def xǁAdrNumberUniqueǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        """Unused for this rule — collisions are cross-file (see collect_violations)."""
        return False

    def xǁAdrNumberUniqueǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        """Unused for this rule — collisions are cross-file (see collect_violations)."""
        return True

    @_mutmut_mutated(mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut)
    def collect_violations(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root / self.record_dir
        collisions = find_collisions(record_dir, pattern=self.record_pattern)
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(p))
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_orig(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root / self.record_dir
        collisions = find_collisions(record_dir, pattern=self.record_pattern)
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(p))
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_1(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = None
        collisions = find_collisions(record_dir, pattern=self.record_pattern)
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(p))
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_2(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root * self.record_dir
        collisions = find_collisions(record_dir, pattern=self.record_pattern)
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(p))
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_3(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root / self.record_dir
        collisions = None
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(p))
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_4(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root / self.record_dir
        collisions = find_collisions(None, pattern=self.record_pattern)
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(p))
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_5(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root / self.record_dir
        collisions = find_collisions(record_dir, pattern=None)
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(p))
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_6(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root / self.record_dir
        collisions = find_collisions(pattern=self.record_pattern)
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(p))
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_7(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root / self.record_dir
        collisions = find_collisions(record_dir, )
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(p))
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_8(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root / self.record_dir
        collisions = find_collisions(record_dir, pattern=self.record_pattern)
        out: set[Path] = None
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(p))
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_9(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root / self.record_dir
        collisions = find_collisions(record_dir, pattern=self.record_pattern)
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(None)
        return out

    def xǁAdrNumberUniqueǁcollect_violations__mutmut_10(self) -> set[Path]:
        """Override: every file sharing its number with another is in violation."""
        record_dir = self._repo_root / self.record_dir
        collisions = find_collisions(record_dir, pattern=self.record_pattern)
        out: set[Path] = set()
        for paths in collisions.values():
            for p in paths:
                out.add(self._repo_relative(None))
        return out

mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['_mutmut_orig'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_1'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_2'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_3'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_4'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_5'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_6'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_7'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_8'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_9'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_10'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_11'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_12'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_13'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_14'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_15'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_16'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_17'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_18'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_19'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_20'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_21'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfrom_config__mutmut['xǁAdrNumberUniqueǁfrom_config__mutmut_22'] = AdrNumberUnique.xǁAdrNumberUniqueǁfrom_config__mutmut_22 # type: ignore # mutmut generated

mutants_xǁAdrNumberUniqueǁfile_has_violation__mutmut['_mutmut_orig'] = AdrNumberUnique.xǁAdrNumberUniqueǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁfile_has_violation__mutmut['xǁAdrNumberUniqueǁfile_has_violation__mutmut_1'] = AdrNumberUnique.xǁAdrNumberUniqueǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated

mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['_mutmut_orig'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_orig # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['xǁAdrNumberUniqueǁcollect_violations__mutmut_1'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_1 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['xǁAdrNumberUniqueǁcollect_violations__mutmut_2'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_2 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['xǁAdrNumberUniqueǁcollect_violations__mutmut_3'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_3 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['xǁAdrNumberUniqueǁcollect_violations__mutmut_4'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_4 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['xǁAdrNumberUniqueǁcollect_violations__mutmut_5'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_5 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['xǁAdrNumberUniqueǁcollect_violations__mutmut_6'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_6 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['xǁAdrNumberUniqueǁcollect_violations__mutmut_7'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_7 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['xǁAdrNumberUniqueǁcollect_violations__mutmut_8'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_8 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['xǁAdrNumberUniqueǁcollect_violations__mutmut_9'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_9 # type: ignore # mutmut generated
mutants_xǁAdrNumberUniqueǁcollect_violations__mutmut['xǁAdrNumberUniqueǁcollect_violations__mutmut_10'] = AdrNumberUnique.xǁAdrNumberUniqueǁcollect_violations__mutmut_10 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> AdrNumberUnique:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return AdrNumberUnique.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> AdrNumberUnique:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return AdrNumberUnique.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> AdrNumberUnique:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return AdrNumberUnique.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> AdrNumberUnique:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return AdrNumberUnique.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> AdrNumberUnique:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return AdrNumberUnique.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> AdrNumberUnique:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return AdrNumberUnique.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(AdrNumberUnique, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(AdrNumberUnique, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(AdrNumberUnique, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(AdrNumberUnique, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
