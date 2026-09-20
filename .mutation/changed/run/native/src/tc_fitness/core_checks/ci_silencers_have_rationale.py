"""CORE check: ci_silencers_have_rationale — every CI/local silencer is justified.

A CI or local quality silencer (``continue-on-error: true``, ``|| true``,
``--cov-fail-under=0``, ``if: ${{ always() }}``) hides a failing step. Left
undocumented it rots into a permanently-green gate that catches nothing. A
silencer PASSES when the same line OR an adjacent line (within a small window)
carries a rationale token or a trailing ``# <text>`` comment.

Ported from tc-agent-zone ``scripts/checks/ci_silencers.py`` (F10) and
re-expressed as a configurable, repo-agnostic rule. The silencer and rationale
token shapes are CI idioms (the rule's own domain-intrinsic ``DEFAULT_*``),
overridable via config; the workflow directory and the named scan-file list
come from config. No repo paths are baked in.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Rationale tokens that justify a silencer when found nearby — CI idiom, overridable.
DEFAULT_RATIONALE_TOKENS: tuple[str, ...] = (
    "quality-harness",
    "intentional",
    "rationale",
    "non-blocking",
    "best-effort",
    "compatibility",
)
#: Silencer constructs the rule scans for — CI idiom, overridable.
DEFAULT_SILENCER_PATTERNS: tuple[str, ...] = (
    r"continue-on-error\s*:\s*true",
    r"fail_ci_if_error\s*:\s*false",
    r"\|\|\s*true",
    r"--cov-fail-under=0",
    r"if:\s*\$\{\{\s*always\(\)",
)
#: How many lines either side of a silencer count as "nearby". Overridable.
DEFAULT_WINDOW = 2
#: The CI workflow directory globbed for ``*.yml`` / ``*.yaml``. Overridable.
DEFAULT_WORKFLOWS_DIR = ".github/workflows"

REMEDIATION = _remediation(
    fix=(
        "add a same-line trailing # <reason> comment explaining why the silencer "
        "is safe, OR place a comment containing one of the recognised rationale "
        "tokens (quality-harness / intentional / rationale / non-blocking / "
        "best-effort / compatibility) within the configured window."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.ci_silencers_have_rationale",
    passing="continue-on-error: true  # non-blocking: advisory lint job",
    forbidden="continue-on-error: true",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__has_nearby_rationale__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_nearby_rationale__mutmut)
def _has_nearby_rationale(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_orig(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_1(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = None
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_2(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(None, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_3(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, None)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_4(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_5(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, )
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_6(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(1, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_7(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index + window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_8(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = None
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_9(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(None, index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_10(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), None)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_11(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_12(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), )
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_13(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window - 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_14(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index - window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_15(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 2)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_16(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search(None):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_17(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(None)):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_18(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("XX\nXX".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_19(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return False
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_20(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = None
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_21(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line or line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_22(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "XX#XX" in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_23(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" not in line and line.split("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_24(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split(None, 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_25(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", None)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_26(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split(1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_27(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", )[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_28(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.rsplit("#", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_29(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("XX#XX", 1)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_30(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 2)[1].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_31(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[2].strip():
        return True
    return False


def x__has_nearby_rationale__mutmut_32(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return False
    return False


def x__has_nearby_rationale__mutmut_33(
    lines: list[str],
    index: int,
    *,
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    start = max(0, index - window)
    end = min(len(lines), index + window + 1)
    if rationale_re.search("\n".join(lines[start:end])):
        return True
    line = lines[index]
    if "#" in line and line.split("#", 1)[1].strip():
        return True
    return True

mutants_x__has_nearby_rationale__mutmut['_mutmut_orig'] = x__has_nearby_rationale__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_1'] = x__has_nearby_rationale__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_2'] = x__has_nearby_rationale__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_3'] = x__has_nearby_rationale__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_4'] = x__has_nearby_rationale__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_5'] = x__has_nearby_rationale__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_6'] = x__has_nearby_rationale__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_7'] = x__has_nearby_rationale__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_8'] = x__has_nearby_rationale__mutmut_8 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_9'] = x__has_nearby_rationale__mutmut_9 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_10'] = x__has_nearby_rationale__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_11'] = x__has_nearby_rationale__mutmut_11 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_12'] = x__has_nearby_rationale__mutmut_12 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_13'] = x__has_nearby_rationale__mutmut_13 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_14'] = x__has_nearby_rationale__mutmut_14 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_15'] = x__has_nearby_rationale__mutmut_15 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_16'] = x__has_nearby_rationale__mutmut_16 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_17'] = x__has_nearby_rationale__mutmut_17 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_18'] = x__has_nearby_rationale__mutmut_18 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_19'] = x__has_nearby_rationale__mutmut_19 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_20'] = x__has_nearby_rationale__mutmut_20 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_21'] = x__has_nearby_rationale__mutmut_21 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_22'] = x__has_nearby_rationale__mutmut_22 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_23'] = x__has_nearby_rationale__mutmut_23 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_24'] = x__has_nearby_rationale__mutmut_24 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_25'] = x__has_nearby_rationale__mutmut_25 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_26'] = x__has_nearby_rationale__mutmut_26 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_27'] = x__has_nearby_rationale__mutmut_27 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_28'] = x__has_nearby_rationale__mutmut_28 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_29'] = x__has_nearby_rationale__mutmut_29 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_30'] = x__has_nearby_rationale__mutmut_30 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_31'] = x__has_nearby_rationale__mutmut_31 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_32'] = x__has_nearby_rationale__mutmut_32 # type: ignore # mutmut generated
mutants_x__has_nearby_rationale__mutmut['x__has_nearby_rationale__mutmut_33'] = x__has_nearby_rationale__mutmut_33 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_has_unjustified_silencer__mutmut)
def file_has_unjustified_silencer(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_orig(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_1(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = None
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_2(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding=None).splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_3(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="XXutf-8XX").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_4(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="UTF-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_5(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_6(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(None):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_7(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) or not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_8(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(None) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_9(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_10(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            None, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_11(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, None, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_12(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=None, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_13(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=None
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_14(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            idx, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_15(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, rationale_re=rationale_re, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_16(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, window=window
        ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_17(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, ):
            return True
    return False


def x_file_has_unjustified_silencer__mutmut_18(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return False
    return False


def x_file_has_unjustified_silencer__mutmut_19(
    path: Path,
    *,
    silencer_re: re.Pattern[str],
    rationale_re: re.Pattern[str],
    window: int,
) -> bool:
    """True iff ``path`` has a silencer line lacking a nearby rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is treated as "no violation".
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        if silencer_re.search(line) and not _has_nearby_rationale(
            lines, idx, rationale_re=rationale_re, window=window
        ):
            return True
    return True

mutants_x_file_has_unjustified_silencer__mutmut['_mutmut_orig'] = x_file_has_unjustified_silencer__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_1'] = x_file_has_unjustified_silencer__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_2'] = x_file_has_unjustified_silencer__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_3'] = x_file_has_unjustified_silencer__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_4'] = x_file_has_unjustified_silencer__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_5'] = x_file_has_unjustified_silencer__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_6'] = x_file_has_unjustified_silencer__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_7'] = x_file_has_unjustified_silencer__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_8'] = x_file_has_unjustified_silencer__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_9'] = x_file_has_unjustified_silencer__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_10'] = x_file_has_unjustified_silencer__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_11'] = x_file_has_unjustified_silencer__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_12'] = x_file_has_unjustified_silencer__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_13'] = x_file_has_unjustified_silencer__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_14'] = x_file_has_unjustified_silencer__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_15'] = x_file_has_unjustified_silencer__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_16'] = x_file_has_unjustified_silencer__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_17'] = x_file_has_unjustified_silencer__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_18'] = x_file_has_unjustified_silencer__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_silencer__mutmut['x_file_has_unjustified_silencer__mutmut_19'] = x_file_has_unjustified_silencer__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiSilencersHaveRationaleǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class CiSilencersHaveRationale(FitnessRule):
    """Flags a CI/local file holding a rationale-free quality silencer."""

    name = "ci-silencers-have-rationale"
    remediation = REMEDIATION
    # Enumeration is custom (workflow glob + named scan files), so extension
    # scoping is not used for selection.
    extensions = ()

    #: Rule-specific knobs — overridable per consumer.
    rationale_tokens: tuple[str, ...] = DEFAULT_RATIONALE_TOKENS
    silencer_patterns: tuple[str, ...] = DEFAULT_SILENCER_PATTERNS
    window: int = DEFAULT_WINDOW
    workflows_dir: str = DEFAULT_WORKFLOWS_DIR
    #: Extra named files (shell/python harnesses) to scan; supplied via config.
    scan_files: tuple[str, ...] = ()

    @classmethod
    @_mutmut_mutated(mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = None
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, )
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = None
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get(None)
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("XXrationale_tokensXX")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("RATIONALE_TOKENS")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = None
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(None) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = None
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get(None)
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("XXsilencer_patternsXX")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("SILENCER_PATTERNS")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = None
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(None) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = None
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(None)
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get(None, DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", None))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get(DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", ))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_26(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("XXwindowXX", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_27(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("WINDOW", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_28(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = None
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_29(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(None)
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_30(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get(None, DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_31(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", None))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_32(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get(DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_33(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", ))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_34(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("XXworkflows_dirXX", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_35(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("WORKFLOWS_DIR", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_36(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = None
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_37(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get(None)
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_38(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("XXscan_filesXX")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_39(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("SCAN_FILES")
        rule.scan_files = tuple(scans) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_40(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = None
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_41(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(None) if scans is not None else ()
        return rule

    @classmethod
    def xǁCiSilencersHaveRationaleǁfrom_config__mutmut_42(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> CiSilencersHaveRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, CiSilencersHaveRationale)  # noqa: S101  # narrowing for mypy
        tokens = config.get("rationale_tokens")
        rule.rationale_tokens = tuple(tokens) if tokens is not None else DEFAULT_RATIONALE_TOKENS
        sil = config.get("silencer_patterns")
        rule.silencer_patterns = tuple(sil) if sil is not None else DEFAULT_SILENCER_PATTERNS
        rule.window = int(config.get("window", DEFAULT_WINDOW))
        rule.workflows_dir = str(config.get("workflows_dir", DEFAULT_WORKFLOWS_DIR))
        scans = config.get("scan_files")
        rule.scan_files = tuple(scans) if scans is None else ()
        return rule

    @_mutmut_mutated(mutants_xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut)
    def _silencer_re(self) -> re.Pattern[str]:
        return re.compile("|".join(f"(?:{p})" for p in self.silencer_patterns))

    def xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_orig(self) -> re.Pattern[str]:
        return re.compile("|".join(f"(?:{p})" for p in self.silencer_patterns))

    def xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_1(self) -> re.Pattern[str]:
        return re.compile(None)

    def xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_2(self) -> re.Pattern[str]:
        return re.compile("|".join(None))

    def xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_3(self) -> re.Pattern[str]:
        return re.compile("XX|XX".join(f"(?:{p})" for p in self.silencer_patterns))

    @_mutmut_mutated(mutants_xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut)
    def _rationale_re(self) -> re.Pattern[str]:
        return re.compile("|".join(re.escape(t) for t in self.rationale_tokens), re.IGNORECASE)

    def xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_orig(self) -> re.Pattern[str]:
        return re.compile("|".join(re.escape(t) for t in self.rationale_tokens), re.IGNORECASE)

    def xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_1(self) -> re.Pattern[str]:
        return re.compile(None, re.IGNORECASE)

    def xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_2(self) -> re.Pattern[str]:
        return re.compile("|".join(re.escape(t) for t in self.rationale_tokens), None)

    def xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_3(self) -> re.Pattern[str]:
        return re.compile(re.IGNORECASE)

    def xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_4(self) -> re.Pattern[str]:
        return re.compile("|".join(re.escape(t) for t in self.rationale_tokens), )

    def xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_5(self) -> re.Pattern[str]:
        return re.compile("|".join(None), re.IGNORECASE)

    def xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_6(self) -> re.Pattern[str]:
        return re.compile("XX|XX".join(re.escape(t) for t in self.rationale_tokens), re.IGNORECASE)

    def xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_7(self) -> re.Pattern[str]:
        return re.compile("|".join(re.escape(None) for t in self.rationale_tokens), re.IGNORECASE)

    @_mutmut_mutated(mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = None
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_2(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = None
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_3(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root * self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_4(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("XX*.ymlXX", "*.yaml"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_5(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.YML", "*.yaml"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_6(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "XX*.yamlXX"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_7(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.YAML"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_8(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(None)
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_9(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(sorted(None))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_10(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(sorted(wf.glob(None)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_11(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = None
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_12(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root * rel
            if target.is_file():
                out.append(target)
        return out

    def xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_13(self) -> list[Path]:
        """Glob the workflow dir for YAML, plus any explicitly named scan files."""
        out: list[Path] = []
        wf = self._repo_root / self.workflows_dir
        if wf.exists():
            for pattern in ("*.yml", "*.yaml"):
                out.extend(sorted(wf.glob(pattern)))
        for rel in self.scan_files:
            target = self._repo_root / rel
            if target.is_file():
                out.append(None)
        return out

    @_mutmut_mutated(mutants_xǁCiSilencersHaveRationaleǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        """Scope is whatever enumeration returns; exempt-file filtering applies upstream."""
        return True

    def xǁCiSilencersHaveRationaleǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        """Scope is whatever enumeration returns; exempt-file filtering applies upstream."""
        return True

    def xǁCiSilencersHaveRationaleǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        """Scope is whatever enumeration returns; exempt-file filtering applies upstream."""
        return False

    @_mutmut_mutated(mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_has_unjustified_silencer(
            path,
            silencer_re=self._silencer_re(),
            rationale_re=self._rationale_re(),
            window=self.window,
        )

    def xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_has_unjustified_silencer(
            path,
            silencer_re=self._silencer_re(),
            rationale_re=self._rationale_re(),
            window=self.window,
        )

    def xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_has_unjustified_silencer(
            None,
            silencer_re=self._silencer_re(),
            rationale_re=self._rationale_re(),
            window=self.window,
        )

    def xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_has_unjustified_silencer(
            path,
            silencer_re=None,
            rationale_re=self._rationale_re(),
            window=self.window,
        )

    def xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_has_unjustified_silencer(
            path,
            silencer_re=self._silencer_re(),
            rationale_re=None,
            window=self.window,
        )

    def xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_has_unjustified_silencer(
            path,
            silencer_re=self._silencer_re(),
            rationale_re=self._rationale_re(),
            window=None,
        )

    def xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        return file_has_unjustified_silencer(
            silencer_re=self._silencer_re(),
            rationale_re=self._rationale_re(),
            window=self.window,
        )

    def xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        return file_has_unjustified_silencer(
            path,
            rationale_re=self._rationale_re(),
            window=self.window,
        )

    def xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        return file_has_unjustified_silencer(
            path,
            silencer_re=self._silencer_re(),
            window=self.window,
        )

    def xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_8(self, path: Path) -> bool:
        return file_has_unjustified_silencer(
            path,
            silencer_re=self._silencer_re(),
            rationale_re=self._rationale_re(),
            )

mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['_mutmut_orig'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_1'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_2'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_3'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_4'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_5'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_6'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_7'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_8'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_9'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_10'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_11'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_12'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_13'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_14'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_15'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_16'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_17'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_18'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_19'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_20'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_21'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_22'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_23'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_24'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_25'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_26'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_27'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_28'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_29'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_30'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_31'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_32'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_33'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_34'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_35'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_36'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_37'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_38'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_38 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_39'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_39 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_40'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_40 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_41'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_41 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfrom_config__mutmut['xǁCiSilencersHaveRationaleǁfrom_config__mutmut_42'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfrom_config__mutmut_42 # type: ignore # mutmut generated

mutants_xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut['_mutmut_orig'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut['xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_1'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut['xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_2'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut['xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_3'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_silencer_re__mutmut_3 # type: ignore # mutmut generated

mutants_xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut['_mutmut_orig'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut['xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_1'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut['xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_2'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut['xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_3'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut['xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_4'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut['xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_5'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut['xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_6'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut['xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_7'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁ_rationale_re__mutmut_7 # type: ignore # mutmut generated

mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['_mutmut_orig'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_1'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_2'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_3'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_4'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_5'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_6'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_7'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_8'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_9'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_10'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_11'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_12'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁenumerate_files__mutmut['xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_13'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁenumerate_files__mutmut_13 # type: ignore # mutmut generated

mutants_xǁCiSilencersHaveRationaleǁis_in_scope__mutmut['_mutmut_orig'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁis_in_scope__mutmut['xǁCiSilencersHaveRationaleǁis_in_scope__mutmut_1'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁis_in_scope__mutmut_1 # type: ignore # mutmut generated

mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut['_mutmut_orig'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut['xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_1'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut['xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_2'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut['xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_3'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut['xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_4'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut['xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_5'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut['xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_6'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut['xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_7'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut['xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_8'] = CiSilencersHaveRationale.xǁCiSilencersHaveRationaleǁfile_has_violation__mutmut_8 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CiSilencersHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiSilencersHaveRationale.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CiSilencersHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiSilencersHaveRationale.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CiSilencersHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiSilencersHaveRationale.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CiSilencersHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiSilencersHaveRationale.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CiSilencersHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiSilencersHaveRationale.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CiSilencersHaveRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return CiSilencersHaveRationale.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiSilencersHaveRationale, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiSilencersHaveRationale, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiSilencersHaveRationale, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(CiSilencersHaveRationale, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
