"""CORE check: unused_params_named — Sonar S1172.

A function parameter never read in the body is either dead code (delete it from
the signature) or a Protocol-required position the implementation does not need
(rename to ``_unused`` so the reader sees the intent and the linter stops
flagging it). The convention: rename to ``_``-prefixed if a Protocol requires
the slot; otherwise delete it.

Ported from kairix ``scripts/checks/check_unused_params_named.py`` (F19) and
re-expressed as a configurable, repo-agnostic rule. The detection is pure AST
with no domain-intrinsic threshold; the consumer supplies ``roots`` /
``exempt_files`` via ``[tool.tc_fitness]``. No repo paths or globs are baked in.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

_EXEMPT_NAMES = frozenset({"self", "cls"})
_ABSTRACT_DECORATORS = frozenset({"abstractmethod", "abstractproperty", "overload"})

REMEDIATION = _remediation(
    fix=(
        "if the unused parameter is required by a Protocol/abstract-base "
        "position, rename it with a leading underscore (_unused); if it is "
        "not load-bearing, delete it from the signature outright."
    ),
    nxt="re-run this check to confirm the gate goes green.",
    run="python -m tc_fitness.core_checks.unused_params_named",
    passing="def handle(event: Event, _context: Context) -> Result: ...",
    forbidden="def handle(event: Event, context: Context) -> Result:  # context never read",
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
mutants_x__is_not_implemented_raise__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_not_implemented_raise__mutmut)
def _is_not_implemented_raise(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or not isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) and target.id == "NotImplementedError"


def x__is_not_implemented_raise__mutmut_orig(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or not isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) and target.id == "NotImplementedError"


def x__is_not_implemented_raise__mutmut_1(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) and not isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) and target.id == "NotImplementedError"


def x__is_not_implemented_raise__mutmut_2(stmt: ast.stmt) -> bool:
    if isinstance(stmt, ast.Raise) or not isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) and target.id == "NotImplementedError"


def x__is_not_implemented_raise__mutmut_3(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) and target.id == "NotImplementedError"


def x__is_not_implemented_raise__mutmut_4(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or not isinstance(stmt.exc, ast.Name | ast.Call):
        return True
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) and target.id == "NotImplementedError"


def x__is_not_implemented_raise__mutmut_5(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or not isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = None
    return isinstance(target, ast.Name) and target.id == "NotImplementedError"


def x__is_not_implemented_raise__mutmut_6(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or not isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) or target.id == "NotImplementedError"


def x__is_not_implemented_raise__mutmut_7(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or not isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) and target.id != "NotImplementedError"


def x__is_not_implemented_raise__mutmut_8(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or not isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) and target.id == "XXNotImplementedErrorXX"


def x__is_not_implemented_raise__mutmut_9(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or not isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) and target.id == "notimplementederror"


def x__is_not_implemented_raise__mutmut_10(stmt: ast.stmt) -> bool:
    if not isinstance(stmt, ast.Raise) or not isinstance(stmt.exc, ast.Name | ast.Call):
        return False
    target = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
    return isinstance(target, ast.Name) and target.id == "NOTIMPLEMENTEDERROR"

mutants_x__is_not_implemented_raise__mutmut['_mutmut_orig'] = x__is_not_implemented_raise__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_not_implemented_raise__mutmut['x__is_not_implemented_raise__mutmut_1'] = x__is_not_implemented_raise__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_not_implemented_raise__mutmut['x__is_not_implemented_raise__mutmut_2'] = x__is_not_implemented_raise__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_not_implemented_raise__mutmut['x__is_not_implemented_raise__mutmut_3'] = x__is_not_implemented_raise__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_not_implemented_raise__mutmut['x__is_not_implemented_raise__mutmut_4'] = x__is_not_implemented_raise__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_not_implemented_raise__mutmut['x__is_not_implemented_raise__mutmut_5'] = x__is_not_implemented_raise__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_not_implemented_raise__mutmut['x__is_not_implemented_raise__mutmut_6'] = x__is_not_implemented_raise__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_not_implemented_raise__mutmut['x__is_not_implemented_raise__mutmut_7'] = x__is_not_implemented_raise__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_not_implemented_raise__mutmut['x__is_not_implemented_raise__mutmut_8'] = x__is_not_implemented_raise__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_not_implemented_raise__mutmut['x__is_not_implemented_raise__mutmut_9'] = x__is_not_implemented_raise__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_not_implemented_raise__mutmut['x__is_not_implemented_raise__mutmut_10'] = x__is_not_implemented_raise__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_abstract_or_overload__mutmut)
def _is_abstract_or_overload(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_orig(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_1(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(None):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_2(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(None) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_3(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) not in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_4(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return False
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_5(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = None
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_6(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) != 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_7(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 2:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_8(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = None
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_9(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[1]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_10(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return False
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_11(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant) or (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_12(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr) or isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_13(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) and only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_14(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is not ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_15(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return False
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_16(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(None):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_17(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return False
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_18(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) != 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_19(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 3:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_20(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = None
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_21(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = None
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_22(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant) or isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_23(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr) or isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_24(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return False
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_25(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant) or second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_26(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr) or isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_27(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is not ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_28(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return False
            if _is_not_implemented_raise(second):
                return True
    return False


def x__is_abstract_or_overload__mutmut_29(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(None):
                return True
    return False


def x__is_abstract_or_overload__mutmut_30(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return False
    return False


def x__is_abstract_or_overload__mutmut_31(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if decorated abstract/overload, or the body is a stub.

    Stub bodies: a lone ``...`` / ``pass`` / ``raise NotImplementedError`` /
    docstring, or a docstring followed by one of those — the signature is the
    contract.
    """
    if any(_decorator_name(d) in _ABSTRACT_DECORATORS for d in func.decorator_list):
        return True
    body = func.body
    if len(body) == 1:
        only = body[0]
        if isinstance(only, ast.Pass):
            return True
        if (
            isinstance(only, ast.Expr)
            and isinstance(only.value, ast.Constant)
            and (isinstance(only.value.value, str) or only.value.value is ...)
        ):
            return True
        if _is_not_implemented_raise(only):
            return True
    if len(body) == 2:
        first, second = body
        first_is_doc = (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        )
        if first_is_doc:
            if isinstance(second, ast.Pass):
                return True
            if (
                isinstance(second, ast.Expr)
                and isinstance(second.value, ast.Constant)
                and second.value.value is ...
            ):
                return True
            if _is_not_implemented_raise(second):
                return True
    return True

mutants_x__is_abstract_or_overload__mutmut['_mutmut_orig'] = x__is_abstract_or_overload__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_1'] = x__is_abstract_or_overload__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_2'] = x__is_abstract_or_overload__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_3'] = x__is_abstract_or_overload__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_4'] = x__is_abstract_or_overload__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_5'] = x__is_abstract_or_overload__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_6'] = x__is_abstract_or_overload__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_7'] = x__is_abstract_or_overload__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_8'] = x__is_abstract_or_overload__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_9'] = x__is_abstract_or_overload__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_10'] = x__is_abstract_or_overload__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_11'] = x__is_abstract_or_overload__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_12'] = x__is_abstract_or_overload__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_13'] = x__is_abstract_or_overload__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_14'] = x__is_abstract_or_overload__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_15'] = x__is_abstract_or_overload__mutmut_15 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_16'] = x__is_abstract_or_overload__mutmut_16 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_17'] = x__is_abstract_or_overload__mutmut_17 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_18'] = x__is_abstract_or_overload__mutmut_18 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_19'] = x__is_abstract_or_overload__mutmut_19 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_20'] = x__is_abstract_or_overload__mutmut_20 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_21'] = x__is_abstract_or_overload__mutmut_21 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_22'] = x__is_abstract_or_overload__mutmut_22 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_23'] = x__is_abstract_or_overload__mutmut_23 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_24'] = x__is_abstract_or_overload__mutmut_24 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_25'] = x__is_abstract_or_overload__mutmut_25 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_26'] = x__is_abstract_or_overload__mutmut_26 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_27'] = x__is_abstract_or_overload__mutmut_27 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_28'] = x__is_abstract_or_overload__mutmut_28 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_29'] = x__is_abstract_or_overload__mutmut_29 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_30'] = x__is_abstract_or_overload__mutmut_30 # type: ignore # mutmut generated
mutants_x__is_abstract_or_overload__mutmut['x__is_abstract_or_overload__mutmut_31'] = x__is_abstract_or_overload__mutmut_31 # type: ignore # mutmut generated
mutants_x__is_property_setter__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_property_setter__mutmut)
def _is_property_setter(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(isinstance(d, ast.Attribute) and d.attr == "setter" for d in func.decorator_list)


def x__is_property_setter__mutmut_orig(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(isinstance(d, ast.Attribute) and d.attr == "setter" for d in func.decorator_list)


def x__is_property_setter__mutmut_1(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(None)


def x__is_property_setter__mutmut_2(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(isinstance(d, ast.Attribute) or d.attr == "setter" for d in func.decorator_list)


def x__is_property_setter__mutmut_3(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(isinstance(d, ast.Attribute) and d.attr != "setter" for d in func.decorator_list)


def x__is_property_setter__mutmut_4(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(isinstance(d, ast.Attribute) and d.attr == "XXsetterXX" for d in func.decorator_list)


def x__is_property_setter__mutmut_5(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return any(isinstance(d, ast.Attribute) and d.attr == "SETTER" for d in func.decorator_list)

mutants_x__is_property_setter__mutmut['_mutmut_orig'] = x__is_property_setter__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_property_setter__mutmut['x__is_property_setter__mutmut_1'] = x__is_property_setter__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_property_setter__mutmut['x__is_property_setter__mutmut_2'] = x__is_property_setter__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_property_setter__mutmut['x__is_property_setter__mutmut_3'] = x__is_property_setter__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_property_setter__mutmut['x__is_property_setter__mutmut_4'] = x__is_property_setter__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_property_setter__mutmut['x__is_property_setter__mutmut_5'] = x__is_property_setter__mutmut_5 # type: ignore # mutmut generated
mutants_x__names_read__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__names_read__mutmut)
def _names_read(body: list[ast.stmt]) -> set[str]:
    refs: set[str] = set()
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                refs.add(node.id)
    return refs


def x__names_read__mutmut_orig(body: list[ast.stmt]) -> set[str]:
    refs: set[str] = set()
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                refs.add(node.id)
    return refs


def x__names_read__mutmut_1(body: list[ast.stmt]) -> set[str]:
    refs: set[str] = None
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                refs.add(node.id)
    return refs


def x__names_read__mutmut_2(body: list[ast.stmt]) -> set[str]:
    refs: set[str] = set()
    for stmt in body:
        for node in ast.walk(None):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                refs.add(node.id)
    return refs


def x__names_read__mutmut_3(body: list[ast.stmt]) -> set[str]:
    refs: set[str] = set()
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Name) or isinstance(node.ctx, ast.Load):
                refs.add(node.id)
    return refs


def x__names_read__mutmut_4(body: list[ast.stmt]) -> set[str]:
    refs: set[str] = set()
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                refs.add(None)
    return refs

mutants_x__names_read__mutmut['_mutmut_orig'] = x__names_read__mutmut_orig # type: ignore # mutmut generated
mutants_x__names_read__mutmut['x__names_read__mutmut_1'] = x__names_read__mutmut_1 # type: ignore # mutmut generated
mutants_x__names_read__mutmut['x__names_read__mutmut_2'] = x__names_read__mutmut_2 # type: ignore # mutmut generated
mutants_x__names_read__mutmut['x__names_read__mutmut_3'] = x__names_read__mutmut_3 # type: ignore # mutmut generated
mutants_x__names_read__mutmut['x__names_read__mutmut_4'] = x__names_read__mutmut_4 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__function_has_unused_param__mutmut)
def _function_has_unused_param(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_orig(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_1(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) and _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_2(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(None) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_3(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(None):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_4(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return True
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_5(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = None
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_6(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = None
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_7(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_8(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return True
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_9(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = None
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_10(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(None)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_11(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = None
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_12(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES and name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_13(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name not in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_14(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith(None):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_15(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("XX_XX"):
            continue
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_16(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            break
        if name not in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_17(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name in refs:
            return True
    return False


def x__function_has_unused_param__mutmut_18(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return False
    return False


def x__function_has_unused_param__mutmut_19(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    if _is_abstract_or_overload(func) or _is_property_setter(func):
        return False
    args = func.args
    all_args = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    if not all_args:
        return False
    refs = _names_read(func.body)
    for arg in all_args:
        name = arg.arg
        if name in _EXEMPT_NAMES or name.startswith("_"):
            continue
        if name not in refs:
            return True
    return True

mutants_x__function_has_unused_param__mutmut['_mutmut_orig'] = x__function_has_unused_param__mutmut_orig # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_1'] = x__function_has_unused_param__mutmut_1 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_2'] = x__function_has_unused_param__mutmut_2 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_3'] = x__function_has_unused_param__mutmut_3 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_4'] = x__function_has_unused_param__mutmut_4 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_5'] = x__function_has_unused_param__mutmut_5 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_6'] = x__function_has_unused_param__mutmut_6 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_7'] = x__function_has_unused_param__mutmut_7 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_8'] = x__function_has_unused_param__mutmut_8 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_9'] = x__function_has_unused_param__mutmut_9 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_10'] = x__function_has_unused_param__mutmut_10 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_11'] = x__function_has_unused_param__mutmut_11 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_12'] = x__function_has_unused_param__mutmut_12 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_13'] = x__function_has_unused_param__mutmut_13 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_14'] = x__function_has_unused_param__mutmut_14 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_15'] = x__function_has_unused_param__mutmut_15 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_16'] = x__function_has_unused_param__mutmut_16 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_17'] = x__function_has_unused_param__mutmut_17 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_18'] = x__function_has_unused_param__mutmut_18 # type: ignore # mutmut generated
mutants_x__function_has_unused_param__mutmut['x__function_has_unused_param__mutmut_19'] = x__function_has_unused_param__mutmut_19 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_module_has_unused_param__mutmut)
def module_has_unused_param(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_orig(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_1(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_2(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_3(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_4(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_5(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_6(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_7(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_8(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_9(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_10(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_11(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(None):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_12(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or _function_has_unused_param(node):
            return True
    return False


def x_module_has_unused_param__mutmut_13(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(None):
            return True
    return False


def x_module_has_unused_param__mutmut_14(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return False
    return False


def x_module_has_unused_param__mutmut_15(path: Path) -> bool:
    """True iff any function in ``path`` has an unused, non-underscore parameter.

    Pure helper (the detection core). A syntax / decode / read error is a
    violation because the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _function_has_unused_param(node):
            return True
    return True

mutants_x_module_has_unused_param__mutmut['_mutmut_orig'] = x_module_has_unused_param__mutmut_orig # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_1'] = x_module_has_unused_param__mutmut_1 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_2'] = x_module_has_unused_param__mutmut_2 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_3'] = x_module_has_unused_param__mutmut_3 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_4'] = x_module_has_unused_param__mutmut_4 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_5'] = x_module_has_unused_param__mutmut_5 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_6'] = x_module_has_unused_param__mutmut_6 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_7'] = x_module_has_unused_param__mutmut_7 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_8'] = x_module_has_unused_param__mutmut_8 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_9'] = x_module_has_unused_param__mutmut_9 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_10'] = x_module_has_unused_param__mutmut_10 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_11'] = x_module_has_unused_param__mutmut_11 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_12'] = x_module_has_unused_param__mutmut_12 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_13'] = x_module_has_unused_param__mutmut_13 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_14'] = x_module_has_unused_param__mutmut_14 # type: ignore # mutmut generated
mutants_x_module_has_unused_param__mutmut['x_module_has_unused_param__mutmut_15'] = x_module_has_unused_param__mutmut_15 # type: ignore # mutmut generated
mutants_xǁUnusedParamsNamedǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class UnusedParamsNamed(FitnessRule):
    """Flags files holding an unused, non-underscore-prefixed parameter (S1172)."""

    name = "unused-params-named"
    remediation = REMEDIATION
    extensions = (".py",)

    @_mutmut_mutated(mutants_xǁUnusedParamsNamedǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return module_has_unused_param(path)

    def xǁUnusedParamsNamedǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return module_has_unused_param(path)

    def xǁUnusedParamsNamedǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return module_has_unused_param(None)

mutants_xǁUnusedParamsNamedǁfile_has_violation__mutmut['_mutmut_orig'] = UnusedParamsNamed.xǁUnusedParamsNamedǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁUnusedParamsNamedǁfile_has_violation__mutmut['xǁUnusedParamsNamedǁfile_has_violation__mutmut_1'] = UnusedParamsNamed.xǁUnusedParamsNamedǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> FitnessRule:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return UnusedParamsNamed.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> FitnessRule:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return UnusedParamsNamed.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> FitnessRule:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return UnusedParamsNamed.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> FitnessRule:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return UnusedParamsNamed.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> FitnessRule:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return UnusedParamsNamed.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> FitnessRule:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return UnusedParamsNamed.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(UnusedParamsNamed, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(UnusedParamsNamed, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(UnusedParamsNamed, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(UnusedParamsNamed, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
