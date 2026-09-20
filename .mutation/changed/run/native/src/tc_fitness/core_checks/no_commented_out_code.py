"""CORE check: no_commented_out_code — Sonar S125.

A run of consecutive ``#``-prefixed lines that lex as valid Python statements
is commented-out code. Git history is the archive — dead code in a comment
accumulates confusion (is it still relevant? the intended replacement for the
line below?). The fix is always to delete it; ``git log -p`` recovers any
prior state.

Ported from kairix ``scripts/checks/check_no_commented_out_code.py`` (F18) and
re-expressed as a configurable, repo-agnostic rule: the only domain-intrinsic
number is S125's own minimum-run length (3 contiguous comment lines), exposed
as a ``min_run`` knob the consumer overrides via ``[tool.tc_fitness]``. No repo
paths or globs are baked in.
"""

from __future__ import annotations

import ast
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: S125's own minimum run — domain-intrinsic, not repo identity. Overridable.
DEFAULT_MIN_RUN = 3

# Directive comments (shebangs, encoding cookies, tool directives) are never code.
_DIRECTIVE_RE = re.compile(r"^\s*#\s*(!|pyright:|type:\s*ignore|noqa|nosec|pragma:|coding[:=])")
# Section-rule boilerplate (``# -----`` / ``# =====`` / box-drawing rules) is never code.
_BOILERPLATE_RE = re.compile(r"^\s*#\s*[=─—―-]{3,}")

# Syntactic anchors: a comment block lacking all of these is prose, not code.
_CODE_ANCHORS = (
    "=",
    "(",
    "import ",
    "def ",
    "class ",
    "return",
    "raise",
    "if ",
    "for ",
    "while ",
    "with ",
)

REMEDIATION = _remediation(
    fix=(
        "delete the run of consecutive commented-out Python lines outright; "
        "if the code might come back, leave a referenced TODO with a ticket "
        "number instead of the dead code itself (git history is the archive)."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.no_commented_out_code",
    passing="# Strip leading slash so we can join cleanly.\\npath = path.lstrip('/')",
    forbidden="# old = path.replace('/a/','/b/')\\n# if old.startswith('/x'):\\n#     old = old[6:]",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__strip_comment_prefix__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__strip_comment_prefix__mutmut)
def _strip_comment_prefix(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = len(line) - len(line.lstrip())
    rest = line[leading_ws + 1 :]
    if rest.startswith(" "):
        rest = rest[1:]
    return rest


def x__strip_comment_prefix__mutmut_orig(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = len(line) - len(line.lstrip())
    rest = line[leading_ws + 1 :]
    if rest.startswith(" "):
        rest = rest[1:]
    return rest


def x__strip_comment_prefix__mutmut_1(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = None
    rest = line[leading_ws + 1 :]
    if rest.startswith(" "):
        rest = rest[1:]
    return rest


def x__strip_comment_prefix__mutmut_2(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = len(line) + len(line.lstrip())
    rest = line[leading_ws + 1 :]
    if rest.startswith(" "):
        rest = rest[1:]
    return rest


def x__strip_comment_prefix__mutmut_3(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = len(line) - len(line.lstrip())
    rest = None
    if rest.startswith(" "):
        rest = rest[1:]
    return rest


def x__strip_comment_prefix__mutmut_4(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = len(line) - len(line.lstrip())
    rest = line[leading_ws - 1 :]
    if rest.startswith(" "):
        rest = rest[1:]
    return rest


def x__strip_comment_prefix__mutmut_5(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = len(line) - len(line.lstrip())
    rest = line[leading_ws + 2 :]
    if rest.startswith(" "):
        rest = rest[1:]
    return rest


def x__strip_comment_prefix__mutmut_6(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = len(line) - len(line.lstrip())
    rest = line[leading_ws + 1 :]
    if rest.startswith(None):
        rest = rest[1:]
    return rest


def x__strip_comment_prefix__mutmut_7(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = len(line) - len(line.lstrip())
    rest = line[leading_ws + 1 :]
    if rest.startswith("XX XX"):
        rest = rest[1:]
    return rest


def x__strip_comment_prefix__mutmut_8(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = len(line) - len(line.lstrip())
    rest = line[leading_ws + 1 :]
    if rest.startswith(" "):
        rest = None
    return rest


def x__strip_comment_prefix__mutmut_9(line: str) -> str:
    """Strip leading whitespace + ``#`` + one optional space, preserving the rest."""
    leading_ws = len(line) - len(line.lstrip())
    rest = line[leading_ws + 1 :]
    if rest.startswith(" "):
        rest = rest[2:]
    return rest

mutants_x__strip_comment_prefix__mutmut['_mutmut_orig'] = x__strip_comment_prefix__mutmut_orig # type: ignore # mutmut generated
mutants_x__strip_comment_prefix__mutmut['x__strip_comment_prefix__mutmut_1'] = x__strip_comment_prefix__mutmut_1 # type: ignore # mutmut generated
mutants_x__strip_comment_prefix__mutmut['x__strip_comment_prefix__mutmut_2'] = x__strip_comment_prefix__mutmut_2 # type: ignore # mutmut generated
mutants_x__strip_comment_prefix__mutmut['x__strip_comment_prefix__mutmut_3'] = x__strip_comment_prefix__mutmut_3 # type: ignore # mutmut generated
mutants_x__strip_comment_prefix__mutmut['x__strip_comment_prefix__mutmut_4'] = x__strip_comment_prefix__mutmut_4 # type: ignore # mutmut generated
mutants_x__strip_comment_prefix__mutmut['x__strip_comment_prefix__mutmut_5'] = x__strip_comment_prefix__mutmut_5 # type: ignore # mutmut generated
mutants_x__strip_comment_prefix__mutmut['x__strip_comment_prefix__mutmut_6'] = x__strip_comment_prefix__mutmut_6 # type: ignore # mutmut generated
mutants_x__strip_comment_prefix__mutmut['x__strip_comment_prefix__mutmut_7'] = x__strip_comment_prefix__mutmut_7 # type: ignore # mutmut generated
mutants_x__strip_comment_prefix__mutmut['x__strip_comment_prefix__mutmut_8'] = x__strip_comment_prefix__mutmut_8 # type: ignore # mutmut generated
mutants_x__strip_comment_prefix__mutmut['x__strip_comment_prefix__mutmut_9'] = x__strip_comment_prefix__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_commentlike_directive__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_commentlike_directive__mutmut)
def _is_commentlike_directive(line: str) -> bool:
    return bool(_DIRECTIVE_RE.match(line) or _BOILERPLATE_RE.match(line))


def x__is_commentlike_directive__mutmut_orig(line: str) -> bool:
    return bool(_DIRECTIVE_RE.match(line) or _BOILERPLATE_RE.match(line))


def x__is_commentlike_directive__mutmut_1(line: str) -> bool:
    return bool(None)


def x__is_commentlike_directive__mutmut_2(line: str) -> bool:
    return bool(_DIRECTIVE_RE.match(line) and _BOILERPLATE_RE.match(line))


def x__is_commentlike_directive__mutmut_3(line: str) -> bool:
    return bool(_DIRECTIVE_RE.match(None) or _BOILERPLATE_RE.match(line))


def x__is_commentlike_directive__mutmut_4(line: str) -> bool:
    return bool(_DIRECTIVE_RE.match(line) or _BOILERPLATE_RE.match(None))

mutants_x__is_commentlike_directive__mutmut['_mutmut_orig'] = x__is_commentlike_directive__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_commentlike_directive__mutmut['x__is_commentlike_directive__mutmut_1'] = x__is_commentlike_directive__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_commentlike_directive__mutmut['x__is_commentlike_directive__mutmut_2'] = x__is_commentlike_directive__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_commentlike_directive__mutmut['x__is_commentlike_directive__mutmut_3'] = x__is_commentlike_directive__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_commentlike_directive__mutmut['x__is_commentlike_directive__mutmut_4'] = x__is_commentlike_directive__mutmut_4 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__looks_like_code__mutmut)
def _looks_like_code(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_orig(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_1(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = None
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_2(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip(None)
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_3(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("XX\nXX")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_4(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_5(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return True
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_6(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_7(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(None):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_8(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker not in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_9(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return True
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_10(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = None
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_11(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = None
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_12(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = None
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_13(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(None)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_14(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) + len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_15(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = None
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_16(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(None)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_17(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "XX\nXX".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_18(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "XXXX" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_19(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(None)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_20(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return False
    except (SyntaxError, ValueError, IndentationError):
        return False


def x__looks_like_code__mutmut_21(block_text: str) -> bool:
    """True if the dedented comment block parses as one or more Python statements."""
    stripped = block_text.strip("\n")
    if not stripped:
        return False
    if not any(marker in stripped for marker in _CODE_ANCHORS):
        return False
    try:
        lines = stripped.splitlines()
        non_empty = [line for line in lines if line.strip()]
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        dedented = "\n".join(line[min_indent:] if line.strip() else "" for line in lines)
        ast.parse(dedented)
        return True
    except (SyntaxError, ValueError, IndentationError):
        return True

mutants_x__looks_like_code__mutmut['_mutmut_orig'] = x__looks_like_code__mutmut_orig # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_1'] = x__looks_like_code__mutmut_1 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_2'] = x__looks_like_code__mutmut_2 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_3'] = x__looks_like_code__mutmut_3 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_4'] = x__looks_like_code__mutmut_4 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_5'] = x__looks_like_code__mutmut_5 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_6'] = x__looks_like_code__mutmut_6 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_7'] = x__looks_like_code__mutmut_7 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_8'] = x__looks_like_code__mutmut_8 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_9'] = x__looks_like_code__mutmut_9 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_10'] = x__looks_like_code__mutmut_10 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_11'] = x__looks_like_code__mutmut_11 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_12'] = x__looks_like_code__mutmut_12 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_13'] = x__looks_like_code__mutmut_13 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_14'] = x__looks_like_code__mutmut_14 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_15'] = x__looks_like_code__mutmut_15 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_16'] = x__looks_like_code__mutmut_16 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_17'] = x__looks_like_code__mutmut_17 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_18'] = x__looks_like_code__mutmut_18 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_19'] = x__looks_like_code__mutmut_19 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_20'] = x__looks_like_code__mutmut_20 # type: ignore # mutmut generated
mutants_x__looks_like_code__mutmut['x__looks_like_code__mutmut_21'] = x__looks_like_code__mutmut_21 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__docstring_lines__mutmut)
def _docstring_lines(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_orig(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_1(tree: ast.AST) -> set[int]:
    out: set[int] = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_2(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(None):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_3(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) or node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_4(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = None
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_5(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[1]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_6(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant) or isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_7(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr) or isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_8(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = None
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_9(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = None
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_10(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno and first.lineno
                out.update(range(start, end + 1))
    return out


def x__docstring_lines__mutmut_11(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(None)
    return out


def x__docstring_lines__mutmut_12(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(None, end + 1))
    return out


def x__docstring_lines__mutmut_13(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, None))
    return out


def x__docstring_lines__mutmut_14(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(end + 1))
    return out


def x__docstring_lines__mutmut_15(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, ))
    return out


def x__docstring_lines__mutmut_16(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end - 1))
    return out


def x__docstring_lines__mutmut_17(tree: ast.AST) -> set[int]:
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                start = first.lineno
                end = first.end_lineno or first.lineno
                out.update(range(start, end + 2))
    return out

mutants_x__docstring_lines__mutmut['_mutmut_orig'] = x__docstring_lines__mutmut_orig # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_1'] = x__docstring_lines__mutmut_1 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_2'] = x__docstring_lines__mutmut_2 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_3'] = x__docstring_lines__mutmut_3 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_4'] = x__docstring_lines__mutmut_4 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_5'] = x__docstring_lines__mutmut_5 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_6'] = x__docstring_lines__mutmut_6 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_7'] = x__docstring_lines__mutmut_7 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_8'] = x__docstring_lines__mutmut_8 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_9'] = x__docstring_lines__mutmut_9 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_10'] = x__docstring_lines__mutmut_10 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_11'] = x__docstring_lines__mutmut_11 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_12'] = x__docstring_lines__mutmut_12 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_13'] = x__docstring_lines__mutmut_13 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_14'] = x__docstring_lines__mutmut_14 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_15'] = x__docstring_lines__mutmut_15 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_16'] = x__docstring_lines__mutmut_16 # type: ignore # mutmut generated
mutants_x__docstring_lines__mutmut['x__docstring_lines__mutmut_17'] = x__docstring_lines__mutmut_17 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_module_has_commented_code__mutmut)
def module_has_commented_code(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_orig(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_1(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = None
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_2(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding=None)
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_3(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="XXutf-8XX")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_4(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="UTF-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_5(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_6(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_7(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_8(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_9(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_10(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_11(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_12(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_13(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(None)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_14(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_15(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = None
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_16(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 1
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_17(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i <= len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_18(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = None
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_19(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i - 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_20(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 2 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_21(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 not in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_22(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i = 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_23(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i -= 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_24(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 2
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_25(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            break
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_26(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = None
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_27(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") and _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_28(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_29(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith(None) or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_30(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("XX#XX") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_31(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(None):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_32(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i = 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_33(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i -= 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_34(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 2
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_35(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            break
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_36(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = None
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_37(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = None
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_38(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j <= len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_39(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = None
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_40(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") and _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_41(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_42(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith(None) or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_43(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("XX#XX") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_44(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(None):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_45(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                return
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_46(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j - 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_47(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 3 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_48(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 not in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_49(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                return
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_50(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(None)
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_51(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(None))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_52(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j = 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_53(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j -= 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_54(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 2
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_55(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run or _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_56(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) > min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_57(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code(None):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_58(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(None)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_59(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("XX\nXX".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_60(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return False
        i = j + 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_61(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = None
    return False


def x_module_has_commented_code__mutmut_62(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j - 1 if j == i else j
    return False


def x_module_has_commented_code__mutmut_63(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 2 if j == i else j
    return False


def x_module_has_commented_code__mutmut_64(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j != i else j
    return False


def x_module_has_commented_code__mutmut_65(path: Path, *, min_run: int) -> bool:
    """True iff ``path`` has a run of ``min_run``+ comment lines that lex as code.

    Pure helper (the detection core). Docstrings and directive/boilerplate
    comments are skipped. A syntax / decode error is treated as "no violation".
    """
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    docstring_lines = _docstring_lines(tree)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if i + 1 in docstring_lines:
            i += 1
            continue
        stripped = line.strip()
        if not stripped.startswith("#") or _is_commentlike_directive(line):
            i += 1
            continue
        block_lines: list[str] = []
        j = i
        while j < len(lines):
            cur = lines[j]
            if not cur.strip().startswith("#") or _is_commentlike_directive(cur):
                break
            if j + 2 in docstring_lines:
                break
            block_lines.append(_strip_comment_prefix(cur))
            j += 1
        if len(block_lines) >= min_run and _looks_like_code("\n".join(block_lines)):
            return True
        i = j + 1 if j == i else j
    return True

mutants_x_module_has_commented_code__mutmut['_mutmut_orig'] = x_module_has_commented_code__mutmut_orig # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_1'] = x_module_has_commented_code__mutmut_1 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_2'] = x_module_has_commented_code__mutmut_2 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_3'] = x_module_has_commented_code__mutmut_3 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_4'] = x_module_has_commented_code__mutmut_4 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_5'] = x_module_has_commented_code__mutmut_5 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_6'] = x_module_has_commented_code__mutmut_6 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_7'] = x_module_has_commented_code__mutmut_7 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_8'] = x_module_has_commented_code__mutmut_8 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_9'] = x_module_has_commented_code__mutmut_9 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_10'] = x_module_has_commented_code__mutmut_10 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_11'] = x_module_has_commented_code__mutmut_11 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_12'] = x_module_has_commented_code__mutmut_12 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_13'] = x_module_has_commented_code__mutmut_13 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_14'] = x_module_has_commented_code__mutmut_14 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_15'] = x_module_has_commented_code__mutmut_15 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_16'] = x_module_has_commented_code__mutmut_16 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_17'] = x_module_has_commented_code__mutmut_17 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_18'] = x_module_has_commented_code__mutmut_18 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_19'] = x_module_has_commented_code__mutmut_19 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_20'] = x_module_has_commented_code__mutmut_20 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_21'] = x_module_has_commented_code__mutmut_21 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_22'] = x_module_has_commented_code__mutmut_22 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_23'] = x_module_has_commented_code__mutmut_23 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_24'] = x_module_has_commented_code__mutmut_24 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_25'] = x_module_has_commented_code__mutmut_25 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_26'] = x_module_has_commented_code__mutmut_26 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_27'] = x_module_has_commented_code__mutmut_27 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_28'] = x_module_has_commented_code__mutmut_28 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_29'] = x_module_has_commented_code__mutmut_29 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_30'] = x_module_has_commented_code__mutmut_30 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_31'] = x_module_has_commented_code__mutmut_31 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_32'] = x_module_has_commented_code__mutmut_32 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_33'] = x_module_has_commented_code__mutmut_33 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_34'] = x_module_has_commented_code__mutmut_34 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_35'] = x_module_has_commented_code__mutmut_35 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_36'] = x_module_has_commented_code__mutmut_36 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_37'] = x_module_has_commented_code__mutmut_37 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_38'] = x_module_has_commented_code__mutmut_38 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_39'] = x_module_has_commented_code__mutmut_39 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_40'] = x_module_has_commented_code__mutmut_40 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_41'] = x_module_has_commented_code__mutmut_41 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_42'] = x_module_has_commented_code__mutmut_42 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_43'] = x_module_has_commented_code__mutmut_43 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_44'] = x_module_has_commented_code__mutmut_44 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_45'] = x_module_has_commented_code__mutmut_45 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_46'] = x_module_has_commented_code__mutmut_46 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_47'] = x_module_has_commented_code__mutmut_47 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_48'] = x_module_has_commented_code__mutmut_48 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_49'] = x_module_has_commented_code__mutmut_49 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_50'] = x_module_has_commented_code__mutmut_50 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_51'] = x_module_has_commented_code__mutmut_51 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_52'] = x_module_has_commented_code__mutmut_52 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_53'] = x_module_has_commented_code__mutmut_53 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_54'] = x_module_has_commented_code__mutmut_54 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_55'] = x_module_has_commented_code__mutmut_55 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_56'] = x_module_has_commented_code__mutmut_56 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_57'] = x_module_has_commented_code__mutmut_57 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_58'] = x_module_has_commented_code__mutmut_58 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_59'] = x_module_has_commented_code__mutmut_59 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_60'] = x_module_has_commented_code__mutmut_60 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_61'] = x_module_has_commented_code__mutmut_61 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_62'] = x_module_has_commented_code__mutmut_62 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_63'] = x_module_has_commented_code__mutmut_63 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_64'] = x_module_has_commented_code__mutmut_64 # type: ignore # mutmut generated
mutants_x_module_has_commented_code__mutmut['x_module_has_commented_code__mutmut_65'] = x_module_has_commented_code__mutmut_65 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoCommentedOutCodeǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoCommentedOutCode(FitnessRule):
    """Flags files holding a run of commented-out Python code (Sonar S125)."""

    name = "no-commented-out-code"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knob — S125's own minimum run; overridable per consumer.
    min_run: int = DEFAULT_MIN_RUN

    @classmethod
    @_mutmut_mutated(mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("min_run", DEFAULT_MIN_RUN))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("min_run", DEFAULT_MIN_RUN))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = None
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("min_run", DEFAULT_MIN_RUN))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("min_run", DEFAULT_MIN_RUN))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("min_run", DEFAULT_MIN_RUN))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("min_run", DEFAULT_MIN_RUN))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, )
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("min_run", DEFAULT_MIN_RUN))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = None
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(None)
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get(None, DEFAULT_MIN_RUN))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("min_run", None))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get(DEFAULT_MIN_RUN))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("min_run", ))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("XXmin_runXX", DEFAULT_MIN_RUN))
        return rule

    @classmethod
    def xǁNoCommentedOutCodeǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoCommentedOutCode:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoCommentedOutCode)  # noqa: S101  # narrowing for mypy
        rule.min_run = int(config.get("MIN_RUN", DEFAULT_MIN_RUN))
        return rule

    @_mutmut_mutated(mutants_xǁNoCommentedOutCodeǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return module_has_commented_code(path, min_run=self.min_run)

    def xǁNoCommentedOutCodeǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return module_has_commented_code(path, min_run=self.min_run)

    def xǁNoCommentedOutCodeǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return module_has_commented_code(None, min_run=self.min_run)

    def xǁNoCommentedOutCodeǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return module_has_commented_code(path, min_run=None)

    def xǁNoCommentedOutCodeǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return module_has_commented_code(min_run=self.min_run)

    def xǁNoCommentedOutCodeǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return module_has_commented_code(path, )

mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['_mutmut_orig'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_1'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_2'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_3'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_4'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_5'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_6'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_7'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_8'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_9'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_10'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_11'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_12'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfrom_config__mutmut['xǁNoCommentedOutCodeǁfrom_config__mutmut_13'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfrom_config__mutmut_13 # type: ignore # mutmut generated

mutants_xǁNoCommentedOutCodeǁfile_has_violation__mutmut['_mutmut_orig'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfile_has_violation__mutmut['xǁNoCommentedOutCodeǁfile_has_violation__mutmut_1'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfile_has_violation__mutmut['xǁNoCommentedOutCodeǁfile_has_violation__mutmut_2'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfile_has_violation__mutmut['xǁNoCommentedOutCodeǁfile_has_violation__mutmut_3'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoCommentedOutCodeǁfile_has_violation__mutmut['xǁNoCommentedOutCodeǁfile_has_violation__mutmut_4'] = NoCommentedOutCode.xǁNoCommentedOutCodeǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoCommentedOutCode:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoCommentedOutCode.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoCommentedOutCode:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoCommentedOutCode.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoCommentedOutCode:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoCommentedOutCode.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoCommentedOutCode:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoCommentedOutCode.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoCommentedOutCode:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoCommentedOutCode.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoCommentedOutCode:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoCommentedOutCode.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoCommentedOutCode, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoCommentedOutCode, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoCommentedOutCode, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoCommentedOutCode, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
