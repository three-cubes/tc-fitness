"""Shared Cobertura path resolution for coverage assurance.

Coverage producers may emit repository-relative source roots, absolute source
roots, or several roots. Assurance resolves every class filename back to one
repository-relative file and rejects ambiguous or out-of-repository evidence.
"""

from __future__ import annotations

import ast
import math
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@dataclass(frozen=True)
class CoverageCounts:
    """Independent executable-line and branch-exit counts, never combined."""

    lines: int
    covered_lines: int
    branches: int
    covered_branches: int

    @property
    def line_pct(self) -> float:
        return 100 * self.covered_lines / self.lines if self.lines else 100.0

    @property
    def branch_pct(self) -> float:
        return 100 * self.covered_branches / self.branches if self.branches else 100.0
mutants_x_coverage_integer__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_coverage_integer__mutmut)
def coverage_integer(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def x_coverage_integer__mutmut_orig(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def x_coverage_integer__mutmut_1(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None and re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def x_coverage_integer__mutmut_2(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is not None or re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def x_coverage_integer__mutmut_3(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(None, value) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def x_coverage_integer__mutmut_4(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"0|[1-9][0-9]*", None) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def x_coverage_integer__mutmut_5(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(value) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def x_coverage_integer__mutmut_6(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"0|[1-9][0-9]*", ) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def x_coverage_integer__mutmut_7(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"XX0|[1-9][0-9]*XX", value) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def x_coverage_integer__mutmut_8(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"0|[1-9][0-9]*", value) is not None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(value)


def x_coverage_integer__mutmut_9(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise ValueError(None)
    return int(value)


def x_coverage_integer__mutmut_10(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise ValueError("XXcoverage detail requires non-negative integer countsXX")
    return int(value)


def x_coverage_integer__mutmut_11(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise ValueError("COVERAGE DETAIL REQUIRES NON-NEGATIVE INTEGER COUNTS")
    return int(value)


def x_coverage_integer__mutmut_12(value: str | None) -> int:
    """Require explicit non-negative integer evidence rather than defaults."""
    if value is None or re.fullmatch(r"0|[1-9][0-9]*", value) is None:
        raise ValueError("coverage detail requires non-negative integer counts")
    return int(None)

mutants_x_coverage_integer__mutmut['_mutmut_orig'] = x_coverage_integer__mutmut_orig # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_1'] = x_coverage_integer__mutmut_1 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_2'] = x_coverage_integer__mutmut_2 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_3'] = x_coverage_integer__mutmut_3 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_4'] = x_coverage_integer__mutmut_4 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_5'] = x_coverage_integer__mutmut_5 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_6'] = x_coverage_integer__mutmut_6 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_7'] = x_coverage_integer__mutmut_7 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_8'] = x_coverage_integer__mutmut_8 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_9'] = x_coverage_integer__mutmut_9 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_10'] = x_coverage_integer__mutmut_10 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_11'] = x_coverage_integer__mutmut_11 # type: ignore # mutmut generated
mutants_x_coverage_integer__mutmut['x_coverage_integer__mutmut_12'] = x_coverage_integer__mutmut_12 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_validate_coverage_rate__mutmut)
def validate_coverage_rate(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_orig(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_1(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is not None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_2(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError(None)
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_3(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("XXmissing coverage rateXX")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_4(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("MISSING COVERAGE RATE")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_5(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = None
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_6(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(None)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_7(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) and not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_8(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_9(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(None) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_10(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_11(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 1 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_12(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 < rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_13(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate < 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_14(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 2:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_15(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError(None)
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_16(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("XXcoverage rate must be finite and between zero and oneXX")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_17(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("COVERAGE RATE MUST BE FINITE AND BETWEEN ZERO AND ONE")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_18(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total or rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_19(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_20(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate == 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_21(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 2:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_22(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError(None)
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_23(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("XXzero-opportunity coverage must be measured, not disabledXX")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_24(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("ZERO-OPPORTUNITY COVERAGE MUST BE MEASURED, NOT DISABLED")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_25(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = None
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_26(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered * total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_27(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") or not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_28(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate == float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_29(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(None) and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_30(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_31(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(None, exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_32(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, None, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_33(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=None):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_34(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(exact, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_35(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, abs_tol=0.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_36(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, ):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_37(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=1.000001):
            raise ValueError("coverage rate disagrees with detailed counts")


def x_validate_coverage_rate__mutmut_38(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError(None)


def x_validate_coverage_rate__mutmut_39(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("XXcoverage rate disagrees with detailed countsXX")


def x_validate_coverage_rate__mutmut_40(value: str | None, covered: int, total: int) -> None:
    """Check a rounded summary against its detailed integer evidence."""
    if value is None:
        raise ValueError("missing coverage rate")
    rate = float(value)
    if not math.isfinite(rate) or not 0 <= rate <= 1:
        raise ValueError("coverage rate must be finite and between zero and one")
    if not total and rate != 1:
        # A branch-enabled Coverage.py report uses 1 for a branchless file.
        # A line-only report uses 0: it has no branch measurement to admit.
        raise ValueError("zero-opportunity coverage must be measured, not disabled")
    if total:
        exact = covered / total
        # Coverage.py's Cobertura producer writes four significant digits.
        # This tolerance validates summaries only: floors use integer detail.
        if rate != float(f"{exact:.4g}") and not math.isclose(rate, exact, abs_tol=0.000001):
            raise ValueError("COVERAGE RATE DISAGREES WITH DETAILED COUNTS")

mutants_x_validate_coverage_rate__mutmut['_mutmut_orig'] = x_validate_coverage_rate__mutmut_orig # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_1'] = x_validate_coverage_rate__mutmut_1 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_2'] = x_validate_coverage_rate__mutmut_2 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_3'] = x_validate_coverage_rate__mutmut_3 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_4'] = x_validate_coverage_rate__mutmut_4 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_5'] = x_validate_coverage_rate__mutmut_5 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_6'] = x_validate_coverage_rate__mutmut_6 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_7'] = x_validate_coverage_rate__mutmut_7 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_8'] = x_validate_coverage_rate__mutmut_8 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_9'] = x_validate_coverage_rate__mutmut_9 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_10'] = x_validate_coverage_rate__mutmut_10 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_11'] = x_validate_coverage_rate__mutmut_11 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_12'] = x_validate_coverage_rate__mutmut_12 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_13'] = x_validate_coverage_rate__mutmut_13 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_14'] = x_validate_coverage_rate__mutmut_14 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_15'] = x_validate_coverage_rate__mutmut_15 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_16'] = x_validate_coverage_rate__mutmut_16 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_17'] = x_validate_coverage_rate__mutmut_17 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_18'] = x_validate_coverage_rate__mutmut_18 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_19'] = x_validate_coverage_rate__mutmut_19 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_20'] = x_validate_coverage_rate__mutmut_20 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_21'] = x_validate_coverage_rate__mutmut_21 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_22'] = x_validate_coverage_rate__mutmut_22 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_23'] = x_validate_coverage_rate__mutmut_23 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_24'] = x_validate_coverage_rate__mutmut_24 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_25'] = x_validate_coverage_rate__mutmut_25 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_26'] = x_validate_coverage_rate__mutmut_26 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_27'] = x_validate_coverage_rate__mutmut_27 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_28'] = x_validate_coverage_rate__mutmut_28 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_29'] = x_validate_coverage_rate__mutmut_29 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_30'] = x_validate_coverage_rate__mutmut_30 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_31'] = x_validate_coverage_rate__mutmut_31 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_32'] = x_validate_coverage_rate__mutmut_32 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_33'] = x_validate_coverage_rate__mutmut_33 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_34'] = x_validate_coverage_rate__mutmut_34 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_35'] = x_validate_coverage_rate__mutmut_35 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_36'] = x_validate_coverage_rate__mutmut_36 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_37'] = x_validate_coverage_rate__mutmut_37 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_38'] = x_validate_coverage_rate__mutmut_38 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_39'] = x_validate_coverage_rate__mutmut_39 # type: ignore # mutmut generated
mutants_x_validate_coverage_rate__mutmut['x_validate_coverage_rate__mutmut_40'] = x_validate_coverage_rate__mutmut_40 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_count_class_coverage__mutmut)
def count_class_coverage(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_orig(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_1(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_2(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(None)
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_3(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = None
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_4(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding=None)
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_5(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="XXutf-8XX")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_6(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="UTF-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_7(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = None
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_8(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = None
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_9(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find(None)
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_10(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.rfind("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_11(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("XXlinesXX")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_12(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("LINES")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_13(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is not None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_14(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError(None)
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_15(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("XXmissing coverage line detailXX")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_16(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("MISSING COVERAGE LINE DETAIL")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_17(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = None
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_18(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = None
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_19(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 1
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_20(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag == "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_21(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "XXlineXX":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_22(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "LINE":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_23(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError(None)
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_24(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("XXunexpected coverage line detailXX")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_25(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("UNEXPECTED COVERAGE LINE DETAIL")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_26(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = None
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_27(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(None)
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_28(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get(None))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_29(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("XXnumberXX"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_30(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("NUMBER"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_31(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = None
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_32(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(None)
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_33(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get(None))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_34(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("XXhitsXX"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_35(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("HITS"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_36(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines and number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_37(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_38(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 2 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_39(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 < number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_40(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number < physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_41(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number not in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_42(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError(None)
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_43(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("XXcoverage line number is duplicate or outside sourceXX")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_44(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("COVERAGE LINE NUMBER IS DUPLICATE OR OUTSIDE SOURCE")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_45(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(None)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_46(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines = int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_47(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines -= int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_48(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(None)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_49(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits >= 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_50(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 1)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_51(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = None
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_52(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get(None)
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_53(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("XXbranchXX")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_54(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("BRANCH")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_55(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_56(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "XXfalseXX", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_57(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "FALSE", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_58(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "XXtrueXX"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_59(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "TRUE"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_60(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError(None)
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_61(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("XXinvalid coverage branch flagXX")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_62(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("INVALID COVERAGE BRANCH FLAG")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_63(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = None
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_64(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get(None)
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_65(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("XXcondition-coverageXX")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_66(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("CONDITION-COVERAGE")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_67(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch == "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_68(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "XXtrueXX":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_69(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "TRUE":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_70(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_71(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError(None)
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_72(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("XXcondition coverage without a branchXX")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_73(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("CONDITION COVERAGE WITHOUT A BRANCH")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_74(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            break
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_75(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = None
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_76(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(None, condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_77(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", None)
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_78(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_79(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", )
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_80(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"XX([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)XX", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_81(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition and "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_82(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "XXXX")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_83(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is not None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_84(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError(None)
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_85(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("XXmissing or malformed branch coverage detailXX")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_86(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("MISSING OR MALFORMED BRANCH COVERAGE DETAIL")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_87(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = None
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_88(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(None), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_89(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[3]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_90(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(None)
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_91(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[4])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_92(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total and (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_93(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 and covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_94(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total != 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_95(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 1 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_96(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered >= total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_97(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered or not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_98(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_99(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError(None)
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_100(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("XXinvalid detailed branch countsXX")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_101(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("INVALID DETAILED BRANCH COUNTS")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_102(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_103(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(None, 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_104(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), None, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_105(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=None):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_106(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_107(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_108(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, ):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_109(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(None), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_110(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[2]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_111(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered * total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_112(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 / covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_113(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 101 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_114(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=2):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_115(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError(None)
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_116(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("XXbranch percentage disagrees with detailed countsXX")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_117(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("BRANCH PERCENTAGE DISAGREES WITH DETAILED COUNTS")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_118(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches = total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_119(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches -= total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_120(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches = covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_121(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches -= covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_122(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen or ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_123(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_124(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(None).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_125(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError(None)
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_126(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("XXmissing coverage detail for non-empty sourceXX")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_127(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("MISSING COVERAGE DETAIL FOR NON-EMPTY SOURCE")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_128(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = None
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_129(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(None, covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_130(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), None, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_131(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, None, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_132(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, None)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_133(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_134(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_135(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_136(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, )
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_137(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(None, counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_138(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), None, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_139(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, None)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_140(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_141(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_142(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, )
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_143(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get(None), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_144(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("XXline-rateXX"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_145(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("LINE-RATE"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_146(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(None, counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_147(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), None, counts.branches)
    return counts


def x_count_class_coverage__mutmut_148(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, None)
    return counts


def x_count_class_coverage__mutmut_149(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_150(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.branches)
    return counts


def x_count_class_coverage__mutmut_151(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("branch-rate"), counts.covered_branches, )
    return counts


def x_count_class_coverage__mutmut_152(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get(None), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_153(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("XXbranch-rateXX"), counts.covered_branches, counts.branches)
    return counts


def x_count_class_coverage__mutmut_154(element: Any, source: Path) -> CoverageCounts:
    """Validate Cobertura detail for one real Python source file.

    This validates evidence consistency, not report authenticity: exact-source
    digest and execution bindings belong to coverage receipt admission.
    """
    if not source.is_file():
        raise ValueError(f"coverage source file is missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    physical_lines = len(source_text.splitlines())
    details = element.find("lines")
    if details is None:
        raise ValueError("missing coverage line detail")
    seen: set[int] = set()
    covered_lines = branches = covered_branches = 0
    for line in details:
        if line.tag != "line":
            raise ValueError("unexpected coverage line detail")
        number = coverage_integer(line.get("number"))
        hits = coverage_integer(line.get("hits"))
        if not 1 <= number <= physical_lines or number in seen:
            raise ValueError("coverage line number is duplicate or outside source")
        seen.add(number)
        covered_lines += int(hits > 0)
        branch = line.get("branch")
        if branch not in {None, "false", "true"}:
            raise ValueError("invalid coverage branch flag")
        condition = line.get("condition-coverage")
        if branch != "true":
            if condition is not None:
                raise ValueError("condition coverage without a branch")
            continue
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)% \(([0-9]+)/([0-9]+)\)", condition or "")
        if match is None:
            raise ValueError("missing or malformed branch coverage detail")
        covered, total = int(match[2]), int(match[3])
        if total == 0 or covered > total or (covered and not hits):
            raise ValueError("invalid detailed branch counts")
        if not math.isclose(float(match[1]), 100 * covered / total, abs_tol=1):
            raise ValueError("branch percentage disagrees with detailed counts")
        branches += total
        covered_branches += covered
    if not seen and ast.parse(source_text).body:
        raise ValueError("missing coverage detail for non-empty source")
    counts = CoverageCounts(len(seen), covered_lines, branches, covered_branches)
    validate_coverage_rate(element.get("line-rate"), counts.covered_lines, counts.lines)
    validate_coverage_rate(element.get("BRANCH-RATE"), counts.covered_branches, counts.branches)
    return counts

mutants_x_count_class_coverage__mutmut['_mutmut_orig'] = x_count_class_coverage__mutmut_orig # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_1'] = x_count_class_coverage__mutmut_1 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_2'] = x_count_class_coverage__mutmut_2 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_3'] = x_count_class_coverage__mutmut_3 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_4'] = x_count_class_coverage__mutmut_4 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_5'] = x_count_class_coverage__mutmut_5 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_6'] = x_count_class_coverage__mutmut_6 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_7'] = x_count_class_coverage__mutmut_7 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_8'] = x_count_class_coverage__mutmut_8 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_9'] = x_count_class_coverage__mutmut_9 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_10'] = x_count_class_coverage__mutmut_10 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_11'] = x_count_class_coverage__mutmut_11 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_12'] = x_count_class_coverage__mutmut_12 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_13'] = x_count_class_coverage__mutmut_13 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_14'] = x_count_class_coverage__mutmut_14 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_15'] = x_count_class_coverage__mutmut_15 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_16'] = x_count_class_coverage__mutmut_16 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_17'] = x_count_class_coverage__mutmut_17 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_18'] = x_count_class_coverage__mutmut_18 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_19'] = x_count_class_coverage__mutmut_19 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_20'] = x_count_class_coverage__mutmut_20 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_21'] = x_count_class_coverage__mutmut_21 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_22'] = x_count_class_coverage__mutmut_22 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_23'] = x_count_class_coverage__mutmut_23 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_24'] = x_count_class_coverage__mutmut_24 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_25'] = x_count_class_coverage__mutmut_25 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_26'] = x_count_class_coverage__mutmut_26 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_27'] = x_count_class_coverage__mutmut_27 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_28'] = x_count_class_coverage__mutmut_28 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_29'] = x_count_class_coverage__mutmut_29 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_30'] = x_count_class_coverage__mutmut_30 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_31'] = x_count_class_coverage__mutmut_31 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_32'] = x_count_class_coverage__mutmut_32 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_33'] = x_count_class_coverage__mutmut_33 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_34'] = x_count_class_coverage__mutmut_34 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_35'] = x_count_class_coverage__mutmut_35 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_36'] = x_count_class_coverage__mutmut_36 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_37'] = x_count_class_coverage__mutmut_37 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_38'] = x_count_class_coverage__mutmut_38 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_39'] = x_count_class_coverage__mutmut_39 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_40'] = x_count_class_coverage__mutmut_40 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_41'] = x_count_class_coverage__mutmut_41 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_42'] = x_count_class_coverage__mutmut_42 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_43'] = x_count_class_coverage__mutmut_43 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_44'] = x_count_class_coverage__mutmut_44 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_45'] = x_count_class_coverage__mutmut_45 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_46'] = x_count_class_coverage__mutmut_46 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_47'] = x_count_class_coverage__mutmut_47 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_48'] = x_count_class_coverage__mutmut_48 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_49'] = x_count_class_coverage__mutmut_49 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_50'] = x_count_class_coverage__mutmut_50 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_51'] = x_count_class_coverage__mutmut_51 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_52'] = x_count_class_coverage__mutmut_52 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_53'] = x_count_class_coverage__mutmut_53 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_54'] = x_count_class_coverage__mutmut_54 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_55'] = x_count_class_coverage__mutmut_55 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_56'] = x_count_class_coverage__mutmut_56 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_57'] = x_count_class_coverage__mutmut_57 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_58'] = x_count_class_coverage__mutmut_58 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_59'] = x_count_class_coverage__mutmut_59 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_60'] = x_count_class_coverage__mutmut_60 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_61'] = x_count_class_coverage__mutmut_61 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_62'] = x_count_class_coverage__mutmut_62 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_63'] = x_count_class_coverage__mutmut_63 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_64'] = x_count_class_coverage__mutmut_64 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_65'] = x_count_class_coverage__mutmut_65 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_66'] = x_count_class_coverage__mutmut_66 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_67'] = x_count_class_coverage__mutmut_67 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_68'] = x_count_class_coverage__mutmut_68 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_69'] = x_count_class_coverage__mutmut_69 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_70'] = x_count_class_coverage__mutmut_70 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_71'] = x_count_class_coverage__mutmut_71 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_72'] = x_count_class_coverage__mutmut_72 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_73'] = x_count_class_coverage__mutmut_73 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_74'] = x_count_class_coverage__mutmut_74 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_75'] = x_count_class_coverage__mutmut_75 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_76'] = x_count_class_coverage__mutmut_76 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_77'] = x_count_class_coverage__mutmut_77 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_78'] = x_count_class_coverage__mutmut_78 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_79'] = x_count_class_coverage__mutmut_79 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_80'] = x_count_class_coverage__mutmut_80 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_81'] = x_count_class_coverage__mutmut_81 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_82'] = x_count_class_coverage__mutmut_82 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_83'] = x_count_class_coverage__mutmut_83 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_84'] = x_count_class_coverage__mutmut_84 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_85'] = x_count_class_coverage__mutmut_85 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_86'] = x_count_class_coverage__mutmut_86 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_87'] = x_count_class_coverage__mutmut_87 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_88'] = x_count_class_coverage__mutmut_88 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_89'] = x_count_class_coverage__mutmut_89 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_90'] = x_count_class_coverage__mutmut_90 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_91'] = x_count_class_coverage__mutmut_91 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_92'] = x_count_class_coverage__mutmut_92 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_93'] = x_count_class_coverage__mutmut_93 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_94'] = x_count_class_coverage__mutmut_94 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_95'] = x_count_class_coverage__mutmut_95 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_96'] = x_count_class_coverage__mutmut_96 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_97'] = x_count_class_coverage__mutmut_97 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_98'] = x_count_class_coverage__mutmut_98 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_99'] = x_count_class_coverage__mutmut_99 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_100'] = x_count_class_coverage__mutmut_100 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_101'] = x_count_class_coverage__mutmut_101 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_102'] = x_count_class_coverage__mutmut_102 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_103'] = x_count_class_coverage__mutmut_103 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_104'] = x_count_class_coverage__mutmut_104 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_105'] = x_count_class_coverage__mutmut_105 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_106'] = x_count_class_coverage__mutmut_106 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_107'] = x_count_class_coverage__mutmut_107 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_108'] = x_count_class_coverage__mutmut_108 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_109'] = x_count_class_coverage__mutmut_109 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_110'] = x_count_class_coverage__mutmut_110 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_111'] = x_count_class_coverage__mutmut_111 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_112'] = x_count_class_coverage__mutmut_112 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_113'] = x_count_class_coverage__mutmut_113 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_114'] = x_count_class_coverage__mutmut_114 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_115'] = x_count_class_coverage__mutmut_115 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_116'] = x_count_class_coverage__mutmut_116 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_117'] = x_count_class_coverage__mutmut_117 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_118'] = x_count_class_coverage__mutmut_118 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_119'] = x_count_class_coverage__mutmut_119 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_120'] = x_count_class_coverage__mutmut_120 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_121'] = x_count_class_coverage__mutmut_121 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_122'] = x_count_class_coverage__mutmut_122 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_123'] = x_count_class_coverage__mutmut_123 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_124'] = x_count_class_coverage__mutmut_124 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_125'] = x_count_class_coverage__mutmut_125 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_126'] = x_count_class_coverage__mutmut_126 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_127'] = x_count_class_coverage__mutmut_127 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_128'] = x_count_class_coverage__mutmut_128 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_129'] = x_count_class_coverage__mutmut_129 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_130'] = x_count_class_coverage__mutmut_130 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_131'] = x_count_class_coverage__mutmut_131 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_132'] = x_count_class_coverage__mutmut_132 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_133'] = x_count_class_coverage__mutmut_133 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_134'] = x_count_class_coverage__mutmut_134 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_135'] = x_count_class_coverage__mutmut_135 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_136'] = x_count_class_coverage__mutmut_136 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_137'] = x_count_class_coverage__mutmut_137 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_138'] = x_count_class_coverage__mutmut_138 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_139'] = x_count_class_coverage__mutmut_139 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_140'] = x_count_class_coverage__mutmut_140 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_141'] = x_count_class_coverage__mutmut_141 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_142'] = x_count_class_coverage__mutmut_142 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_143'] = x_count_class_coverage__mutmut_143 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_144'] = x_count_class_coverage__mutmut_144 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_145'] = x_count_class_coverage__mutmut_145 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_146'] = x_count_class_coverage__mutmut_146 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_147'] = x_count_class_coverage__mutmut_147 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_148'] = x_count_class_coverage__mutmut_148 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_149'] = x_count_class_coverage__mutmut_149 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_150'] = x_count_class_coverage__mutmut_150 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_151'] = x_count_class_coverage__mutmut_151 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_152'] = x_count_class_coverage__mutmut_152 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_153'] = x_count_class_coverage__mutmut_153 # type: ignore # mutmut generated
mutants_x_count_class_coverage__mutmut['x_count_class_coverage__mutmut_154'] = x_count_class_coverage__mutmut_154 # type: ignore # mutmut generated
mutants_x__relative_to_repository__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__relative_to_repository__mutmut)
def _relative_to_repository(candidate: Path, repo_root: Path) -> str:
    try:
        return candidate.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"coverage path is outside the repository: {candidate}") from exc


def x__relative_to_repository__mutmut_orig(candidate: Path, repo_root: Path) -> str:
    try:
        return candidate.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"coverage path is outside the repository: {candidate}") from exc


def x__relative_to_repository__mutmut_1(candidate: Path, repo_root: Path) -> str:
    try:
        return candidate.resolve().relative_to(None).as_posix()
    except ValueError as exc:
        raise ValueError(f"coverage path is outside the repository: {candidate}") from exc


def x__relative_to_repository__mutmut_2(candidate: Path, repo_root: Path) -> str:
    try:
        return candidate.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(None) from exc

mutants_x__relative_to_repository__mutmut['_mutmut_orig'] = x__relative_to_repository__mutmut_orig # type: ignore # mutmut generated
mutants_x__relative_to_repository__mutmut['x__relative_to_repository__mutmut_1'] = x__relative_to_repository__mutmut_1 # type: ignore # mutmut generated
mutants_x__relative_to_repository__mutmut['x__relative_to_repository__mutmut_2'] = x__relative_to_repository__mutmut_2 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_resolve_coverage_filename__mutmut)
def resolve_coverage_filename(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_orig(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_1(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = None
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_2(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(None)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_3(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = None
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_4(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(None)
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_5(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(None) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_6(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value or value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_7(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value == ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_8(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != "XX.XX")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_9(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is not None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_10(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_11(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) == 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_12(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 2:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_13(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(None)
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_14(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = None
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_15(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[1]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_16(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source * declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_17(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] != source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_18(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source * declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_19(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = None
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_20(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(None, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_21(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, None)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_22(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_23(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, )

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_24(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = None
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_25(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = None
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_26(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root * source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_27(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(None)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_28(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base * declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_29(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(None)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_30(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root * declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_31(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = None
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_32(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) != 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_33(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 2:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_34(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(None, root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_35(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), None)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_36(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_37(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), )
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_38(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) >= 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_39(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 2:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_40(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = None
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_41(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(None)
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_42(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = "XX, XX".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_43(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(None))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_44(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(None)

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_45(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_46(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = None
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_47(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(None, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_48(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, None) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_49(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_50(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, ) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_51(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root * source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_52(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = None
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_53(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(None)]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_54(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") - "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_55(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip(None) + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_56(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.lstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_57(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("XX/XX") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_58(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "XX/XX")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_59(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) != 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_60(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 2:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_61(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) != 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_62(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 2:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_63(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = None
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_64(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(None)
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_65(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[1])
        return (source / declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_66(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source * declared).as_posix()
    raise ValueError(f"coverage filename has ambiguous source roots: {filename}")


def x_resolve_coverage_filename__mutmut_67(
    filename: str,
    source_roots: Iterable[str],
    *,
    repo_root: Path | None,
) -> str:
    """Resolve one Cobertura class filename to a stable repository path.

    Existing files decide between multiple source roots. When a synthetic
    report has no materialised source tree, one relative source root remains a
    deterministic fallback. Multiple unresolved roots are ambiguous and fail.
    """
    declared = Path(filename)
    sources = tuple(Path(value) for value in source_roots if value and value != ".")
    if repo_root is None:
        if declared.is_absolute():
            return declared.as_posix()
        if not sources:
            return declared.as_posix()
        if len(sources) != 1:
            raise ValueError(f"coverage filename has ambiguous source roots: {filename}")
        source = sources[0]
        if source.is_absolute():
            return (source / declared).as_posix()
        if declared.parts[: len(source.parts)] == source.parts:
            return declared.as_posix()
        return (source / declared).as_posix()

    root = repo_root.resolve()
    if declared.is_absolute():
        return _relative_to_repository(declared, root)

    candidates: list[Path] = []
    for source in sources:
        base = source if source.is_absolute() else root / source
        candidates.append(base / declared)
    candidates.append(root / declared)
    existing = {candidate.resolve() for candidate in candidates if candidate.is_file()}
    if len(existing) == 1:
        return _relative_to_repository(existing.pop(), root)
    if len(existing) > 1:
        paths = ", ".join(sorted(path.as_posix() for path in existing))
        raise ValueError(f"coverage filename resolves to multiple repository files: {filename}: {paths}")

    if not sources:
        return declared.as_posix()
    repo_sources = [
        _relative_to_repository(source if source.is_absolute() else root / source, root) for source in sources
    ]
    matching = [source for source in repo_sources if declared.as_posix().startswith(source.rstrip("/") + "/")]
    if len(matching) == 1:
        return declared.as_posix()
    if len(repo_sources) == 1:
        source = Path(repo_sources[0])
        return (source / declared).as_posix()
    raise ValueError(None)

mutants_x_resolve_coverage_filename__mutmut['_mutmut_orig'] = x_resolve_coverage_filename__mutmut_orig # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_1'] = x_resolve_coverage_filename__mutmut_1 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_2'] = x_resolve_coverage_filename__mutmut_2 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_3'] = x_resolve_coverage_filename__mutmut_3 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_4'] = x_resolve_coverage_filename__mutmut_4 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_5'] = x_resolve_coverage_filename__mutmut_5 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_6'] = x_resolve_coverage_filename__mutmut_6 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_7'] = x_resolve_coverage_filename__mutmut_7 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_8'] = x_resolve_coverage_filename__mutmut_8 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_9'] = x_resolve_coverage_filename__mutmut_9 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_10'] = x_resolve_coverage_filename__mutmut_10 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_11'] = x_resolve_coverage_filename__mutmut_11 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_12'] = x_resolve_coverage_filename__mutmut_12 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_13'] = x_resolve_coverage_filename__mutmut_13 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_14'] = x_resolve_coverage_filename__mutmut_14 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_15'] = x_resolve_coverage_filename__mutmut_15 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_16'] = x_resolve_coverage_filename__mutmut_16 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_17'] = x_resolve_coverage_filename__mutmut_17 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_18'] = x_resolve_coverage_filename__mutmut_18 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_19'] = x_resolve_coverage_filename__mutmut_19 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_20'] = x_resolve_coverage_filename__mutmut_20 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_21'] = x_resolve_coverage_filename__mutmut_21 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_22'] = x_resolve_coverage_filename__mutmut_22 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_23'] = x_resolve_coverage_filename__mutmut_23 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_24'] = x_resolve_coverage_filename__mutmut_24 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_25'] = x_resolve_coverage_filename__mutmut_25 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_26'] = x_resolve_coverage_filename__mutmut_26 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_27'] = x_resolve_coverage_filename__mutmut_27 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_28'] = x_resolve_coverage_filename__mutmut_28 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_29'] = x_resolve_coverage_filename__mutmut_29 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_30'] = x_resolve_coverage_filename__mutmut_30 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_31'] = x_resolve_coverage_filename__mutmut_31 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_32'] = x_resolve_coverage_filename__mutmut_32 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_33'] = x_resolve_coverage_filename__mutmut_33 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_34'] = x_resolve_coverage_filename__mutmut_34 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_35'] = x_resolve_coverage_filename__mutmut_35 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_36'] = x_resolve_coverage_filename__mutmut_36 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_37'] = x_resolve_coverage_filename__mutmut_37 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_38'] = x_resolve_coverage_filename__mutmut_38 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_39'] = x_resolve_coverage_filename__mutmut_39 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_40'] = x_resolve_coverage_filename__mutmut_40 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_41'] = x_resolve_coverage_filename__mutmut_41 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_42'] = x_resolve_coverage_filename__mutmut_42 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_43'] = x_resolve_coverage_filename__mutmut_43 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_44'] = x_resolve_coverage_filename__mutmut_44 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_45'] = x_resolve_coverage_filename__mutmut_45 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_46'] = x_resolve_coverage_filename__mutmut_46 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_47'] = x_resolve_coverage_filename__mutmut_47 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_48'] = x_resolve_coverage_filename__mutmut_48 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_49'] = x_resolve_coverage_filename__mutmut_49 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_50'] = x_resolve_coverage_filename__mutmut_50 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_51'] = x_resolve_coverage_filename__mutmut_51 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_52'] = x_resolve_coverage_filename__mutmut_52 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_53'] = x_resolve_coverage_filename__mutmut_53 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_54'] = x_resolve_coverage_filename__mutmut_54 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_55'] = x_resolve_coverage_filename__mutmut_55 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_56'] = x_resolve_coverage_filename__mutmut_56 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_57'] = x_resolve_coverage_filename__mutmut_57 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_58'] = x_resolve_coverage_filename__mutmut_58 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_59'] = x_resolve_coverage_filename__mutmut_59 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_60'] = x_resolve_coverage_filename__mutmut_60 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_61'] = x_resolve_coverage_filename__mutmut_61 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_62'] = x_resolve_coverage_filename__mutmut_62 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_63'] = x_resolve_coverage_filename__mutmut_63 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_64'] = x_resolve_coverage_filename__mutmut_64 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_65'] = x_resolve_coverage_filename__mutmut_65 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_66'] = x_resolve_coverage_filename__mutmut_66 # type: ignore # mutmut generated
mutants_x_resolve_coverage_filename__mutmut['x_resolve_coverage_filename__mutmut_67'] = x_resolve_coverage_filename__mutmut_67 # type: ignore # mutmut generated


__all__ = ["resolve_coverage_filename"]
