"""CORE check: actionable_feedback — every emitted check error is agent-actionable.

A fitness check whose failure message says only "validation failed" leaves the
next agent nowhere to go. Every error a check appends to its failure list MUST
carry an action marker (``fix:`` / ``next:`` / ``run:``) so the reader knows the
corrective action, the follow-up, and the exact re-verify command.

Detection is AST-based: it walks each in-scope module for ``<errors>.append(...)``
/ ``<errors>.extend(...)`` calls (any variable whose name contains ``error``) and
flags a literal string argument — including a flat f-string's literal parts —
that contains none of the action markers.

Ported from tc-agent-zone ``scripts/checks/actionable_feedback.py`` and
re-expressed as a configurable, repo-agnostic rule: the scan roots, in-scope
extensions, exempt files and the action markers themselves all arrive from the
consumer's ``[tool.tc_fitness]`` config. The donor hardcoded ``scripts/checks``
and three exempt dispatcher filenames; this module bakes in NONE.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The action markers an agent-actionable error message carries. Domain-
#: intrinsic (the fix/next/run affordance shape), overridable via config.
DEFAULT_ACTION_MARKERS: tuple[str, ...] = ("fix:", "next:", "run:")

REMEDIATION = _remediation(
    fix=(
        "include an agent-actionable correction in the emitted error — at "
        "least one of fix: / next: / run: naming the corrective action, the "
        "follow-up, and the exact command to re-verify."
    ),
    nxt="re-run this check to confirm the message now carries a marker.",
    run="python -m tc_fitness.core_checks.actionable_feedback",
    passing='errors.append(f"{rel}: bad; fix: rename it; next: rerun the gate")',
    forbidden='errors.append(f"{rel}: validation failed")',
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__literal_text__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__literal_text__mutmut)
def _literal_text(node: ast.AST) -> str | None:
    """The literal string an arg node carries (Constant or flat f-string), else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = [v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str)]
        return "".join(parts)
    return None


def x__literal_text__mutmut_orig(node: ast.AST) -> str | None:
    """The literal string an arg node carries (Constant or flat f-string), else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = [v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str)]
        return "".join(parts)
    return None


def x__literal_text__mutmut_1(node: ast.AST) -> str | None:
    """The literal string an arg node carries (Constant or flat f-string), else None."""
    if isinstance(node, ast.Constant) or isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = [v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str)]
        return "".join(parts)
    return None


def x__literal_text__mutmut_2(node: ast.AST) -> str | None:
    """The literal string an arg node carries (Constant or flat f-string), else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = None
        return "".join(parts)
    return None


def x__literal_text__mutmut_3(node: ast.AST) -> str | None:
    """The literal string an arg node carries (Constant or flat f-string), else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = [v.value for v in node.values if isinstance(v, ast.Constant) or isinstance(v.value, str)]
        return "".join(parts)
    return None


def x__literal_text__mutmut_4(node: ast.AST) -> str | None:
    """The literal string an arg node carries (Constant or flat f-string), else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = [v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str)]
        return "".join(None)
    return None


def x__literal_text__mutmut_5(node: ast.AST) -> str | None:
    """The literal string an arg node carries (Constant or flat f-string), else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = [v.value for v in node.values if isinstance(v, ast.Constant) and isinstance(v.value, str)]
        return "XXXX".join(parts)
    return None

mutants_x__literal_text__mutmut['_mutmut_orig'] = x__literal_text__mutmut_orig # type: ignore # mutmut generated
mutants_x__literal_text__mutmut['x__literal_text__mutmut_1'] = x__literal_text__mutmut_1 # type: ignore # mutmut generated
mutants_x__literal_text__mutmut['x__literal_text__mutmut_2'] = x__literal_text__mutmut_2 # type: ignore # mutmut generated
mutants_x__literal_text__mutmut['x__literal_text__mutmut_3'] = x__literal_text__mutmut_3 # type: ignore # mutmut generated
mutants_x__literal_text__mutmut['x__literal_text__mutmut_4'] = x__literal_text__mutmut_4 # type: ignore # mutmut generated
mutants_x__literal_text__mutmut['x__literal_text__mutmut_5'] = x__literal_text__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_error_append_call__mutmut)
def _is_error_append_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_orig(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_1(node: ast.AST) -> bool:
    if isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_2(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return True
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_3(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = None
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_4(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name) or "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_5(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"} or isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_6(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute) or func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_7(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr not in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_8(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"XXappendXX", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_9(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"APPEND", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_10(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "XXextendXX"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_11(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "EXTEND"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_12(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "XXerrorXX" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_13(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "ERROR" in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_14(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" not in func.value.id.lower()
    )


def x__is_error_append_call__mutmut_15(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr in {"append", "extend"}
        and isinstance(func.value, ast.Name)
        and "error" in func.value.id.upper()
    )

mutants_x__is_error_append_call__mutmut['_mutmut_orig'] = x__is_error_append_call__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_1'] = x__is_error_append_call__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_2'] = x__is_error_append_call__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_3'] = x__is_error_append_call__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_4'] = x__is_error_append_call__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_5'] = x__is_error_append_call__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_6'] = x__is_error_append_call__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_7'] = x__is_error_append_call__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_8'] = x__is_error_append_call__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_9'] = x__is_error_append_call__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_10'] = x__is_error_append_call__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_11'] = x__is_error_append_call__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_12'] = x__is_error_append_call__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_13'] = x__is_error_append_call__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_14'] = x__is_error_append_call__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_error_append_call__mutmut['x__is_error_append_call__mutmut_15'] = x__is_error_append_call__mutmut_15 # type: ignore # mutmut generated
mutants_x__literal_arg_texts__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__literal_arg_texts__mutmut)
def _literal_arg_texts(arg: ast.AST) -> list[str]:
    text = _literal_text(arg)
    if text is not None:
        return [text]
    if isinstance(arg, ast.List | ast.Tuple):
        return [t for item in arg.elts if (t := _literal_text(item)) is not None]
    return []


def x__literal_arg_texts__mutmut_orig(arg: ast.AST) -> list[str]:
    text = _literal_text(arg)
    if text is not None:
        return [text]
    if isinstance(arg, ast.List | ast.Tuple):
        return [t for item in arg.elts if (t := _literal_text(item)) is not None]
    return []


def x__literal_arg_texts__mutmut_1(arg: ast.AST) -> list[str]:
    text = None
    if text is not None:
        return [text]
    if isinstance(arg, ast.List | ast.Tuple):
        return [t for item in arg.elts if (t := _literal_text(item)) is not None]
    return []


def x__literal_arg_texts__mutmut_2(arg: ast.AST) -> list[str]:
    text = _literal_text(None)
    if text is not None:
        return [text]
    if isinstance(arg, ast.List | ast.Tuple):
        return [t for item in arg.elts if (t := _literal_text(item)) is not None]
    return []


def x__literal_arg_texts__mutmut_3(arg: ast.AST) -> list[str]:
    text = _literal_text(arg)
    if text is None:
        return [text]
    if isinstance(arg, ast.List | ast.Tuple):
        return [t for item in arg.elts if (t := _literal_text(item)) is not None]
    return []


def x__literal_arg_texts__mutmut_4(arg: ast.AST) -> list[str]:
    text = _literal_text(arg)
    if text is not None:
        return [text]
    if isinstance(arg, ast.List | ast.Tuple):
        return [t for item in arg.elts if (t := _literal_text(None)) is not None]
    return []


def x__literal_arg_texts__mutmut_5(arg: ast.AST) -> list[str]:
    text = _literal_text(arg)
    if text is not None:
        return [text]
    if isinstance(arg, ast.List | ast.Tuple):
        return [t for item in arg.elts if (t := _literal_text(item)) is None]
    return []

mutants_x__literal_arg_texts__mutmut['_mutmut_orig'] = x__literal_arg_texts__mutmut_orig # type: ignore # mutmut generated
mutants_x__literal_arg_texts__mutmut['x__literal_arg_texts__mutmut_1'] = x__literal_arg_texts__mutmut_1 # type: ignore # mutmut generated
mutants_x__literal_arg_texts__mutmut['x__literal_arg_texts__mutmut_2'] = x__literal_arg_texts__mutmut_2 # type: ignore # mutmut generated
mutants_x__literal_arg_texts__mutmut['x__literal_arg_texts__mutmut_3'] = x__literal_arg_texts__mutmut_3 # type: ignore # mutmut generated
mutants_x__literal_arg_texts__mutmut['x__literal_arg_texts__mutmut_4'] = x__literal_arg_texts__mutmut_4 # type: ignore # mutmut generated
mutants_x__literal_arg_texts__mutmut['x__literal_arg_texts__mutmut_5'] = x__literal_arg_texts__mutmut_5 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_module_has_unactionable_error__mutmut)
def module_has_unactionable_error(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_orig(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_1(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_2(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_3(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_4(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_5(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_6(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_7(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_8(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_9(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_10(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return True
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_11(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = None
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_12(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(None)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_13(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.upper() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_14(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(None):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_15(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_16(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(None):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_17(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            break
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_18(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(None):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_19(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if any(marker in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_20(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(None):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_21(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker not in text.lower() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_22(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.upper() for marker in lowered):
                    return True
    return False


def x_module_has_unactionable_error__mutmut_23(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return False
    return False


def x_module_has_unactionable_error__mutmut_24(path: Path, *, markers: tuple[str, ...]) -> bool:
    """True iff ``path`` appends an error string lacking any action ``markers``.

    Pure helper (the detection core) so tests can assert on it directly. Walks
    ``<errors>.append/extend(...)`` calls and flags a literal-string argument
    carrying none of the (case-insensitive) markers. A syntax/decode error
    returns False (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    lowered = tuple(m.lower() for m in markers)
    for node in ast.walk(tree):
        if not _is_error_append_call(node):
            continue
        assert isinstance(node, ast.Call)  # noqa: S101  # narrowed by _is_error_append_call
        for arg in node.args:
            for text in _literal_arg_texts(arg):
                if not any(marker in text.lower() for marker in lowered):
                    return True
    return True

mutants_x_module_has_unactionable_error__mutmut['_mutmut_orig'] = x_module_has_unactionable_error__mutmut_orig # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_1'] = x_module_has_unactionable_error__mutmut_1 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_2'] = x_module_has_unactionable_error__mutmut_2 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_3'] = x_module_has_unactionable_error__mutmut_3 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_4'] = x_module_has_unactionable_error__mutmut_4 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_5'] = x_module_has_unactionable_error__mutmut_5 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_6'] = x_module_has_unactionable_error__mutmut_6 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_7'] = x_module_has_unactionable_error__mutmut_7 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_8'] = x_module_has_unactionable_error__mutmut_8 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_9'] = x_module_has_unactionable_error__mutmut_9 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_10'] = x_module_has_unactionable_error__mutmut_10 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_11'] = x_module_has_unactionable_error__mutmut_11 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_12'] = x_module_has_unactionable_error__mutmut_12 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_13'] = x_module_has_unactionable_error__mutmut_13 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_14'] = x_module_has_unactionable_error__mutmut_14 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_15'] = x_module_has_unactionable_error__mutmut_15 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_16'] = x_module_has_unactionable_error__mutmut_16 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_17'] = x_module_has_unactionable_error__mutmut_17 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_18'] = x_module_has_unactionable_error__mutmut_18 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_19'] = x_module_has_unactionable_error__mutmut_19 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_20'] = x_module_has_unactionable_error__mutmut_20 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_21'] = x_module_has_unactionable_error__mutmut_21 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_22'] = x_module_has_unactionable_error__mutmut_22 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_23'] = x_module_has_unactionable_error__mutmut_23 # type: ignore # mutmut generated
mutants_x_module_has_unactionable_error__mutmut['x_module_has_unactionable_error__mutmut_24'] = x_module_has_unactionable_error__mutmut_24 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁActionableFeedbackǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class ActionableFeedback(FitnessRule):
    """Flags check modules emitting errors without a fix/next/run marker."""

    name = "actionable-feedback"
    remediation = REMEDIATION
    extensions = (".py",)

    #: The action markers a message must carry. Instance attribute so
    #: ``from_config`` can override; class default is the affordance shape.
    markers: tuple[str, ...] = DEFAULT_ACTION_MARKERS

    @classmethod
    @_mutmut_mutated(mutants_xǁActionableFeedbackǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("markers")
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("markers")
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = None
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("markers")
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("markers")
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("markers")
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("markers")
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, )
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("markers")
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = None
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get(None)
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("XXmarkersXX")
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("MARKERS")
        if markers is not None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("markers")
        if markers is None:
            rule.markers = tuple(markers)
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("markers")
        if markers is not None:
            rule.markers = None
        return rule

    @classmethod
    def xǁActionableFeedbackǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ActionableFeedback:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ActionableFeedback)  # noqa: S101  # narrowing for mypy
        markers = config.get("markers")
        if markers is not None:
            rule.markers = tuple(None)
        return rule

    @_mutmut_mutated(mutants_xǁActionableFeedbackǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return module_has_unactionable_error(path, markers=self.markers)

    def xǁActionableFeedbackǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return module_has_unactionable_error(path, markers=self.markers)

    def xǁActionableFeedbackǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return module_has_unactionable_error(None, markers=self.markers)

    def xǁActionableFeedbackǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return module_has_unactionable_error(path, markers=None)

    def xǁActionableFeedbackǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return module_has_unactionable_error(markers=self.markers)

    def xǁActionableFeedbackǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return module_has_unactionable_error(path, )

mutants_xǁActionableFeedbackǁfrom_config__mutmut['_mutmut_orig'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_1'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_2'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_3'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_4'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_5'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_6'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_7'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_8'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_9'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_10'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_11'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfrom_config__mutmut['xǁActionableFeedbackǁfrom_config__mutmut_12'] = ActionableFeedback.xǁActionableFeedbackǁfrom_config__mutmut_12 # type: ignore # mutmut generated

mutants_xǁActionableFeedbackǁfile_has_violation__mutmut['_mutmut_orig'] = ActionableFeedback.xǁActionableFeedbackǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfile_has_violation__mutmut['xǁActionableFeedbackǁfile_has_violation__mutmut_1'] = ActionableFeedback.xǁActionableFeedbackǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfile_has_violation__mutmut['xǁActionableFeedbackǁfile_has_violation__mutmut_2'] = ActionableFeedback.xǁActionableFeedbackǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfile_has_violation__mutmut['xǁActionableFeedbackǁfile_has_violation__mutmut_3'] = ActionableFeedback.xǁActionableFeedbackǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁActionableFeedbackǁfile_has_violation__mutmut['xǁActionableFeedbackǁfile_has_violation__mutmut_4'] = ActionableFeedback.xǁActionableFeedbackǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ActionableFeedback:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ActionableFeedback.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ActionableFeedback:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ActionableFeedback.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ActionableFeedback:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ActionableFeedback.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ActionableFeedback:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ActionableFeedback.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ActionableFeedback:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ActionableFeedback.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> ActionableFeedback:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ActionableFeedback.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ActionableFeedback, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ActionableFeedback, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ActionableFeedback, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ActionableFeedback, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
