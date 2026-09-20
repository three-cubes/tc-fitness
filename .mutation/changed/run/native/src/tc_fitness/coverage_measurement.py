"""Cross-check bound Coverage.py JSON/XML against source-derived branch arcs."""

from __future__ import annotations

import importlib
import json
import re
from pathlib import Path
from typing import Any

from tc_fitness.core_checks._coverage_evidence import CoverageCounts, resolve_coverage_filename


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__integers__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__integers__mutmut)
def _integers(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_orig(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_1(value: object) -> set[int]:
    if not isinstance(value, list) and any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_2(value: object) -> set[int]:
    if isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_3(value: object) -> set[int]:
    if not isinstance(value, list) or any(None):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_4(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(None) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_5(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_6(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError(None)
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_7(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("XXcoverage JSON requires integer line detailXX")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_8(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage json requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_9(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("COVERAGE JSON REQUIRES INTEGER LINE DETAIL")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_10(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) == len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(value)


def x__integers__mutmut_11(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError(None)
    return set(value)


def x__integers__mutmut_12(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("XXcoverage JSON contains duplicate linesXX")
    return set(value)


def x__integers__mutmut_13(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage json contains duplicate lines")
    return set(value)


def x__integers__mutmut_14(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("COVERAGE JSON CONTAINS DUPLICATE LINES")
    return set(value)


def x__integers__mutmut_15(value: object) -> set[int]:
    if not isinstance(value, list) or any(type(item) is not int for item in value):
        raise ValueError("coverage JSON requires integer line detail")
    if len(value) != len(set(value)):
        raise ValueError("coverage JSON contains duplicate lines")
    return set(None)

mutants_x__integers__mutmut['_mutmut_orig'] = x__integers__mutmut_orig # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_1'] = x__integers__mutmut_1 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_2'] = x__integers__mutmut_2 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_3'] = x__integers__mutmut_3 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_4'] = x__integers__mutmut_4 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_5'] = x__integers__mutmut_5 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_6'] = x__integers__mutmut_6 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_7'] = x__integers__mutmut_7 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_8'] = x__integers__mutmut_8 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_9'] = x__integers__mutmut_9 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_10'] = x__integers__mutmut_10 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_11'] = x__integers__mutmut_11 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_12'] = x__integers__mutmut_12 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_13'] = x__integers__mutmut_13 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_14'] = x__integers__mutmut_14 # type: ignore # mutmut generated
mutants_x__integers__mutmut['x__integers__mutmut_15'] = x__integers__mutmut_15 # type: ignore # mutmut generated
mutants_x__arcs__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__arcs__mutmut)
def _arcs(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_orig(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_1(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) and any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_2(value: object) -> set[tuple[int, int]]:
    if isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_3(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        None
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_4(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 and any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_5(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) and len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_6(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_7(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) == 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_8(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 3 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_9(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(None)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_10(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(None) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_11(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_12(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError(None)
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_13(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("XXcoverage JSON requires branch arc pairsXX")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_14(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage json requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_15(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("COVERAGE JSON REQUIRES BRANCH ARC PAIRS")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_16(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = None
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_17(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[1], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_18(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[2]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_19(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) == len(value):
        raise ValueError("coverage JSON contains duplicate branch arcs")
    return result


def x__arcs__mutmut_20(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError(None)
    return result


def x__arcs__mutmut_21(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("XXcoverage JSON contains duplicate branch arcsXX")
    return result


def x__arcs__mutmut_22(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("coverage json contains duplicate branch arcs")
    return result


def x__arcs__mutmut_23(value: object) -> set[tuple[int, int]]:
    if not isinstance(value, list) or any(
        not isinstance(arc, list) or len(arc) != 2 or any(type(line) is not int for line in arc)
        for arc in value
    ):
        raise ValueError("coverage JSON requires branch arc pairs")
    result = {(arc[0], arc[1]) for arc in value}
    if len(result) != len(value):
        raise ValueError("COVERAGE JSON CONTAINS DUPLICATE BRANCH ARCS")
    return result

mutants_x__arcs__mutmut['_mutmut_orig'] = x__arcs__mutmut_orig # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_1'] = x__arcs__mutmut_1 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_2'] = x__arcs__mutmut_2 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_3'] = x__arcs__mutmut_3 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_4'] = x__arcs__mutmut_4 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_5'] = x__arcs__mutmut_5 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_6'] = x__arcs__mutmut_6 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_7'] = x__arcs__mutmut_7 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_8'] = x__arcs__mutmut_8 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_9'] = x__arcs__mutmut_9 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_10'] = x__arcs__mutmut_10 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_11'] = x__arcs__mutmut_11 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_12'] = x__arcs__mutmut_12 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_13'] = x__arcs__mutmut_13 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_14'] = x__arcs__mutmut_14 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_15'] = x__arcs__mutmut_15 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_16'] = x__arcs__mutmut_16 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_17'] = x__arcs__mutmut_17 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_18'] = x__arcs__mutmut_18 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_19'] = x__arcs__mutmut_19 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_20'] = x__arcs__mutmut_20 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_21'] = x__arcs__mutmut_21 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_22'] = x__arcs__mutmut_22 # type: ignore # mutmut generated
mutants_x__arcs__mutmut['x__arcs__mutmut_23'] = x__arcs__mutmut_23 # type: ignore # mutmut generated
mutants_x__summary__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__summary__mutmut)
def _summary(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_orig(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_1(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = None
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_2(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "XXnum_statementsXX": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_3(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "NUM_STATEMENTS": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_4(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "XXcovered_linesXX": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_5(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "COVERED_LINES": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_6(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "XXmissing_linesXX": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_7(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "MISSING_LINES": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_8(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines + counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_9(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "XXexcluded_linesXX": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_10(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "EXCLUDED_LINES": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_11(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 1,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_12(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "XXnum_branchesXX": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_13(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "NUM_BRANCHES": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_14(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "XXcovered_branchesXX": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_15(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "COVERED_BRANCHES": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_16(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "XXmissing_branchesXX": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_17(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "MISSING_BRANCHES": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_18(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches + counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_19(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(None):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_20(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int and summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_21(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(None) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_22(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(None)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_23(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_24(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] == value for key, value in expected.items()):
        raise ValueError("coverage JSON summary counts disagree with source detail")


def x__summary__mutmut_25(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError(None)


def x__summary__mutmut_26(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("XXcoverage JSON summary counts disagree with source detailXX")


def x__summary__mutmut_27(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("coverage json summary counts disagree with source detail")


def x__summary__mutmut_28(summary: dict[str, Any], counts: CoverageCounts) -> None:
    expected = {
        "num_statements": counts.lines,
        "covered_lines": counts.covered_lines,
        "missing_lines": counts.lines - counts.covered_lines,
        "excluded_lines": 0,
        "num_branches": counts.branches,
        "covered_branches": counts.covered_branches,
        "missing_branches": counts.branches - counts.covered_branches,
    }
    if any(type(summary.get(key)) is not int or summary[key] != value for key, value in expected.items()):
        raise ValueError("COVERAGE JSON SUMMARY COUNTS DISAGREE WITH SOURCE DETAIL")

mutants_x__summary__mutmut['_mutmut_orig'] = x__summary__mutmut_orig # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_1'] = x__summary__mutmut_1 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_2'] = x__summary__mutmut_2 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_3'] = x__summary__mutmut_3 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_4'] = x__summary__mutmut_4 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_5'] = x__summary__mutmut_5 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_6'] = x__summary__mutmut_6 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_7'] = x__summary__mutmut_7 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_8'] = x__summary__mutmut_8 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_9'] = x__summary__mutmut_9 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_10'] = x__summary__mutmut_10 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_11'] = x__summary__mutmut_11 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_12'] = x__summary__mutmut_12 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_13'] = x__summary__mutmut_13 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_14'] = x__summary__mutmut_14 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_15'] = x__summary__mutmut_15 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_16'] = x__summary__mutmut_16 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_17'] = x__summary__mutmut_17 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_18'] = x__summary__mutmut_18 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_19'] = x__summary__mutmut_19 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_20'] = x__summary__mutmut_20 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_21'] = x__summary__mutmut_21 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_22'] = x__summary__mutmut_22 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_23'] = x__summary__mutmut_23 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_24'] = x__summary__mutmut_24 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_25'] = x__summary__mutmut_25 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_26'] = x__summary__mutmut_26 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_27'] = x__summary__mutmut_27 # type: ignore # mutmut generated
mutants_x__summary__mutmut['x__summary__mutmut_28'] = x__summary__mutmut_28 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_cross_check_branches__mutmut)
def cross_check_branches(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_orig(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_1(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = None
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_2(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(None)
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_3(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(None).read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_4(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix("XX.jsonXX").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_5(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".JSON").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_6(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get(None) is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_7(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["XXmetaXX"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_8(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["META"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_9(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("XXbranch_coverageXX") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_10(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("BRANCH_COVERAGE") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_11(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_12(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not False:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_13(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError(None)
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_14(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("XXcoverage JSON must contain branch measurementXX")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_15(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage json must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_16(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("COVERAGE JSON MUST CONTAIN BRANCH MEASUREMENT")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_17(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = None
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_18(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(None, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_19(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, None, repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_20(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=None): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_21(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename([], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_22(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_23(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], ): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_24(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["XXfilesXX"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_25(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["FILES"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_26(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) and len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_27(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(None) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_28(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) == set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_29(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(None) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_30(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) == len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_31(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError(None)
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_32(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("XXcoverage JSON does not measure the exact source setXX")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_33(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage json does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_34(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("COVERAGE JSON DOES NOT MEASURE THE EXACT SOURCE SET")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_35(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = None
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_36(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(None).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_37(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = None
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_38(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter(None) if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_39(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("XXsourceXX") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_40(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("SOURCE") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_41(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = None
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_42(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter(None):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_43(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("XXclassXX"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_44(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("CLASS"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_45(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = None
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_46(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(None, sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_47(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), None, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_48(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=None)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_49(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_50(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_51(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, )
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_52(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get(None), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_53(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("XXfilenameXX"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_54(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("FILENAME"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_55(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = None
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_56(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find(None):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_57(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.rfind("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_58(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("XXlinesXX"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_59(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("LINES"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_60(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get(None) == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_61(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("XXbranchXX") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_62(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("BRANCH") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_63(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") != "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_64(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "XXtrueXX":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_65(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "TRUE":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_66(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = None
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_67(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(None, line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_68(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", None)
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_69(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_70(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", )
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_71(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"XX[0-9.]+% \(([0-9]+)/([0-9]+)\)XX", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_72(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get(None, ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_73(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", None))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_74(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get(""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_75(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_76(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("XXcondition-coverageXX", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_77(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("CONDITION-COVERAGE", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_78(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", "XXXX"))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_79(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is not None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_80(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError(None)
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_81(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("XXcoverage XML branch counts are malformedXX")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_82(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage xml branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_83(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("COVERAGE XML BRANCH COUNTS ARE MALFORMED")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_84(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = None
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_85(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(None)] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_86(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get(None))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_87(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("XXnumberXX"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_88(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("NUMBER"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_89(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(None), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_90(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[2]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_91(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(None))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_92(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[3]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_93(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = None
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_94(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = None
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_95(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module(None).PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_96(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("XXcoverage.parserXX").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_97(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("COVERAGE.PARSER").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_98(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = None
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_99(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = None
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_100(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(None)
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_101(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["XXexecuted_linesXX"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_102(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["EXECUTED_LINES"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_103(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = None
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_104(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(None)
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_105(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["XXmissing_linesXX"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_106(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["MISSING_LINES"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_107(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing and executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_108(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] and executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_109(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["XXexcluded_linesXX"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_110(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["EXCLUDED_LINES"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_111(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed | missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_112(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed & missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_113(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing == set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_114(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(None):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_115(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError(None)
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_116(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("XXcoverage JSON line inventory disagrees with source detailXX")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_117(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage json line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_118(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("COVERAGE JSON LINE INVENTORY DISAGREES WITH SOURCE DETAIL")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_119(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed == {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_120(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit >= 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_121(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 1}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_122(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError(None)
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_123(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("XXcoverage XML and JSON disagree on executed linesXX")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_124(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage xml and json disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_125(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("COVERAGE XML AND JSON DISAGREE ON EXECUTED LINES")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_126(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = None
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_127(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=None, exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_128(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_129(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), )
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_130(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(None), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_131(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = None
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_132(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = None
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_133(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] >= 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_134(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 2}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_135(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = None
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_136(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(None), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_137(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["XXexecuted_branchesXX"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_138(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["EXECUTED_BRANCHES"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_139(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(None)
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_140(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["XXmissing_branchesXX"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_141(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["MISSING_BRANCHES"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_142(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent and taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_143(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken | absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_144(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken & absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_145(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent == possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_146(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError(None)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_147(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " - name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_148(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("XXcoverage JSON branch arcs disagree with source opportunities: XX" + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_149(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage json branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_150(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("COVERAGE JSON BRANCH ARCS DISAGREE WITH SOURCE OPPORTUNITIES: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_151(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = None
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_152(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(None), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_153(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin != start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_154(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total >= 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_155(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 2
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_156(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] == expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_157(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError(None)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_158(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " - name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_159(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("XXcoverage XML branch detail disagrees with source and JSON: XX" + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_160(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage xml branch detail disagrees with source and json: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_161(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("COVERAGE XML BRANCH DETAIL DISAGREES WITH SOURCE AND JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_162(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(None, counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_163(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], None)
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_164(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_165(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], )
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_166(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["XXsummaryXX"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_167(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["SUMMARY"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_168(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = None
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_169(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(None)
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_170(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(None, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_171(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, None) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_172(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_173(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, ) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_174(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("XXlinesXX", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_175(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("LINES", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_176(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "XXcovered_linesXX", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_177(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "COVERED_LINES", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_178(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "XXbranchesXX", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_179(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "BRANCHES", "covered_branches")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_180(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "XXcovered_branchesXX")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_181(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "COVERED_BRANCHES")
        }
    )
    _summary(payload["totals"], total)


def x_cross_check_branches__mutmut_182(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(None, total)


def x_cross_check_branches__mutmut_183(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], None)


def x_cross_check_branches__mutmut_184(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(total)


def x_cross_check_branches__mutmut_185(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["totals"], )


def x_cross_check_branches__mutmut_186(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["XXtotalsXX"], total)


def x_cross_check_branches__mutmut_187(
    root: Path,
    report: Path,
    files: dict[str, Path],
    hits: dict[str, dict[int, int]],
    counts: dict[str, CoverageCounts],
) -> None:
    """Neither XML nor JSON can omit branch opportunities present in source."""
    from tc_fitness.core_checks.coverage_floor import _resolve_element_tree

    payload = json.loads(report.with_suffix(".json").read_text())
    if payload["meta"].get("branch_coverage") is not True:
        raise ValueError("coverage JSON must contain branch measurement")
    documents = {
        resolve_coverage_filename(name, [], repo_root=root): detail
        for name, detail in payload["files"].items()
    }
    if set(documents) != set(files) or len(documents) != len(payload["files"]):
        raise ValueError("coverage JSON does not measure the exact source set")
    xml = _resolve_element_tree().parse(report).getroot()
    sources = [node.text for node in xml.iter("source") if node.text]
    xml_branches = {}
    for element in xml.iter("class"):
        relative = resolve_coverage_filename(element.get("filename"), sources, repo_root=root)
        branches = {}
        for line in element.find("lines"):
            if line.get("branch") == "true":
                match = re.fullmatch(r"[0-9.]+% \(([0-9]+)/([0-9]+)\)", line.get("condition-coverage", ""))
                if match is None:
                    raise ValueError("coverage XML branch counts are malformed")
                branches[int(line.get("number"))] = (int(match[1]), int(match[2]))
        xml_branches[relative] = branches
    parser_type = importlib.import_module("coverage.parser").PythonParser
    for name, path in files.items():
        detail = documents[name]
        executed = _integers(detail["executed_lines"])
        missing = _integers(detail["missing_lines"])
        if detail["excluded_lines"] or executed & missing or executed | missing != set(hits[name]):
            raise ValueError("coverage JSON line inventory disagrees with source detail")
        if executed != {line for line, hit in hits[name].items() if hit > 0}:
            raise ValueError("coverage XML and JSON disagree on executed lines")
        parser = parser_type(filename=str(path), exclude=None)
        parser.parse_source()
        exits = parser.exit_counts()
        possible = {(start, end) for start, end in parser.arcs() if exits[start] > 1}
        taken, absent = _arcs(detail["executed_branches"]), _arcs(detail["missing_branches"])
        if taken & absent or taken | absent != possible:
            raise ValueError("coverage JSON branch arcs disagree with source opportunities: " + name)
        expected = {
            start: (sum(origin == start for origin, _ in taken), total)
            for start, total in exits.items()
            if total > 1
        }
        if xml_branches[name] != expected:
            raise ValueError("coverage XML branch detail disagrees with source and JSON: " + name)
        _summary(detail["summary"], counts[name])
    total = CoverageCounts(
        **{
            key: sum(getattr(value, key) for value in counts.values())
            for key in ("lines", "covered_lines", "branches", "covered_branches")
        }
    )
    _summary(payload["TOTALS"], total)

mutants_x_cross_check_branches__mutmut['_mutmut_orig'] = x_cross_check_branches__mutmut_orig # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_1'] = x_cross_check_branches__mutmut_1 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_2'] = x_cross_check_branches__mutmut_2 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_3'] = x_cross_check_branches__mutmut_3 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_4'] = x_cross_check_branches__mutmut_4 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_5'] = x_cross_check_branches__mutmut_5 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_6'] = x_cross_check_branches__mutmut_6 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_7'] = x_cross_check_branches__mutmut_7 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_8'] = x_cross_check_branches__mutmut_8 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_9'] = x_cross_check_branches__mutmut_9 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_10'] = x_cross_check_branches__mutmut_10 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_11'] = x_cross_check_branches__mutmut_11 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_12'] = x_cross_check_branches__mutmut_12 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_13'] = x_cross_check_branches__mutmut_13 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_14'] = x_cross_check_branches__mutmut_14 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_15'] = x_cross_check_branches__mutmut_15 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_16'] = x_cross_check_branches__mutmut_16 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_17'] = x_cross_check_branches__mutmut_17 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_18'] = x_cross_check_branches__mutmut_18 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_19'] = x_cross_check_branches__mutmut_19 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_20'] = x_cross_check_branches__mutmut_20 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_21'] = x_cross_check_branches__mutmut_21 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_22'] = x_cross_check_branches__mutmut_22 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_23'] = x_cross_check_branches__mutmut_23 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_24'] = x_cross_check_branches__mutmut_24 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_25'] = x_cross_check_branches__mutmut_25 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_26'] = x_cross_check_branches__mutmut_26 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_27'] = x_cross_check_branches__mutmut_27 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_28'] = x_cross_check_branches__mutmut_28 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_29'] = x_cross_check_branches__mutmut_29 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_30'] = x_cross_check_branches__mutmut_30 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_31'] = x_cross_check_branches__mutmut_31 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_32'] = x_cross_check_branches__mutmut_32 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_33'] = x_cross_check_branches__mutmut_33 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_34'] = x_cross_check_branches__mutmut_34 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_35'] = x_cross_check_branches__mutmut_35 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_36'] = x_cross_check_branches__mutmut_36 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_37'] = x_cross_check_branches__mutmut_37 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_38'] = x_cross_check_branches__mutmut_38 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_39'] = x_cross_check_branches__mutmut_39 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_40'] = x_cross_check_branches__mutmut_40 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_41'] = x_cross_check_branches__mutmut_41 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_42'] = x_cross_check_branches__mutmut_42 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_43'] = x_cross_check_branches__mutmut_43 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_44'] = x_cross_check_branches__mutmut_44 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_45'] = x_cross_check_branches__mutmut_45 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_46'] = x_cross_check_branches__mutmut_46 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_47'] = x_cross_check_branches__mutmut_47 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_48'] = x_cross_check_branches__mutmut_48 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_49'] = x_cross_check_branches__mutmut_49 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_50'] = x_cross_check_branches__mutmut_50 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_51'] = x_cross_check_branches__mutmut_51 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_52'] = x_cross_check_branches__mutmut_52 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_53'] = x_cross_check_branches__mutmut_53 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_54'] = x_cross_check_branches__mutmut_54 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_55'] = x_cross_check_branches__mutmut_55 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_56'] = x_cross_check_branches__mutmut_56 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_57'] = x_cross_check_branches__mutmut_57 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_58'] = x_cross_check_branches__mutmut_58 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_59'] = x_cross_check_branches__mutmut_59 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_60'] = x_cross_check_branches__mutmut_60 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_61'] = x_cross_check_branches__mutmut_61 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_62'] = x_cross_check_branches__mutmut_62 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_63'] = x_cross_check_branches__mutmut_63 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_64'] = x_cross_check_branches__mutmut_64 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_65'] = x_cross_check_branches__mutmut_65 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_66'] = x_cross_check_branches__mutmut_66 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_67'] = x_cross_check_branches__mutmut_67 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_68'] = x_cross_check_branches__mutmut_68 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_69'] = x_cross_check_branches__mutmut_69 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_70'] = x_cross_check_branches__mutmut_70 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_71'] = x_cross_check_branches__mutmut_71 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_72'] = x_cross_check_branches__mutmut_72 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_73'] = x_cross_check_branches__mutmut_73 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_74'] = x_cross_check_branches__mutmut_74 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_75'] = x_cross_check_branches__mutmut_75 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_76'] = x_cross_check_branches__mutmut_76 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_77'] = x_cross_check_branches__mutmut_77 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_78'] = x_cross_check_branches__mutmut_78 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_79'] = x_cross_check_branches__mutmut_79 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_80'] = x_cross_check_branches__mutmut_80 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_81'] = x_cross_check_branches__mutmut_81 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_82'] = x_cross_check_branches__mutmut_82 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_83'] = x_cross_check_branches__mutmut_83 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_84'] = x_cross_check_branches__mutmut_84 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_85'] = x_cross_check_branches__mutmut_85 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_86'] = x_cross_check_branches__mutmut_86 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_87'] = x_cross_check_branches__mutmut_87 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_88'] = x_cross_check_branches__mutmut_88 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_89'] = x_cross_check_branches__mutmut_89 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_90'] = x_cross_check_branches__mutmut_90 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_91'] = x_cross_check_branches__mutmut_91 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_92'] = x_cross_check_branches__mutmut_92 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_93'] = x_cross_check_branches__mutmut_93 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_94'] = x_cross_check_branches__mutmut_94 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_95'] = x_cross_check_branches__mutmut_95 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_96'] = x_cross_check_branches__mutmut_96 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_97'] = x_cross_check_branches__mutmut_97 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_98'] = x_cross_check_branches__mutmut_98 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_99'] = x_cross_check_branches__mutmut_99 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_100'] = x_cross_check_branches__mutmut_100 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_101'] = x_cross_check_branches__mutmut_101 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_102'] = x_cross_check_branches__mutmut_102 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_103'] = x_cross_check_branches__mutmut_103 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_104'] = x_cross_check_branches__mutmut_104 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_105'] = x_cross_check_branches__mutmut_105 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_106'] = x_cross_check_branches__mutmut_106 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_107'] = x_cross_check_branches__mutmut_107 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_108'] = x_cross_check_branches__mutmut_108 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_109'] = x_cross_check_branches__mutmut_109 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_110'] = x_cross_check_branches__mutmut_110 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_111'] = x_cross_check_branches__mutmut_111 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_112'] = x_cross_check_branches__mutmut_112 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_113'] = x_cross_check_branches__mutmut_113 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_114'] = x_cross_check_branches__mutmut_114 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_115'] = x_cross_check_branches__mutmut_115 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_116'] = x_cross_check_branches__mutmut_116 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_117'] = x_cross_check_branches__mutmut_117 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_118'] = x_cross_check_branches__mutmut_118 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_119'] = x_cross_check_branches__mutmut_119 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_120'] = x_cross_check_branches__mutmut_120 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_121'] = x_cross_check_branches__mutmut_121 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_122'] = x_cross_check_branches__mutmut_122 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_123'] = x_cross_check_branches__mutmut_123 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_124'] = x_cross_check_branches__mutmut_124 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_125'] = x_cross_check_branches__mutmut_125 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_126'] = x_cross_check_branches__mutmut_126 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_127'] = x_cross_check_branches__mutmut_127 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_128'] = x_cross_check_branches__mutmut_128 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_129'] = x_cross_check_branches__mutmut_129 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_130'] = x_cross_check_branches__mutmut_130 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_131'] = x_cross_check_branches__mutmut_131 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_132'] = x_cross_check_branches__mutmut_132 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_133'] = x_cross_check_branches__mutmut_133 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_134'] = x_cross_check_branches__mutmut_134 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_135'] = x_cross_check_branches__mutmut_135 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_136'] = x_cross_check_branches__mutmut_136 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_137'] = x_cross_check_branches__mutmut_137 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_138'] = x_cross_check_branches__mutmut_138 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_139'] = x_cross_check_branches__mutmut_139 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_140'] = x_cross_check_branches__mutmut_140 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_141'] = x_cross_check_branches__mutmut_141 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_142'] = x_cross_check_branches__mutmut_142 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_143'] = x_cross_check_branches__mutmut_143 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_144'] = x_cross_check_branches__mutmut_144 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_145'] = x_cross_check_branches__mutmut_145 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_146'] = x_cross_check_branches__mutmut_146 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_147'] = x_cross_check_branches__mutmut_147 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_148'] = x_cross_check_branches__mutmut_148 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_149'] = x_cross_check_branches__mutmut_149 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_150'] = x_cross_check_branches__mutmut_150 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_151'] = x_cross_check_branches__mutmut_151 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_152'] = x_cross_check_branches__mutmut_152 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_153'] = x_cross_check_branches__mutmut_153 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_154'] = x_cross_check_branches__mutmut_154 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_155'] = x_cross_check_branches__mutmut_155 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_156'] = x_cross_check_branches__mutmut_156 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_157'] = x_cross_check_branches__mutmut_157 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_158'] = x_cross_check_branches__mutmut_158 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_159'] = x_cross_check_branches__mutmut_159 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_160'] = x_cross_check_branches__mutmut_160 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_161'] = x_cross_check_branches__mutmut_161 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_162'] = x_cross_check_branches__mutmut_162 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_163'] = x_cross_check_branches__mutmut_163 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_164'] = x_cross_check_branches__mutmut_164 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_165'] = x_cross_check_branches__mutmut_165 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_166'] = x_cross_check_branches__mutmut_166 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_167'] = x_cross_check_branches__mutmut_167 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_168'] = x_cross_check_branches__mutmut_168 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_169'] = x_cross_check_branches__mutmut_169 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_170'] = x_cross_check_branches__mutmut_170 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_171'] = x_cross_check_branches__mutmut_171 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_172'] = x_cross_check_branches__mutmut_172 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_173'] = x_cross_check_branches__mutmut_173 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_174'] = x_cross_check_branches__mutmut_174 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_175'] = x_cross_check_branches__mutmut_175 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_176'] = x_cross_check_branches__mutmut_176 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_177'] = x_cross_check_branches__mutmut_177 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_178'] = x_cross_check_branches__mutmut_178 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_179'] = x_cross_check_branches__mutmut_179 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_180'] = x_cross_check_branches__mutmut_180 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_181'] = x_cross_check_branches__mutmut_181 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_182'] = x_cross_check_branches__mutmut_182 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_183'] = x_cross_check_branches__mutmut_183 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_184'] = x_cross_check_branches__mutmut_184 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_185'] = x_cross_check_branches__mutmut_185 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_186'] = x_cross_check_branches__mutmut_186 # type: ignore # mutmut generated
mutants_x_cross_check_branches__mutmut['x_cross_check_branches__mutmut_187'] = x_cross_check_branches__mutmut_187 # type: ignore # mutmut generated
