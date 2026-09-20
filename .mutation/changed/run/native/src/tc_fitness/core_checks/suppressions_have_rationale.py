"""CORE check: suppressions_have_rationale — every silencer carries a reason.

Sibling of ``no_production_suppressions`` (which bans suppressions outright in
production source). This covers the *allowed-area* suppressions — tests,
scripts, tools — where a deliberate ``# noqa`` / ``# type: ignore`` / ``# nosec``
is sometimes the right call but a BARE one is debt. A suppression PASSES when
the same line carries non-empty text after the token (em-dash + sentence is the
canonical shape); a bare suppression FAILS.

Ported from kairix ``check-suppressions-have-rationale.sh`` (F3, via the
tc-agent-zone Python port) and re-expressed as a configurable, repo-agnostic
rule. The bare-suppression patterns are the rule's own shape
(``DEFAULT_BARE_PATTERNS``), overridable via a ``bare_patterns`` knob; the
consumer supplies ``roots`` / ``exempt_files`` via ``[tool.tc_fitness]``. No
repo paths are baked in.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Bare-suppression patterns: each matches ``<token>`` followed only by optional
#: whitespace + end-of-line. Any trailing rationale text makes the line PASS.
#: The rule's own shape (ruff / mypy / bandit / coverage / Sonar), overridable.
DEFAULT_BARE_PATTERNS: tuple[str, ...] = (
    r"#\s*NOSONAR\s*$",
    r"#\s*+noqa(?::\s*+[A-Z0-9, ]++)?\s*+$",
    r"#\s*pragma:\s*no cover\s*$",
    r"#\s*type:\s*ignore(\[[A-Za-z0-9,_-]+\])?\s*$",
    r"#\s*nosec(\s+B\d+|:\s*B?\d+)?\s*$",
)

REMEDIATION = _remediation(
    fix=(
        "append a same-line rationale directly after the suppression token so "
        "the line documents WHY the rule is silenced (an em-dash + one-line "
        "reason is the canonical shape) — or delete the suppression and address "
        "the underlying warning."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.suppressions_have_rationale",
    passing="x = 1  # NOSONAR - internal log path; not user-controlled",
    forbidden="x = 1  # NOSONAR",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__compile__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__compile__mutmut)
def _compile(patterns: Sequence[str]) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(p) for p in patterns)


def x__compile__mutmut_orig(patterns: Sequence[str]) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(p) for p in patterns)


def x__compile__mutmut_1(patterns: Sequence[str]) -> tuple[re.Pattern[str], ...]:
    return tuple(None)


def x__compile__mutmut_2(patterns: Sequence[str]) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(None) for p in patterns)

mutants_x__compile__mutmut['_mutmut_orig'] = x__compile__mutmut_orig # type: ignore # mutmut generated
mutants_x__compile__mutmut['x__compile__mutmut_1'] = x__compile__mutmut_1 # type: ignore # mutmut generated
mutants_x__compile__mutmut['x__compile__mutmut_2'] = x__compile__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_bare_suppression__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_has_bare_suppression__mutmut)
def file_has_bare_suppression(path: Path, compiled: Sequence[re.Pattern[str]]) -> bool:
    """True iff any line in ``path`` matches a bare-suppression pattern.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    return any(pat.search(line) for line in lines for pat in compiled)


def x_file_has_bare_suppression__mutmut_orig(path: Path, compiled: Sequence[re.Pattern[str]]) -> bool:
    """True iff any line in ``path`` matches a bare-suppression pattern.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    return any(pat.search(line) for line in lines for pat in compiled)


def x_file_has_bare_suppression__mutmut_1(path: Path, compiled: Sequence[re.Pattern[str]]) -> bool:
    """True iff any line in ``path`` matches a bare-suppression pattern.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = None
    except (UnicodeDecodeError, OSError):
        return True
    return any(pat.search(line) for line in lines for pat in compiled)


def x_file_has_bare_suppression__mutmut_2(path: Path, compiled: Sequence[re.Pattern[str]]) -> bool:
    """True iff any line in ``path`` matches a bare-suppression pattern.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding=None).splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    return any(pat.search(line) for line in lines for pat in compiled)


def x_file_has_bare_suppression__mutmut_3(path: Path, compiled: Sequence[re.Pattern[str]]) -> bool:
    """True iff any line in ``path`` matches a bare-suppression pattern.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="XXutf-8XX").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    return any(pat.search(line) for line in lines for pat in compiled)


def x_file_has_bare_suppression__mutmut_4(path: Path, compiled: Sequence[re.Pattern[str]]) -> bool:
    """True iff any line in ``path`` matches a bare-suppression pattern.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="UTF-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    return any(pat.search(line) for line in lines for pat in compiled)


def x_file_has_bare_suppression__mutmut_5(path: Path, compiled: Sequence[re.Pattern[str]]) -> bool:
    """True iff any line in ``path`` matches a bare-suppression pattern.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    return any(pat.search(line) for line in lines for pat in compiled)


def x_file_has_bare_suppression__mutmut_6(path: Path, compiled: Sequence[re.Pattern[str]]) -> bool:
    """True iff any line in ``path`` matches a bare-suppression pattern.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    return any(None)


def x_file_has_bare_suppression__mutmut_7(path: Path, compiled: Sequence[re.Pattern[str]]) -> bool:
    """True iff any line in ``path`` matches a bare-suppression pattern.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    return any(pat.search(None) for line in lines for pat in compiled)

mutants_x_file_has_bare_suppression__mutmut['_mutmut_orig'] = x_file_has_bare_suppression__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_has_bare_suppression__mutmut['x_file_has_bare_suppression__mutmut_1'] = x_file_has_bare_suppression__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_has_bare_suppression__mutmut['x_file_has_bare_suppression__mutmut_2'] = x_file_has_bare_suppression__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_bare_suppression__mutmut['x_file_has_bare_suppression__mutmut_3'] = x_file_has_bare_suppression__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_has_bare_suppression__mutmut['x_file_has_bare_suppression__mutmut_4'] = x_file_has_bare_suppression__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_has_bare_suppression__mutmut['x_file_has_bare_suppression__mutmut_5'] = x_file_has_bare_suppression__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_has_bare_suppression__mutmut['x_file_has_bare_suppression__mutmut_6'] = x_file_has_bare_suppression__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_has_bare_suppression__mutmut['x_file_has_bare_suppression__mutmut_7'] = x_file_has_bare_suppression__mutmut_7 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class SuppressionsHaveRationale(FitnessRule):
    """Flags files holding a bare (rationale-free) lint/type/security suppression."""

    name = "suppressions-have-rationale"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knob — the bare-suppression regexes; overridable per consumer.
    bare_patterns: tuple[str, ...] = DEFAULT_BARE_PATTERNS

    @_mutmut_mutated(mutants_xǁSuppressionsHaveRationaleǁ__init____mutmut)
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._compiled = _compile(self.bare_patterns)

    def xǁSuppressionsHaveRationaleǁ__init____mutmut_orig(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._compiled = _compile(self.bare_patterns)

    def xǁSuppressionsHaveRationaleǁ__init____mutmut_1(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._compiled = _compile(self.bare_patterns)

    def xǁSuppressionsHaveRationaleǁ__init____mutmut_2(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, )
        self._compiled = _compile(self.bare_patterns)

    def xǁSuppressionsHaveRationaleǁ__init____mutmut_3(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._compiled = None

    def xǁSuppressionsHaveRationaleǁ__init____mutmut_4(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._compiled = _compile(None)

    @classmethod
    @_mutmut_mutated(mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = None
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, )
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = None
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get(None)
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("XXbare_patternsXX")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("BARE_PATTERNS")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = None
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(None) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(patterns) if patterns is None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(rule.bare_patterns)
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = None
        return rule

    @classmethod
    def xǁSuppressionsHaveRationaleǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SuppressionsHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SuppressionsHaveRationale)  # noqa: S101  # narrowing for mypy
        patterns = config.get("bare_patterns")
        rule.bare_patterns = tuple(patterns) if patterns is not None else DEFAULT_BARE_PATTERNS
        rule._compiled = _compile(None)
        return rule

    @_mutmut_mutated(mutants_xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_has_bare_suppression(path, self._compiled)

    def xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_has_bare_suppression(path, self._compiled)

    def xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_has_bare_suppression(None, self._compiled)

    def xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_has_bare_suppression(path, None)

    def xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_has_bare_suppression(self._compiled)

    def xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_has_bare_suppression(path, )

mutants_xǁSuppressionsHaveRationaleǁ__init____mutmut['_mutmut_orig'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁ__init____mutmut['xǁSuppressionsHaveRationaleǁ__init____mutmut_1'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁ__init____mutmut['xǁSuppressionsHaveRationaleǁ__init____mutmut_2'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁ__init____mutmut['xǁSuppressionsHaveRationaleǁ__init____mutmut_3'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁ__init____mutmut['xǁSuppressionsHaveRationaleǁ__init____mutmut_4'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁ__init____mutmut_4 # type: ignore # mutmut generated

mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['_mutmut_orig'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_1'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_2'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_3'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_4'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_5'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_6'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_7'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_8'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_9'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_10'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_11'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_12'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_13'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfrom_config__mutmut['xǁSuppressionsHaveRationaleǁfrom_config__mutmut_14'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfrom_config__mutmut_14 # type: ignore # mutmut generated

mutants_xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut['_mutmut_orig'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut['xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_1'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut['xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_2'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut['xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_3'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut['xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_4'] = SuppressionsHaveRationale.xǁSuppressionsHaveRationaleǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SuppressionsHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SuppressionsHaveRationale.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SuppressionsHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SuppressionsHaveRationale.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SuppressionsHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SuppressionsHaveRationale.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SuppressionsHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SuppressionsHaveRationale.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SuppressionsHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SuppressionsHaveRationale.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SuppressionsHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SuppressionsHaveRationale.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SuppressionsHaveRationale, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SuppressionsHaveRationale, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SuppressionsHaveRationale, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SuppressionsHaveRationale, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
