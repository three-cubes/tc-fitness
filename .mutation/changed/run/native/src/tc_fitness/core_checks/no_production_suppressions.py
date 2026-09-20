"""CORE check: no_production_suppressions — ADR-010 D7 (Sonar/lint silencers).

Production code must be correct, not silenced. A lint / coverage / Sonar
suppression in production source (``# noqa:``, ``# NOSONAR``,
``# pragma: no cover``) is an escape hatch: if a finding is wrong, fix the
structure or delete the dead code rather than tagging it for the linter to
ignore. Tooling and test scaffolding are NOT production code, so the consumer
supplies an exempt-prefix set and the test-file basename rule.

Ported from tc-agent-zone ``scripts/checks/no_production_suppressions.py`` and
re-expressed as a configurable, repo-agnostic rule. The suppression tokens are
the rule's own shape (domain-intrinsic ``DEFAULT_SUPPRESSION_PATTERNS``),
overridable via a ``suppression_patterns`` knob; the exempt path prefixes and
test-basename regex come from config. No repo paths are baked in.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The suppression markers — the rule's own shape, not repo identity. Overridable.
DEFAULT_SUPPRESSION_PATTERNS: tuple[str, ...] = (
    "# pragma: no cover",
    "# NOSONAR",
    "// NOSONAR",
    "# noqa:",
    "// noqa:",
)

#: Python test-file basename convention — domain-intrinsic, overridable.
DEFAULT_TEST_FILE_REGEX = r"^(test_.+\.py|.+_test\.py)$"

REMEDIATION = _remediation(
    fix=(
        "remove the suppression and address the underlying finding (refactor, "
        "delete dead code, or fix the bug); if the file is genuinely tooling "
        "not production logic, move it under an exempt path or list it in "
        "exempt_files."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.no_production_suppressions",
    passing="result = parse(payload)  # finding fixed by validating payload upstream",
    forbidden="result = parse(payload)  # noqa: BLE001",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_file_contains_suppression__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_contains_suppression__mutmut)
def file_contains_suppression(path: Path, patterns: Sequence[str]) -> bool:
    """True iff any line in ``path`` contains one of ``patterns`` (substring).

    Pure helper (the detection core) so tests assert on it directly. A decode /
    read error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(pat in line for line in text.splitlines() for pat in patterns)


def x_file_contains_suppression__mutmut_orig(path: Path, patterns: Sequence[str]) -> bool:
    """True iff any line in ``path`` contains one of ``patterns`` (substring).

    Pure helper (the detection core) so tests assert on it directly. A decode /
    read error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(pat in line for line in text.splitlines() for pat in patterns)


def x_file_contains_suppression__mutmut_1(path: Path, patterns: Sequence[str]) -> bool:
    """True iff any line in ``path`` contains one of ``patterns`` (substring).

    Pure helper (the detection core) so tests assert on it directly. A decode /
    read error is treated as "no violation".
    """
    try:
        text = None
    except (UnicodeDecodeError, OSError):
        return False
    return any(pat in line for line in text.splitlines() for pat in patterns)


def x_file_contains_suppression__mutmut_2(path: Path, patterns: Sequence[str]) -> bool:
    """True iff any line in ``path`` contains one of ``patterns`` (substring).

    Pure helper (the detection core) so tests assert on it directly. A decode /
    read error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding=None)
    except (UnicodeDecodeError, OSError):
        return False
    return any(pat in line for line in text.splitlines() for pat in patterns)


def x_file_contains_suppression__mutmut_3(path: Path, patterns: Sequence[str]) -> bool:
    """True iff any line in ``path`` contains one of ``patterns`` (substring).

    Pure helper (the detection core) so tests assert on it directly. A decode /
    read error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="XXutf-8XX")
    except (UnicodeDecodeError, OSError):
        return False
    return any(pat in line for line in text.splitlines() for pat in patterns)


def x_file_contains_suppression__mutmut_4(path: Path, patterns: Sequence[str]) -> bool:
    """True iff any line in ``path`` contains one of ``patterns`` (substring).

    Pure helper (the detection core) so tests assert on it directly. A decode /
    read error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="UTF-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(pat in line for line in text.splitlines() for pat in patterns)


def x_file_contains_suppression__mutmut_5(path: Path, patterns: Sequence[str]) -> bool:
    """True iff any line in ``path`` contains one of ``patterns`` (substring).

    Pure helper (the detection core) so tests assert on it directly. A decode /
    read error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return True
    return any(pat in line for line in text.splitlines() for pat in patterns)


def x_file_contains_suppression__mutmut_6(path: Path, patterns: Sequence[str]) -> bool:
    """True iff any line in ``path`` contains one of ``patterns`` (substring).

    Pure helper (the detection core) so tests assert on it directly. A decode /
    read error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(None)


def x_file_contains_suppression__mutmut_7(path: Path, patterns: Sequence[str]) -> bool:
    """True iff any line in ``path`` contains one of ``patterns`` (substring).

    Pure helper (the detection core) so tests assert on it directly. A decode /
    read error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    return any(pat not in line for line in text.splitlines() for pat in patterns)

mutants_x_file_contains_suppression__mutmut['_mutmut_orig'] = x_file_contains_suppression__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_contains_suppression__mutmut['x_file_contains_suppression__mutmut_1'] = x_file_contains_suppression__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_contains_suppression__mutmut['x_file_contains_suppression__mutmut_2'] = x_file_contains_suppression__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_contains_suppression__mutmut['x_file_contains_suppression__mutmut_3'] = x_file_contains_suppression__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_contains_suppression__mutmut['x_file_contains_suppression__mutmut_4'] = x_file_contains_suppression__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_contains_suppression__mutmut['x_file_contains_suppression__mutmut_5'] = x_file_contains_suppression__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_contains_suppression__mutmut['x_file_contains_suppression__mutmut_6'] = x_file_contains_suppression__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_contains_suppression__mutmut['x_file_contains_suppression__mutmut_7'] = x_file_contains_suppression__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoProductionSuppressionsǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoProductionSuppressions(FitnessRule):
    """Flags production-code lines carrying a lint/coverage/Sonar suppression."""

    name = "no-production-suppressions"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knobs — overridable per consumer.
    suppression_patterns: tuple[str, ...] = DEFAULT_SUPPRESSION_PATTERNS

    @classmethod
    @_mutmut_mutated(mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("suppression_patterns")
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("suppression_patterns")
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = None
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("suppression_patterns")
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("suppression_patterns")
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("suppression_patterns")
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("suppression_patterns")
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, )
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("suppression_patterns")
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = None
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get(None)
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("XXsuppression_patternsXX")
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("SUPPRESSION_PATTERNS")
        rule.suppression_patterns = tuple(patterns) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("suppression_patterns")
        rule.suppression_patterns = None
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("suppression_patterns")
        rule.suppression_patterns = tuple(None) if patterns is not None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @classmethod
    def xǁNoProductionSuppressionsǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoProductionSuppressions:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoProductionSuppressions)  # noqa: S101  # narrowing for mypy
        patterns = config.get("suppression_patterns")
        rule.suppression_patterns = tuple(patterns) if patterns is None else DEFAULT_SUPPRESSION_PATTERNS
        return rule

    @_mutmut_mutated(mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_2(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(None):
            return False
        basename = rel.rsplit("/", 1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_3(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return True
        basename = rel.rsplit("/", 1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_4(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = None
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_5(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit(None, 1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_6(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", None)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_7(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit(1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_8(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", )[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_9(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.split("/", 1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_10(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("XX/XX", 1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_11(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 2)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_12(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 1)[+1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_13(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 1)[-2]
        return not re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_14(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 1)[-1]
        return re.match(DEFAULT_TEST_FILE_REGEX, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_15(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 1)[-1]
        return not re.match(None, basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_16(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, None)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_17(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 1)[-1]
        return not re.match(basename)

    def xǁNoProductionSuppressionsǁis_in_scope__mutmut_18(self, rel: str) -> bool:
        """Extension-in-scope AND not under an exempt prefix AND not a test file."""
        if not super().is_in_scope(rel):
            return False
        basename = rel.rsplit("/", 1)[-1]
        return not re.match(DEFAULT_TEST_FILE_REGEX, )

    @_mutmut_mutated(mutants_xǁNoProductionSuppressionsǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_contains_suppression(path, self.suppression_patterns)

    def xǁNoProductionSuppressionsǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_contains_suppression(path, self.suppression_patterns)

    def xǁNoProductionSuppressionsǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_contains_suppression(None, self.suppression_patterns)

    def xǁNoProductionSuppressionsǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_contains_suppression(path, None)

    def xǁNoProductionSuppressionsǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_contains_suppression(self.suppression_patterns)

    def xǁNoProductionSuppressionsǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_contains_suppression(path, )

mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['_mutmut_orig'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_1'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_2'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_3'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_4'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_5'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_6'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_7'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_8'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_9'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_10'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_11'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfrom_config__mutmut['xǁNoProductionSuppressionsǁfrom_config__mutmut_12'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfrom_config__mutmut_12 # type: ignore # mutmut generated

mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['_mutmut_orig'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_1'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_2'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_3'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_4'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_5'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_6'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_7'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_8'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_9'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_10'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_11'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_12'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_13'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_14'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_15'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_16'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_17'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁis_in_scope__mutmut['xǁNoProductionSuppressionsǁis_in_scope__mutmut_18'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁis_in_scope__mutmut_18 # type: ignore # mutmut generated

mutants_xǁNoProductionSuppressionsǁfile_has_violation__mutmut['_mutmut_orig'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfile_has_violation__mutmut['xǁNoProductionSuppressionsǁfile_has_violation__mutmut_1'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfile_has_violation__mutmut['xǁNoProductionSuppressionsǁfile_has_violation__mutmut_2'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfile_has_violation__mutmut['xǁNoProductionSuppressionsǁfile_has_violation__mutmut_3'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoProductionSuppressionsǁfile_has_violation__mutmut['xǁNoProductionSuppressionsǁfile_has_violation__mutmut_4'] = NoProductionSuppressions.xǁNoProductionSuppressionsǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoProductionSuppressions:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoProductionSuppressions.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoProductionSuppressions:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoProductionSuppressions.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoProductionSuppressions:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoProductionSuppressions.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoProductionSuppressions:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoProductionSuppressions.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoProductionSuppressions:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoProductionSuppressions.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoProductionSuppressions:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoProductionSuppressions.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoProductionSuppressions, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoProductionSuppressions, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoProductionSuppressions, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoProductionSuppressions, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
