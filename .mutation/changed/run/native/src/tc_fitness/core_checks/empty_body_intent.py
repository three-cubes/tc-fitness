"""CORE check: empty_body_intent — Sonar S1186.

A function body that is exactly ``pass`` or ``...`` with no documentation is a
confusion vector: the reader can't tell whether it's an abstract contract, a
deliberate no-op satisfying a Protocol, or an accidentally-truncated function.
The fix: add a one-line docstring describing the contract, or an intent comment
explaining why the body is genuinely empty.

Ported from kairix ``scripts/checks/check_empty_body_intent.py`` (F20) and
re-expressed as a configurable, repo-agnostic rule. The intent-comment marker
defaults to the conventional phrase but is overridable via a ``marker`` knob;
the consumer supplies ``roots`` / ``exempt_files`` via ``[tool.tc_fitness]``.
No repo paths or globs are baked in.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The conventional intent-comment phrase — domain-intrinsic, overridable.
DEFAULT_MARKER = "Intentionally empty"

_ABSTRACT_DECORATORS = frozenset({"abstractmethod", "abstractproperty", "overload"})

REMEDIATION = _remediation(
    fix=(
        "add either a one-line docstring describing the Protocol contract the "
        "function satisfies, or an intent comment explaining why the body is "
        "genuinely a no-op."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.empty_body_intent",
    passing='def on_event(self, e): """No-op default; strategies override."""',
    forbidden="def on_event(self, e): pass  # no docstring, no intent comment",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__decorator_name__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__decorator_name__mutmut)
def _decorator_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Call):
        return _decorator_name(node.func)
    return None


def x__decorator_name__mutmut_orig(node: ast.expr) -> str | None:
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Call):
        return _decorator_name(node.func)
    return None


def x__decorator_name__mutmut_1(node: ast.expr) -> str | None:
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Call):
        return _decorator_name(None)
    return None

mutants_x__decorator_name__mutmut['_mutmut_orig'] = x__decorator_name__mutmut_orig # type: ignore # mutmut generated
mutants_x__decorator_name__mutmut['x__decorator_name__mutmut_1'] = x__decorator_name__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_abstract_or_overload__mutmut)
def _is_abstract_or_overload(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list)


def x__is_abstract_or_overload__mutmut_orig(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list)


def x__is_abstract_or_overload__mutmut_1(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(None)


def x__is_abstract_or_overload__mutmut_2(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(_decorator_name(None) in _ABSTRACT_DECORATORS for d in func.decorator_list)


def x__is_abstract_or_overload__mutmut_3(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(_decorator_name(d) not in _ABSTRACT_DECORATORS for d in func.decorator_list)

mutants_x__is_abstract_or_overload__mutmut['_mutmut_orig'] = x__is_abstract_or_overload__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_1'] = x__is_abstract_or_overload__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_2'] = x__is_abstract_or_overload__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_3'] = x__is_abstract_or_overload__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_docstring__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_docstring__mutmut)
def _has_docstring(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if not func.body:
        return False
    first = func.body[0]
    return (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    )


def x__has_docstring__mutmut_orig(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if not func.body:
        return False
    first = func.body[0]
    return (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    )


def x__has_docstring__mutmut_1(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if func.body:
        return False
    first = func.body[0]
    return (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    )


def x__has_docstring__mutmut_2(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if not func.body:
        return True
    first = func.body[0]
    return (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    )


def x__has_docstring__mutmut_3(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if not func.body:
        return False
    first = None
    return (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    )


def x__has_docstring__mutmut_4(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if not func.body:
        return False
    first = func.body[1]
    return (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    )


def x__has_docstring__mutmut_5(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if not func.body:
        return False
    first = func.body[0]
    return (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant) or isinstance(first.value.value, str)
    )


def x__has_docstring__mutmut_6(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if not func.body:
        return False
    first = func.body[0]
    return (
        isinstance(first, ast.Expr) or isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    )

mutants_x__has_docstring__mutmut['_mutmut_orig'] = x__has_docstring__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_docstring__mutmut['x__has_docstring__mutmut_1'] = x__has_docstring__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_docstring__mutmut['x__has_docstring__mutmut_2'] = x__has_docstring__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_docstring__mutmut['x__has_docstring__mutmut_3'] = x__has_docstring__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_docstring__mutmut['x__has_docstring__mutmut_4'] = x__has_docstring__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_docstring__mutmut['x__has_docstring__mutmut_5'] = x__has_docstring__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_docstring__mutmut['x__has_docstring__mutmut_6'] = x__has_docstring__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_ellipsis_expr__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_ellipsis_expr__mutmut)
def _is_ellipsis_expr(stmt: ast.stmt) -> bool:
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is ...


def x__is_ellipsis_expr__mutmut_orig(stmt: ast.stmt) -> bool:
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is ...


def x__is_ellipsis_expr__mutmut_1(stmt: ast.stmt) -> bool:
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) or stmt.value.value is ...


def x__is_ellipsis_expr__mutmut_2(stmt: ast.stmt) -> bool:
    return isinstance(stmt, ast.Expr) or isinstance(stmt.value, ast.Constant) and stmt.value.value is ...


def x__is_ellipsis_expr__mutmut_3(stmt: ast.stmt) -> bool:
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is not ...

mutants_x__is_ellipsis_expr__mutmut['_mutmut_orig'] = x__is_ellipsis_expr__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_ellipsis_expr__mutmut['x__is_ellipsis_expr__mutmut_1'] = x__is_ellipsis_expr__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_ellipsis_expr__mutmut['x__is_ellipsis_expr__mutmut_2'] = x__is_ellipsis_expr__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_ellipsis_expr__mutmut['x__is_ellipsis_expr__mutmut_3'] = x__is_ellipsis_expr__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_empty_body__mutmut)
def _is_empty_body(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_orig(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_1(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = None
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_2(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) != 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_3(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 2:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_4(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = None
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_5(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[1]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_6(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) and _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_7(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(None)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_8(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) != 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_9(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 3:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_10(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = None
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_11(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = None
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_12(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant) or isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_13(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr) or isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_14(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) and _is_ellipsis_expr(second)
    return False


def x__is_empty_body__mutmut_15(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(None)
    return False


def x__is_empty_body__mutmut_16(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if the body is exactly ``pass`` / ``...`` / ``docstring + pass|...``."""
    body = func.body
    if len(body) == 1:
        only = body[0]
        return isinstance(only, ast.Pass) or _is_ellipsis_expr(only)
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            return isinstance(second, ast.Pass) or _is_ellipsis_expr(second)
    return True

mutants_x__is_empty_body__mutmut['_mutmut_orig'] = x__is_empty_body__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_1'] = x__is_empty_body__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_2'] = x__is_empty_body__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_3'] = x__is_empty_body__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_4'] = x__is_empty_body__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_5'] = x__is_empty_body__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_6'] = x__is_empty_body__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_7'] = x__is_empty_body__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_8'] = x__is_empty_body__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_9'] = x__is_empty_body__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_10'] = x__is_empty_body__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_11'] = x__is_empty_body__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_12'] = x__is_empty_body__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_13'] = x__is_empty_body__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_14'] = x__is_empty_body__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_15'] = x__is_empty_body__mutmut_15 # type: ignore # mutmut generated
mutants_x__is_empty_body__mutmut['x__is_empty_body__mutmut_16'] = x__is_empty_body__mutmut_16 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_intent_comment__mutmut)
def _has_intent_comment(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_orig(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_1(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = None
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_2(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) + 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_3(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno and 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_4(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 2) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_5(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 2
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_6(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = None
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_7(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno and 1
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_8(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno and func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_9(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 2
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_10(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = None
    return marker in snippet


def x__has_intent_comment__mutmut_11(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(None)
    return marker in snippet


def x__has_intent_comment__mutmut_12(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "XX\nXX".join(source_lines[max(start - 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_13(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(None, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_14(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, None) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_15(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_16(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, ) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_17(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start + 1, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_18(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 2, 0) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_19(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, 1) : end])
    return marker in snippet


def x__has_intent_comment__mutmut_20(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    """True if ``marker`` appears in the function span or the line above ``def``."""
    start = (func.lineno or 1) - 1
    end = func.end_lineno or func.lineno or 1
    snippet = "\n".join(source_lines[max(start - 1, 0) : end])
    return marker not in snippet

mutants_x__has_intent_comment__mutmut['_mutmut_orig'] = x__has_intent_comment__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_1'] = x__has_intent_comment__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_2'] = x__has_intent_comment__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_3'] = x__has_intent_comment__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_4'] = x__has_intent_comment__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_5'] = x__has_intent_comment__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_6'] = x__has_intent_comment__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_7'] = x__has_intent_comment__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_8'] = x__has_intent_comment__mutmut_8 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_9'] = x__has_intent_comment__mutmut_9 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_10'] = x__has_intent_comment__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_11'] = x__has_intent_comment__mutmut_11 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_12'] = x__has_intent_comment__mutmut_12 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_13'] = x__has_intent_comment__mutmut_13 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_14'] = x__has_intent_comment__mutmut_14 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_15'] = x__has_intent_comment__mutmut_15 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_16'] = x__has_intent_comment__mutmut_16 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_17'] = x__has_intent_comment__mutmut_17 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_18'] = x__has_intent_comment__mutmut_18 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_19'] = x__has_intent_comment__mutmut_19 # type: ignore # mutmut generated
mutants_x__has_intent_comment__mutmut['x__has_intent_comment__mutmut_20'] = x__has_intent_comment__mutmut_20 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__function_violates__mutmut)
def _function_violates(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, source_lines, marker)


def x__function_violates__mutmut_orig(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, source_lines, marker)


def x__function_violates__mutmut_1(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(None):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, source_lines, marker)


def x__function_violates__mutmut_2(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return True
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, source_lines, marker)


def x__function_violates__mutmut_3(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, source_lines, marker)


def x__function_violates__mutmut_4(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(None):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, source_lines, marker)


def x__function_violates__mutmut_5(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return True
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, source_lines, marker)


def x__function_violates__mutmut_6(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(None):
        return False
    return not _has_intent_comment(func, source_lines, marker)


def x__function_violates__mutmut_7(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return True
    return not _has_intent_comment(func, source_lines, marker)


def x__function_violates__mutmut_8(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return _has_intent_comment(func, source_lines, marker)


def x__function_violates__mutmut_9(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(None, source_lines, marker)


def x__function_violates__mutmut_10(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, None, marker)


def x__function_violates__mutmut_11(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, source_lines, None)


def x__function_violates__mutmut_12(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(source_lines, marker)


def x__function_violates__mutmut_13(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, marker)


def x__function_violates__mutmut_14(
    func: ast.FunctionDef | ast.AsyncFunctionDef,
    source_lines: list[str],
    marker: str,
) -> bool:
    if _is_abstract_or_overload(func):
        return False
    if not _is_empty_body(func):
        return False
    if _has_docstring(func):
        return False
    return not _has_intent_comment(func, source_lines, )

mutants_x__function_violates__mutmut['_mutmut_orig'] = x__function_violates__mutmut_orig # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_1'] = x__function_violates__mutmut_1 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_2'] = x__function_violates__mutmut_2 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_3'] = x__function_violates__mutmut_3 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_4'] = x__function_violates__mutmut_4 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_5'] = x__function_violates__mutmut_5 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_6'] = x__function_violates__mutmut_6 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_7'] = x__function_violates__mutmut_7 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_8'] = x__function_violates__mutmut_8 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_9'] = x__function_violates__mutmut_9 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_10'] = x__function_violates__mutmut_10 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_11'] = x__function_violates__mutmut_11 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_12'] = x__function_violates__mutmut_12 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_13'] = x__function_violates__mutmut_13 # type: ignore # mutmut generated
mutants_x__function_violates__mutmut['x__function_violates__mutmut_14'] = x__function_violates__mutmut_14 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_module_has_undocumented_empty_body__mutmut)
def module_has_undocumented_empty_body(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_orig(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_1(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = None
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_2(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding=None)
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_3(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="XXutf-8XX")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_4(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="UTF-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_5(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = None
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_6(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_7(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=None)
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_8(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_9(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, )
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_10(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(None))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_11(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return True
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_12(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_13(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(None):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_14(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or _function_violates(
            node, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_15(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            None, source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_16(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, None, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_17(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, None
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_18(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            source_lines, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_19(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, marker
        ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_20(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, ):
            return True
    return False


def x_module_has_undocumented_empty_body__mutmut_21(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return False
    return False


def x_module_has_undocumented_empty_body__mutmut_22(path: Path, *, marker: str) -> bool:
    """True iff any function in ``path`` has an undocumented empty body (S1186).

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" — another check owns unparseable files.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    source_lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_violates(
            node, source_lines, marker
        ):
            return True
    return True

mutants_x_module_has_undocumented_empty_body__mutmut['_mutmut_orig'] = x_module_has_undocumented_empty_body__mutmut_orig # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_1'] = x_module_has_undocumented_empty_body__mutmut_1 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_2'] = x_module_has_undocumented_empty_body__mutmut_2 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_3'] = x_module_has_undocumented_empty_body__mutmut_3 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_4'] = x_module_has_undocumented_empty_body__mutmut_4 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_5'] = x_module_has_undocumented_empty_body__mutmut_5 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_6'] = x_module_has_undocumented_empty_body__mutmut_6 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_7'] = x_module_has_undocumented_empty_body__mutmut_7 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_8'] = x_module_has_undocumented_empty_body__mutmut_8 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_9'] = x_module_has_undocumented_empty_body__mutmut_9 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_10'] = x_module_has_undocumented_empty_body__mutmut_10 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_11'] = x_module_has_undocumented_empty_body__mutmut_11 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_12'] = x_module_has_undocumented_empty_body__mutmut_12 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_13'] = x_module_has_undocumented_empty_body__mutmut_13 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_14'] = x_module_has_undocumented_empty_body__mutmut_14 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_15'] = x_module_has_undocumented_empty_body__mutmut_15 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_16'] = x_module_has_undocumented_empty_body__mutmut_16 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_17'] = x_module_has_undocumented_empty_body__mutmut_17 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_18'] = x_module_has_undocumented_empty_body__mutmut_18 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_19'] = x_module_has_undocumented_empty_body__mutmut_19 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_20'] = x_module_has_undocumented_empty_body__mutmut_20 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_21'] = x_module_has_undocumented_empty_body__mutmut_21 # type: ignore # mutmut generated
mutants_x_module_has_undocumented_empty_body__mutmut['x_module_has_undocumented_empty_body__mutmut_22'] = x_module_has_undocumented_empty_body__mutmut_22 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁEmptyBodyIntentǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class EmptyBodyIntent(FitnessRule):
    """Flags files holding an undocumented empty function body (Sonar S1186)."""

    name = "empty-body-intent"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knob — the intent-comment phrase; overridable per consumer.
    marker: str = DEFAULT_MARKER

    @classmethod
    @_mutmut_mutated(mutants_xǁEmptyBodyIntentǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("marker", DEFAULT_MARKER))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("marker", DEFAULT_MARKER))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = None
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("marker", DEFAULT_MARKER))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("marker", DEFAULT_MARKER))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("marker", DEFAULT_MARKER))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("marker", DEFAULT_MARKER))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, )
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("marker", DEFAULT_MARKER))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = None
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(None)
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get(None, DEFAULT_MARKER))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("marker", None))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get(DEFAULT_MARKER))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("marker", ))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("XXmarkerXX", DEFAULT_MARKER))
        return rule

    @classmethod
    def xǁEmptyBodyIntentǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EmptyBodyIntent:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EmptyBodyIntent)  # noqa: S101  # narrowing for mypy
        rule.marker = str(config.get("MARKER", DEFAULT_MARKER))
        return rule

    @_mutmut_mutated(mutants_xǁEmptyBodyIntentǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return module_has_undocumented_empty_body(path, marker=self.marker)

    def xǁEmptyBodyIntentǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return module_has_undocumented_empty_body(path, marker=self.marker)

    def xǁEmptyBodyIntentǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return module_has_undocumented_empty_body(None, marker=self.marker)

    def xǁEmptyBodyIntentǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return module_has_undocumented_empty_body(path, marker=None)

    def xǁEmptyBodyIntentǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return module_has_undocumented_empty_body(marker=self.marker)

    def xǁEmptyBodyIntentǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return module_has_undocumented_empty_body(path, )

mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['_mutmut_orig'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_1'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_2'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_3'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_4'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_5'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_6'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_7'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_8'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_9'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_10'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_11'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_12'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfrom_config__mutmut['xǁEmptyBodyIntentǁfrom_config__mutmut_13'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfrom_config__mutmut_13 # type: ignore # mutmut generated

mutants_xǁEmptyBodyIntentǁfile_has_violation__mutmut['_mutmut_orig'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfile_has_violation__mutmut['xǁEmptyBodyIntentǁfile_has_violation__mutmut_1'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfile_has_violation__mutmut['xǁEmptyBodyIntentǁfile_has_violation__mutmut_2'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfile_has_violation__mutmut['xǁEmptyBodyIntentǁfile_has_violation__mutmut_3'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEmptyBodyIntentǁfile_has_violation__mutmut['xǁEmptyBodyIntentǁfile_has_violation__mutmut_4'] = EmptyBodyIntent.xǁEmptyBodyIntentǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EmptyBodyIntent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EmptyBodyIntent.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EmptyBodyIntent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EmptyBodyIntent.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EmptyBodyIntent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EmptyBodyIntent.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EmptyBodyIntent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EmptyBodyIntent.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EmptyBodyIntent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EmptyBodyIntent.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EmptyBodyIntent:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EmptyBodyIntent.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EmptyBodyIntent, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EmptyBodyIntent, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EmptyBodyIntent, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EmptyBodyIntent, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
