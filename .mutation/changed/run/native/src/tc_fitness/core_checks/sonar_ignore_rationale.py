"""CORE check: sonar_ignore_rationale — every Sonar rule-ignore is justified.

A SonarCloud ``sonar.issue.ignore.multicriteria.<id>.ruleKey`` entry is a
load-bearing decision that needs visible justification. This check verifies
every such line in the project's Sonar properties file is preceded by a comment
block explaining WHY the rule is ignored — not just THAT it is. A bare or
TODO-only comment block does not count.

Ported from kairix ``scripts/checks/check_sonar_ignore_rationale.py`` (F14) and
re-expressed as a configurable, repo-agnostic rule. The Sonar
properties filename and the rule-key pattern are the rule's own shape
(``DEFAULT_SONAR_FILE`` / ``DEFAULT_RULE_KEY_PATTERN``), overridable via config.
Every unjustified ignore directive is a hard finding.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The conventional Sonar properties filename — overridable per consumer.
DEFAULT_SONAR_FILE = "sonar-project.properties"
#: The multicriteria rule-key line shape — Sonar's own format, overridable.
DEFAULT_RULE_KEY_PATTERN = r"^sonar\.issue\.ignore\.multicriteria\.([A-Za-z0-9_-]+)\.ruleKey="

_BAD_TOKENS = ("todo", "fixme", "xxx")
_MIN_SUBSTANTIVE_LEN = 25

REMEDIATION = _remediation(
    fix=(
        "add a comment block immediately above each multicriteria .ruleKey line "
        "explaining WHY the rule is ignored — at least one comment line with an "
        "em-dash and a substantive sentence (TODO/FIXME placeholders do not "
        "count)."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.sonar_ignore_rationale",
    passing="# python:S5547 - HMAC-SHA1 used only for legacy fingerprinting, never security.",
    forbidden="# TODO",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__rationale_lines_above__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__rationale_lines_above__mutmut)
def _rationale_lines_above(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_orig(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_1(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = None
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_2(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = None
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_3(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index + 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_4(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 2
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_5(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = None
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_6(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = True
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_7(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i > 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_8(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 1:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_9(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = None
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_10(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].lstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_11(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith(None):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_12(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.rstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_13(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("XX#XX"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_14(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(None)
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_15(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.rstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_16(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[2:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_17(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = None
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_18(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = True
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_19(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line != "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_20(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "XXXX":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_21(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                return
            blank_skipped = True
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_22(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = None
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_23(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = False
        else:
            break
        i -= 1
    return out


def x__rationale_lines_above__mutmut_24(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            return
        i -= 1
    return out


def x__rationale_lines_above__mutmut_25(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i = 1
    return out


def x__rationale_lines_above__mutmut_26(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i += 1
    return out


def x__rationale_lines_above__mutmut_27(lines: list[str], index: int) -> list[str]:
    """Collect the contiguous comment block ending immediately above ``index``.

    Walks upward through ``#``-prefixed lines, skipping at most one blank line
    between paragraphs; stops at the first non-comment, non-blank line.
    """
    out: list[str] = []
    i = index - 1
    blank_skipped = False
    while i >= 0:
        line = lines[i].rstrip()
        if line.lstrip().startswith("#"):
            out.append(line.lstrip()[1:].strip())
            blank_skipped = False
        elif line == "":
            if blank_skipped:
                break
            blank_skipped = True
        else:
            break
        i -= 2
    return out

mutants_x__rationale_lines_above__mutmut['_mutmut_orig'] = x__rationale_lines_above__mutmut_orig # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_1'] = x__rationale_lines_above__mutmut_1 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_2'] = x__rationale_lines_above__mutmut_2 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_3'] = x__rationale_lines_above__mutmut_3 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_4'] = x__rationale_lines_above__mutmut_4 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_5'] = x__rationale_lines_above__mutmut_5 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_6'] = x__rationale_lines_above__mutmut_6 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_7'] = x__rationale_lines_above__mutmut_7 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_8'] = x__rationale_lines_above__mutmut_8 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_9'] = x__rationale_lines_above__mutmut_9 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_10'] = x__rationale_lines_above__mutmut_10 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_11'] = x__rationale_lines_above__mutmut_11 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_12'] = x__rationale_lines_above__mutmut_12 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_13'] = x__rationale_lines_above__mutmut_13 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_14'] = x__rationale_lines_above__mutmut_14 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_15'] = x__rationale_lines_above__mutmut_15 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_16'] = x__rationale_lines_above__mutmut_16 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_17'] = x__rationale_lines_above__mutmut_17 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_18'] = x__rationale_lines_above__mutmut_18 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_19'] = x__rationale_lines_above__mutmut_19 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_20'] = x__rationale_lines_above__mutmut_20 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_21'] = x__rationale_lines_above__mutmut_21 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_22'] = x__rationale_lines_above__mutmut_22 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_23'] = x__rationale_lines_above__mutmut_23 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_24'] = x__rationale_lines_above__mutmut_24 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_25'] = x__rationale_lines_above__mutmut_25 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_26'] = x__rationale_lines_above__mutmut_26 # type: ignore # mutmut generated
mutants_x__rationale_lines_above__mutmut['x__rationale_lines_above__mutmut_27'] = x__rationale_lines_above__mutmut_27 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_real_rationale__mutmut)
def _has_real_rationale(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_orig(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_1(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line and any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_2(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_3(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(None):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_4(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok not in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_5(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            break
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_6(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line and "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_7(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "XX—XX" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_8(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" not in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_9(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "XX--XX" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_10(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" not in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_11(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return False
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_12(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN or not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_13(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) > _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_14(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and line.startswith("="):
            return True
    return False


def x__has_real_rationale__mutmut_15(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith(None):
            return True
    return False


def x__has_real_rationale__mutmut_16(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("XX=XX"):
            return True
    return False


def x__has_real_rationale__mutmut_17(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return False
    return False


def x__has_real_rationale__mutmut_18(comment_block: list[str]) -> bool:
    """True if the block has an em-dash or a long substantive (non-TODO) line."""
    for line in comment_block:
        if not line or any(tok in line.casefold() for tok in _BAD_TOKENS):
            continue
        if "—" in line or "--" in line:
            return True
        if len(line) >= _MIN_SUBSTANTIVE_LEN and not line.startswith("="):
            return True
    return True

mutants_x__has_real_rationale__mutmut['_mutmut_orig'] = x__has_real_rationale__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_1'] = x__has_real_rationale__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_2'] = x__has_real_rationale__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_3'] = x__has_real_rationale__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_4'] = x__has_real_rationale__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_5'] = x__has_real_rationale__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_6'] = x__has_real_rationale__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_7'] = x__has_real_rationale__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_8'] = x__has_real_rationale__mutmut_8 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_9'] = x__has_real_rationale__mutmut_9 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_10'] = x__has_real_rationale__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_11'] = x__has_real_rationale__mutmut_11 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_12'] = x__has_real_rationale__mutmut_12 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_13'] = x__has_real_rationale__mutmut_13 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_14'] = x__has_real_rationale__mutmut_14 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_15'] = x__has_real_rationale__mutmut_15 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_16'] = x__has_real_rationale__mutmut_16 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_17'] = x__has_real_rationale__mutmut_17 # type: ignore # mutmut generated
mutants_x__has_real_rationale__mutmut['x__has_real_rationale__mutmut_18'] = x__has_real_rationale__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_has_unjustified_ignore__mutmut)
def file_has_unjustified_ignore(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_orig(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_1(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = None
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_2(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding=None).splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_3(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="XXutf-8XX").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_4(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="UTF-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_5(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_6(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = None
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_7(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(None)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_8(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(None):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_9(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) or not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_10(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(None) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_11(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_12(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(None):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_13(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(None, idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_14(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, None)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_15(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(idx)):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_16(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, )):
            return True
    return False


def x_file_has_unjustified_ignore__mutmut_17(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return False
    return False


def x_file_has_unjustified_ignore__mutmut_18(path: Path, *, rule_key_pattern: str) -> bool:
    """True iff ``path`` has a Sonar rule-ignore lacking a preceding rationale.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured properties file could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    rule_re = re.compile(rule_key_pattern)
    for idx, raw in enumerate(lines):
        if rule_re.match(raw.strip()) and not _has_real_rationale(_rationale_lines_above(lines, idx)):
            return True
    return True

mutants_x_file_has_unjustified_ignore__mutmut['_mutmut_orig'] = x_file_has_unjustified_ignore__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_1'] = x_file_has_unjustified_ignore__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_2'] = x_file_has_unjustified_ignore__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_3'] = x_file_has_unjustified_ignore__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_4'] = x_file_has_unjustified_ignore__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_5'] = x_file_has_unjustified_ignore__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_6'] = x_file_has_unjustified_ignore__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_7'] = x_file_has_unjustified_ignore__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_8'] = x_file_has_unjustified_ignore__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_9'] = x_file_has_unjustified_ignore__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_10'] = x_file_has_unjustified_ignore__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_11'] = x_file_has_unjustified_ignore__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_12'] = x_file_has_unjustified_ignore__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_13'] = x_file_has_unjustified_ignore__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_14'] = x_file_has_unjustified_ignore__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_15'] = x_file_has_unjustified_ignore__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_16'] = x_file_has_unjustified_ignore__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_17'] = x_file_has_unjustified_ignore__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_ignore__mutmut['x_file_has_unjustified_ignore__mutmut_18'] = x_file_has_unjustified_ignore__mutmut_18 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁSonarIgnoreRationaleǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁSonarIgnoreRationaleǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁSonarIgnoreRationaleǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class SonarIgnoreRationale(FitnessRule):
    """Flags a Sonar rule-ignore entry that lacks a preceding rationale comment."""

    name = "sonar-ignore-rationale"
    remediation = REMEDIATION
    # Scope is a single named properties file, not an extension family.
    extensions = ()

    #: Rule-specific knobs — overridable per consumer.
    sonar_file: str = DEFAULT_SONAR_FILE
    rule_key_pattern: str = DEFAULT_RULE_KEY_PATTERN
    sonar_file_required: bool = False

    @classmethod
    @_mutmut_mutated(mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = None
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, )
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = None
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(None)
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get(None, DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", None))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get(DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", ))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("XXsonar_fileXX", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("SONAR_FILE", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = None
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(None)
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get(None, DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", None))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get(DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", ))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("XXrule_key_patternXX", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("RULE_KEY_PATTERN", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_22(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = None
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_23(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "XXsonar_fileXX" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_24(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "SONAR_FILE" in config
        return rule

    @classmethod
    def xǁSonarIgnoreRationaleǁfrom_config__mutmut_25(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> SonarIgnoreRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, SonarIgnoreRationale)  # noqa: S101  # narrowing for mypy
        rule.sonar_file = str(config.get("sonar_file", DEFAULT_SONAR_FILE))
        rule.rule_key_pattern = str(config.get("rule_key_pattern", DEFAULT_RULE_KEY_PATTERN))
        rule.sonar_file_required = "sonar_file" not in config
        return rule

    @_mutmut_mutated(mutants_xǁSonarIgnoreRationaleǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Scan the Sonar file; an explicitly configured missing file is incomplete evidence."""
        target = self._repo_root / self.sonar_file
        return [target] if target.is_file() or self.sonar_file_required else []

    def xǁSonarIgnoreRationaleǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Scan the Sonar file; an explicitly configured missing file is incomplete evidence."""
        target = self._repo_root / self.sonar_file
        return [target] if target.is_file() or self.sonar_file_required else []

    def xǁSonarIgnoreRationaleǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Scan the Sonar file; an explicitly configured missing file is incomplete evidence."""
        target = None
        return [target] if target.is_file() or self.sonar_file_required else []

    def xǁSonarIgnoreRationaleǁenumerate_files__mutmut_2(self) -> list[Path]:
        """Scan the Sonar file; an explicitly configured missing file is incomplete evidence."""
        target = self._repo_root * self.sonar_file
        return [target] if target.is_file() or self.sonar_file_required else []

    def xǁSonarIgnoreRationaleǁenumerate_files__mutmut_3(self) -> list[Path]:
        """Scan the Sonar file; an explicitly configured missing file is incomplete evidence."""
        target = self._repo_root / self.sonar_file
        return [target] if target.is_file() and self.sonar_file_required else []

    @_mutmut_mutated(mutants_xǁSonarIgnoreRationaleǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        """The single named target file is always in scope."""
        return rel == self.sonar_file

    def xǁSonarIgnoreRationaleǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        """The single named target file is always in scope."""
        return rel == self.sonar_file

    def xǁSonarIgnoreRationaleǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        """The single named target file is always in scope."""
        return rel != self.sonar_file

    @_mutmut_mutated(mutants_xǁSonarIgnoreRationaleǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_has_unjustified_ignore(path, rule_key_pattern=self.rule_key_pattern)

    def xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_has_unjustified_ignore(path, rule_key_pattern=self.rule_key_pattern)

    def xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_has_unjustified_ignore(None, rule_key_pattern=self.rule_key_pattern)

    def xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_has_unjustified_ignore(path, rule_key_pattern=None)

    def xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_has_unjustified_ignore(rule_key_pattern=self.rule_key_pattern)

    def xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_has_unjustified_ignore(path, )

mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['_mutmut_orig'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_1'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_2'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_3'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_4'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_5'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_6'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_7'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_8'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_9'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_10'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_11'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_12'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_13'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_14'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_15'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_16'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_17'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_18'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_19'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_20'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_21'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_22'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_23'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_24'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfrom_config__mutmut['xǁSonarIgnoreRationaleǁfrom_config__mutmut_25'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfrom_config__mutmut_25 # type: ignore # mutmut generated

mutants_xǁSonarIgnoreRationaleǁenumerate_files__mutmut['_mutmut_orig'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁenumerate_files__mutmut['xǁSonarIgnoreRationaleǁenumerate_files__mutmut_1'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁenumerate_files__mutmut['xǁSonarIgnoreRationaleǁenumerate_files__mutmut_2'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁenumerate_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁenumerate_files__mutmut['xǁSonarIgnoreRationaleǁenumerate_files__mutmut_3'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁenumerate_files__mutmut_3 # type: ignore # mutmut generated

mutants_xǁSonarIgnoreRationaleǁis_in_scope__mutmut['_mutmut_orig'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁis_in_scope__mutmut['xǁSonarIgnoreRationaleǁis_in_scope__mutmut_1'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁis_in_scope__mutmut_1 # type: ignore # mutmut generated

mutants_xǁSonarIgnoreRationaleǁfile_has_violation__mutmut['_mutmut_orig'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfile_has_violation__mutmut['xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_1'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfile_has_violation__mutmut['xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_2'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfile_has_violation__mutmut['xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_3'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁSonarIgnoreRationaleǁfile_has_violation__mutmut['xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_4'] = SonarIgnoreRationale.xǁSonarIgnoreRationaleǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SonarIgnoreRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SonarIgnoreRationale.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SonarIgnoreRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SonarIgnoreRationale.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SonarIgnoreRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SonarIgnoreRationale.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SonarIgnoreRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SonarIgnoreRationale.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SonarIgnoreRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SonarIgnoreRationale.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> SonarIgnoreRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return SonarIgnoreRationale.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SonarIgnoreRationale, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SonarIgnoreRationale, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SonarIgnoreRationale, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(SonarIgnoreRationale, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
