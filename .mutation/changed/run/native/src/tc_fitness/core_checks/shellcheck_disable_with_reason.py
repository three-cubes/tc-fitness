"""CORE check: shellcheck_disable_with_reason — every shell silencer is justified.

A bare ``# shellcheck disable=SC2034`` is a silent override — six months later
nobody knows whether it is still load-bearing or whether the underlying warning
has become a real bug. An inline rationale (or one on the immediately preceding
``#`` comment line) documents WHY the rule doesn't apply. The shell counterpart
to the Python suppression-rationale rule.

Ported from kairix ``scripts/checks/check_shellcheck_disable_with_reason.py``
(F33) and re-expressed as a configurable, repo-agnostic rule.
The disable-directive shape, the rationale markers, and the minimum rationale
length are the rule's own shape (``DEFAULT_*``), overridable via config; the
consumer supplies ``roots``. No repo paths are baked in.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

# Matches ``# shellcheck disable=SC2034`` (and comma-lists), capturing the tail.
_DISABLE_RE = re.compile(r"#\s*shellcheck\s+disable=(?P<rules>[A-Za-z0-9,]+)(?P<trailing>.*)$")
# A file is a shell script if its name ends in ``.sh`` OR its first line is a
# recognised shell shebang.
_SHEBANG_RE = re.compile(r"^#!\s*(?:/usr/bin/env\s+)?(?:ba)?sh\b")

#: Canonical rationale-marker prefixes — the rule's own shape, overridable.
DEFAULT_RATIONALE_MARKERS: tuple[str, ...] = (
    "fix:",
    "next:",
    "run:",
    "why:",
    "rationale:",
    "reason:",
    "because:",
)
#: Minimum free-text rationale length below which a comment is a stub. Overridable.
DEFAULT_MIN_RATIONALE_LEN = 10

REMEDIATION = _remediation(
    fix=(
        "add an inline comment after the directive that explains WHY the rule "
        "doesn't apply (an em-dash + one-line justification is the canonical "
        "shape), OR put the rationale on the immediately preceding # comment "
        "line; the markers fix:/next:/run:/why:/rationale:/reason:/because: are "
        "recognised."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.shellcheck_disable_with_reason",
    passing="# shellcheck disable=SC2034  # exported via process substitution below",
    forbidden="# shellcheck disable=SC1090",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__is_rationale_comment__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_rationale_comment__mutmut)
def _is_rationale_comment(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_orig(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_1(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") and line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_2(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_3(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith(None) or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_4(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("XX#XX") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_5(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith(None):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_6(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("XX#!XX"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_7(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return True
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_8(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = None
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_9(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip(None).strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_10(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.rstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_11(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("XX#XX").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_12(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_13(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return True
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_14(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = None
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_15(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.upper()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_16(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(None):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_17(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker not in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_18(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return False
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_19(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered or "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_20(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "XXshellcheckXX" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_21(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "SHELLCHECK" in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_22(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" not in lowered and "disable" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_23(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "XXdisableXX" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_24(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "DISABLE" in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_25(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" not in lowered:
        return False
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_26(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return True
    return len(body) >= min_len


def x__is_rationale_comment__mutmut_27(line: str, markers: tuple[str, ...], min_len: int) -> bool:
    if not line.startswith("#") or line.startswith("#!"):
        return False
    body = line.lstrip("#").strip()
    if not body:
        return False
    lowered = body.lower()
    if any(marker in lowered for marker in markers):
        return True
    if "shellcheck" in lowered and "disable" in lowered:
        return False
    return len(body) > min_len

mutants_x__is_rationale_comment__mutmut['_mutmut_orig'] = x__is_rationale_comment__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_1'] = x__is_rationale_comment__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_2'] = x__is_rationale_comment__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_3'] = x__is_rationale_comment__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_4'] = x__is_rationale_comment__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_5'] = x__is_rationale_comment__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_6'] = x__is_rationale_comment__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_7'] = x__is_rationale_comment__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_8'] = x__is_rationale_comment__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_9'] = x__is_rationale_comment__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_10'] = x__is_rationale_comment__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_11'] = x__is_rationale_comment__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_12'] = x__is_rationale_comment__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_13'] = x__is_rationale_comment__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_14'] = x__is_rationale_comment__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_15'] = x__is_rationale_comment__mutmut_15 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_16'] = x__is_rationale_comment__mutmut_16 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_17'] = x__is_rationale_comment__mutmut_17 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_18'] = x__is_rationale_comment__mutmut_18 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_19'] = x__is_rationale_comment__mutmut_19 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_20'] = x__is_rationale_comment__mutmut_20 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_21'] = x__is_rationale_comment__mutmut_21 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_22'] = x__is_rationale_comment__mutmut_22 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_23'] = x__is_rationale_comment__mutmut_23 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_24'] = x__is_rationale_comment__mutmut_24 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_25'] = x__is_rationale_comment__mutmut_25 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_26'] = x__is_rationale_comment__mutmut_26 # type: ignore # mutmut generated
mutants_x__is_rationale_comment__mutmut['x__is_rationale_comment__mutmut_27'] = x__is_rationale_comment__mutmut_27 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__trailing_has_rationale__mutmut)
def _trailing_has_rationale(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_orig(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_1(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = None
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_2(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_3(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return True
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_4(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith(None):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_5(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("XX#XX"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_6(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(None, markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_7(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, None, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_8(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, None)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_9(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_10(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_11(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, )
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_12(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = None
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_13(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.upper()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_14(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(None):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_15(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(marker not in lowered for marker in markers):
        return True
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_16(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return False
    return len(tail) >= min_len


def x__trailing_has_rationale__mutmut_17(trailing: str, markers: tuple[str, ...], min_len: int) -> bool:
    tail = trailing.strip()
    if not tail:
        return False
    if tail.startswith("#"):
        return _is_rationale_comment(tail, markers, min_len)
    lowered = tail.lower()
    if any(marker in lowered for marker in markers):
        return True
    return len(tail) > min_len

mutants_x__trailing_has_rationale__mutmut['_mutmut_orig'] = x__trailing_has_rationale__mutmut_orig # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_1'] = x__trailing_has_rationale__mutmut_1 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_2'] = x__trailing_has_rationale__mutmut_2 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_3'] = x__trailing_has_rationale__mutmut_3 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_4'] = x__trailing_has_rationale__mutmut_4 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_5'] = x__trailing_has_rationale__mutmut_5 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_6'] = x__trailing_has_rationale__mutmut_6 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_7'] = x__trailing_has_rationale__mutmut_7 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_8'] = x__trailing_has_rationale__mutmut_8 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_9'] = x__trailing_has_rationale__mutmut_9 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_10'] = x__trailing_has_rationale__mutmut_10 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_11'] = x__trailing_has_rationale__mutmut_11 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_12'] = x__trailing_has_rationale__mutmut_12 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_13'] = x__trailing_has_rationale__mutmut_13 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_14'] = x__trailing_has_rationale__mutmut_14 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_15'] = x__trailing_has_rationale__mutmut_15 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_16'] = x__trailing_has_rationale__mutmut_16 # type: ignore # mutmut generated
mutants_x__trailing_has_rationale__mutmut['x__trailing_has_rationale__mutmut_17'] = x__trailing_has_rationale__mutmut_17 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__preceding_line_has_rationale__mutmut)
def _preceding_line_has_rationale(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_orig(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_1(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = None
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_2(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx + 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_3(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 2
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_4(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 or not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_5(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j > 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_6(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 1 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_7(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_8(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j = 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_9(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j += 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_10(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 2
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_11(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j <= 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_12(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 1:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_13(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return True
    return _is_rationale_comment(lines[j].strip(), markers, min_len)


def x__preceding_line_has_rationale__mutmut_14(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(None, markers, min_len)


def x__preceding_line_has_rationale__mutmut_15(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), None, min_len)


def x__preceding_line_has_rationale__mutmut_16(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, None)


def x__preceding_line_has_rationale__mutmut_17(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(markers, min_len)


def x__preceding_line_has_rationale__mutmut_18(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), min_len)


def x__preceding_line_has_rationale__mutmut_19(lines: list[str], idx: int, markers: tuple[str, ...], min_len: int) -> bool:
    j = idx - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return False
    return _is_rationale_comment(lines[j].strip(), markers, )

mutants_x__preceding_line_has_rationale__mutmut['_mutmut_orig'] = x__preceding_line_has_rationale__mutmut_orig # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_1'] = x__preceding_line_has_rationale__mutmut_1 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_2'] = x__preceding_line_has_rationale__mutmut_2 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_3'] = x__preceding_line_has_rationale__mutmut_3 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_4'] = x__preceding_line_has_rationale__mutmut_4 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_5'] = x__preceding_line_has_rationale__mutmut_5 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_6'] = x__preceding_line_has_rationale__mutmut_6 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_7'] = x__preceding_line_has_rationale__mutmut_7 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_8'] = x__preceding_line_has_rationale__mutmut_8 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_9'] = x__preceding_line_has_rationale__mutmut_9 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_10'] = x__preceding_line_has_rationale__mutmut_10 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_11'] = x__preceding_line_has_rationale__mutmut_11 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_12'] = x__preceding_line_has_rationale__mutmut_12 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_13'] = x__preceding_line_has_rationale__mutmut_13 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_14'] = x__preceding_line_has_rationale__mutmut_14 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_15'] = x__preceding_line_has_rationale__mutmut_15 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_16'] = x__preceding_line_has_rationale__mutmut_16 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_17'] = x__preceding_line_has_rationale__mutmut_17 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_18'] = x__preceding_line_has_rationale__mutmut_18 # type: ignore # mutmut generated
mutants_x__preceding_line_has_rationale__mutmut['x__preceding_line_has_rationale__mutmut_19'] = x__preceding_line_has_rationale__mutmut_19 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_is_shell_file__mutmut)
def is_shell_file(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_orig(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_1(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(None):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_2(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith("XX.shXX"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_3(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".SH"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_4(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return False
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_5(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open(None, encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_6(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding=None, errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_7(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors=None) as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_8(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open(encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_9(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_10(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="utf-8", ) as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_11(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("XXrXX", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_12(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("R", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_13(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="XXutf-8XX", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_14(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="UTF-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_15(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="XXignoreXX") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_16(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="IGNORE") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_17(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            first = None
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_18(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return True
    return bool(_SHEBANG_RE.match(first))


def x_is_shell_file__mutmut_19(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(None)


def x_is_shell_file__mutmut_20(path: Path) -> bool:
    """True if ``path`` is a ``.sh`` file or its first line is a shell shebang."""
    if path.name.endswith(".sh"):
        return True
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            first = fh.readline()
    except OSError:
        return False
    return bool(_SHEBANG_RE.match(None))

mutants_x_is_shell_file__mutmut['_mutmut_orig'] = x_is_shell_file__mutmut_orig # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_1'] = x_is_shell_file__mutmut_1 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_2'] = x_is_shell_file__mutmut_2 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_3'] = x_is_shell_file__mutmut_3 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_4'] = x_is_shell_file__mutmut_4 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_5'] = x_is_shell_file__mutmut_5 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_6'] = x_is_shell_file__mutmut_6 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_7'] = x_is_shell_file__mutmut_7 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_8'] = x_is_shell_file__mutmut_8 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_9'] = x_is_shell_file__mutmut_9 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_10'] = x_is_shell_file__mutmut_10 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_11'] = x_is_shell_file__mutmut_11 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_12'] = x_is_shell_file__mutmut_12 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_13'] = x_is_shell_file__mutmut_13 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_14'] = x_is_shell_file__mutmut_14 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_15'] = x_is_shell_file__mutmut_15 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_16'] = x_is_shell_file__mutmut_16 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_17'] = x_is_shell_file__mutmut_17 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_18'] = x_is_shell_file__mutmut_18 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_19'] = x_is_shell_file__mutmut_19 # type: ignore # mutmut generated
mutants_x_is_shell_file__mutmut['x_is_shell_file__mutmut_20'] = x_is_shell_file__mutmut_20 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_has_unjustified_disable__mutmut)
def file_has_unjustified_disable(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_orig(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_1(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = None
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_2(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding=None).splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_3(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="XXutf-8XX").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_4(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="UTF-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_5(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return False
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_6(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(None):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_7(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = None
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_8(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(None)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_9(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len) or not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_10(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None or not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_11(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_12(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_13(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(None, markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_14(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), None, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_15(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, None)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_16(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_17(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_18(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, )
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_19(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group(None), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_20(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("XXtrailingXX"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_21(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("TRAILING"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_22(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_23(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(None, idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_24(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, None, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_25(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, None, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_26(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, None)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_27(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(idx, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_28(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, markers, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_29(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, min_len)
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_30(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, )
        ):
            return True
    return False


def x_file_has_unjustified_disable__mutmut_31(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return False
    return False


def x_file_has_unjustified_disable__mutmut_32(
    path: Path,
    *,
    markers: tuple[str, ...],
    min_len: int,
) -> bool:
    """True iff ``path`` has a shellcheck-disable lacking a same/preceding-line reason.

    Pure helper (the detection core) so tests assert on it directly. A read
    error is a violation because the configured source could not be evaluated.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return True
    for idx, line in enumerate(lines):
        m = _DISABLE_RE.search(line)
        if (
            m is not None
            and not _trailing_has_rationale(m.group("trailing"), markers, min_len)
            and not _preceding_line_has_rationale(lines, idx, markers, min_len)
        ):
            return True
    return True

mutants_x_file_has_unjustified_disable__mutmut['_mutmut_orig'] = x_file_has_unjustified_disable__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_1'] = x_file_has_unjustified_disable__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_2'] = x_file_has_unjustified_disable__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_3'] = x_file_has_unjustified_disable__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_4'] = x_file_has_unjustified_disable__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_5'] = x_file_has_unjustified_disable__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_6'] = x_file_has_unjustified_disable__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_7'] = x_file_has_unjustified_disable__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_8'] = x_file_has_unjustified_disable__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_9'] = x_file_has_unjustified_disable__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_10'] = x_file_has_unjustified_disable__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_11'] = x_file_has_unjustified_disable__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_12'] = x_file_has_unjustified_disable__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_13'] = x_file_has_unjustified_disable__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_14'] = x_file_has_unjustified_disable__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_15'] = x_file_has_unjustified_disable__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_16'] = x_file_has_unjustified_disable__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_17'] = x_file_has_unjustified_disable__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_18'] = x_file_has_unjustified_disable__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_19'] = x_file_has_unjustified_disable__mutmut_19 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_20'] = x_file_has_unjustified_disable__mutmut_20 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_21'] = x_file_has_unjustified_disable__mutmut_21 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_22'] = x_file_has_unjustified_disable__mutmut_22 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_23'] = x_file_has_unjustified_disable__mutmut_23 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_24'] = x_file_has_unjustified_disable__mutmut_24 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_25'] = x_file_has_unjustified_disable__mutmut_25 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_26'] = x_file_has_unjustified_disable__mutmut_26 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_27'] = x_file_has_unjustified_disable__mutmut_27 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_28'] = x_file_has_unjustified_disable__mutmut_28 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_29'] = x_file_has_unjustified_disable__mutmut_29 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_30'] = x_file_has_unjustified_disable__mutmut_30 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_31'] = x_file_has_unjustified_disable__mutmut_31 # type: ignore # mutmut generated
mutants_x_file_has_unjustified_disable__mutmut['x_file_has_unjustified_disable__mutmut_32'] = x_file_has_unjustified_disable__mutmut_32 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut: MutantDict = {}  # type: ignore
mutants_xǁShellcheckDisableWithReasonǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class ShellcheckDisableWithReason(FitnessRule):
    """Flags a shell file holding a rationale-free ``# shellcheck disable=`` directive."""

    name = "shellcheck-disable-with-reason"
    remediation = REMEDIATION
    # Shell scope is shebang-aware, so enumeration/scope are overridden below;
    # ``.sh`` is the cheap extension prefilter.
    extensions = (".sh",)

    #: Rule-specific knobs — overridable per consumer.
    rationale_markers: tuple[str, ...] = DEFAULT_RATIONALE_MARKERS
    min_rationale_len: int = DEFAULT_MIN_RATIONALE_LEN

    @classmethod
    @_mutmut_mutated(mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = None
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, )
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = None
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get(None)
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("XXrationale_markersXX")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("RATIONALE_MARKERS")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = None
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(None) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = None
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(None)
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get(None, DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", None))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get(DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("min_rationale_len", ))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("XXmin_rationale_lenXX", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @classmethod
    def xǁShellcheckDisableWithReasonǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ShellcheckDisableWithReason:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ShellcheckDisableWithReason)  # noqa: S101  # narrowing for mypy
        markers = config.get("rationale_markers")
        rule.rationale_markers = tuple(markers) if markers is not None else DEFAULT_RATIONALE_MARKERS
        rule.min_rationale_len = int(config.get("MIN_RATIONALE_LEN", DEFAULT_MIN_RATIONALE_LEN))
        return rule

    @_mutmut_mutated(mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut)
    def enumerate_files(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_orig(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_1(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = None
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_2(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = None
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_3(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root * root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_4(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_5(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(None)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_6(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                break
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_7(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob(None):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_8(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("XX*XX"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_9(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() and "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_10(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_11(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "XX__pycache__XX" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_12(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__PYCACHE__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_13(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" not in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_14(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    break
                if is_shell_file(path):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_15(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(None):
                    out.append(path)
        return out

    def xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_16(self) -> list[Path]:
        """Walk configured roots, returning shell files (``.sh`` or shebang)."""
        out: list[Path] = []
        for root in self._roots:
            root_path = self._repo_root / root
            if not root_path.is_dir():
                out.append(root_path)
                continue
            for path in root_path.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if is_shell_file(path):
                    out.append(None)
        return out

    @_mutmut_mutated(mutants_xǁShellcheckDisableWithReasonǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        """Scope is whatever enumeration returns; exempt-file filtering applies upstream."""
        return True

    def xǁShellcheckDisableWithReasonǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        """Scope is whatever enumeration returns; exempt-file filtering applies upstream."""
        return True

    def xǁShellcheckDisableWithReasonǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        """Scope is whatever enumeration returns; exempt-file filtering applies upstream."""
        return False

    @_mutmut_mutated(mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} and not path.is_dir():
            return True
        return file_has_unjustified_disable(
            path,
            markers=self.rationale_markers,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} and not path.is_dir():
            return True
        return file_has_unjustified_disable(
            path,
            markers=self.rationale_markers,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} or not path.is_dir():
            return True
        return file_has_unjustified_disable(
            path,
            markers=self.rationale_markers,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        if path not in {self._repo_root / root for root in self._roots} and not path.is_dir():
            return True
        return file_has_unjustified_disable(
            path,
            markers=self.rationale_markers,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        if path in {self._repo_root * root for root in self._roots} and not path.is_dir():
            return True
        return file_has_unjustified_disable(
            path,
            markers=self.rationale_markers,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} and path.is_dir():
            return True
        return file_has_unjustified_disable(
            path,
            markers=self.rationale_markers,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} and not path.is_dir():
            return False
        return file_has_unjustified_disable(
            path,
            markers=self.rationale_markers,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} and not path.is_dir():
            return True
        return file_has_unjustified_disable(
            None,
            markers=self.rationale_markers,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} and not path.is_dir():
            return True
        return file_has_unjustified_disable(
            path,
            markers=None,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_8(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} and not path.is_dir():
            return True
        return file_has_unjustified_disable(
            path,
            markers=self.rationale_markers,
            min_len=None,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_9(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} and not path.is_dir():
            return True
        return file_has_unjustified_disable(
            markers=self.rationale_markers,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_10(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} and not path.is_dir():
            return True
        return file_has_unjustified_disable(
            path,
            min_len=self.min_rationale_len,
        )

    def xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_11(self, path: Path) -> bool:
        if path in {self._repo_root / root for root in self._roots} and not path.is_dir():
            return True
        return file_has_unjustified_disable(
            path,
            markers=self.rationale_markers,
            )

mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['_mutmut_orig'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_1'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_2'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_3'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_4'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_5'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_6'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_7'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_8'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_9'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_10'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_11'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_12'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_13'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_14'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_15'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_16'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_17'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_18'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_19'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfrom_config__mutmut['xǁShellcheckDisableWithReasonǁfrom_config__mutmut_20'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfrom_config__mutmut_20 # type: ignore # mutmut generated

mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['_mutmut_orig'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_orig # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_1'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_1 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_2'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_2 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_3'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_3 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_4'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_4 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_5'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_5 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_6'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_6 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_7'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_7 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_8'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_8 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_9'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_9 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_10'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_10 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_11'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_11 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_12'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_12 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_13'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_13 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_14'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_14 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_15'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_15 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁenumerate_files__mutmut['xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_16'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁenumerate_files__mutmut_16 # type: ignore # mutmut generated

mutants_xǁShellcheckDisableWithReasonǁis_in_scope__mutmut['_mutmut_orig'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁis_in_scope__mutmut['xǁShellcheckDisableWithReasonǁis_in_scope__mutmut_1'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁis_in_scope__mutmut_1 # type: ignore # mutmut generated

mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['_mutmut_orig'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_1'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_2'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_3'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_4'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_5'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_6'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_7'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_8'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_8 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_9'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_9 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_10'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_10 # type: ignore # mutmut generated
mutants_xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut['xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_11'] = ShellcheckDisableWithReason.xǁShellcheckDisableWithReasonǁfile_has_violation__mutmut_11 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ShellcheckDisableWithReason:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ShellcheckDisableWithReason.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ShellcheckDisableWithReason:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ShellcheckDisableWithReason.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ShellcheckDisableWithReason:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ShellcheckDisableWithReason.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ShellcheckDisableWithReason:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ShellcheckDisableWithReason.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ShellcheckDisableWithReason:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ShellcheckDisableWithReason.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ShellcheckDisableWithReason:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ShellcheckDisableWithReason.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ShellcheckDisableWithReason, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ShellcheckDisableWithReason, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ShellcheckDisableWithReason, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ShellcheckDisableWithReason, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
