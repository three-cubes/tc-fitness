"""CORE check: no-test-only-kwargs — forbid ``*_fn=None`` test seams in prod.

A production free function declaring a parameter whose name ends in a
test-seam suffix (``_fn`` / ``_loader`` / ``_factory`` ...) defaulting to
``None`` is the canonical "I added a test seam to production" smell:
production grows complexity for tests without operator value, the swap-point
sits on every production call, and nothing forces tests to actually use the
seam (so it rots). The legitimate substitution pattern is constructor
injection on a ``Deps`` dataclass at a boundary class.

Detection (AST, free functions only -- methods on a ``ClassDef`` are exempt
because they ARE the canonical Deps-constructor shape): any
positional-with-default or keyword-only parameter whose name ends in a
configured seam suffix AND whose default is the ``None`` constant.

Ported from tc-agent-zone ``scripts/checks/no_test_only_kwargs.py`` (itself
kairix F6) and re-expressed as a configurable, repo-agnostic rule: scan roots
arrive from config; the seam suffixes are the rule's own shape (overridable).
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Default test-seam parameter-name suffixes -- the smell's own shape, not
#: repo identity. Overridable via config.
DEFAULT_SEAM_SUFFIXES: tuple[str, ...] = ("_fn",)

REMEDIATION = _remediation(
    fix=(
        "delete the *_fn=None parameter and move the collaborator onto a "
        "@dataclass Deps class with field(default_factory=...); tests "
        "construct an overridden Deps and pass it as a single argument."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.no_test_only_kwargs",
    passing="def route(intent: str, deps: RouterDeps | None = None) -> str: ...",
    forbidden="def route(intent: str, clock_fn=None, load_routes_fn=None) -> str: ...",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__is_test_only_kwarg__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_test_only_kwarg__mutmut)
def _is_test_only_kwarg(param: ast.arg, default: ast.expr | None, suffixes: tuple[str, ...]) -> bool:
    """True iff (param, default) describes a ``*<suffix>=None`` kwarg."""
    if default is None:
        return False
    if not param.arg.endswith(suffixes):
        return False
    return isinstance(default, ast.Constant) and default.value is None


def x__is_test_only_kwarg__mutmut_orig(param: ast.arg, default: ast.expr | None, suffixes: tuple[str, ...]) -> bool:
    """True iff (param, default) describes a ``*<suffix>=None`` kwarg."""
    if default is None:
        return False
    if not param.arg.endswith(suffixes):
        return False
    return isinstance(default, ast.Constant) and default.value is None


def x__is_test_only_kwarg__mutmut_1(param: ast.arg, default: ast.expr | None, suffixes: tuple[str, ...]) -> bool:
    """True iff (param, default) describes a ``*<suffix>=None`` kwarg."""
    if default is not None:
        return False
    if not param.arg.endswith(suffixes):
        return False
    return isinstance(default, ast.Constant) and default.value is None


def x__is_test_only_kwarg__mutmut_2(param: ast.arg, default: ast.expr | None, suffixes: tuple[str, ...]) -> bool:
    """True iff (param, default) describes a ``*<suffix>=None`` kwarg."""
    if default is None:
        return True
    if not param.arg.endswith(suffixes):
        return False
    return isinstance(default, ast.Constant) and default.value is None


def x__is_test_only_kwarg__mutmut_3(param: ast.arg, default: ast.expr | None, suffixes: tuple[str, ...]) -> bool:
    """True iff (param, default) describes a ``*<suffix>=None`` kwarg."""
    if default is None:
        return False
    if param.arg.endswith(suffixes):
        return False
    return isinstance(default, ast.Constant) and default.value is None


def x__is_test_only_kwarg__mutmut_4(param: ast.arg, default: ast.expr | None, suffixes: tuple[str, ...]) -> bool:
    """True iff (param, default) describes a ``*<suffix>=None`` kwarg."""
    if default is None:
        return False
    if not param.arg.endswith(None):
        return False
    return isinstance(default, ast.Constant) and default.value is None


def x__is_test_only_kwarg__mutmut_5(param: ast.arg, default: ast.expr | None, suffixes: tuple[str, ...]) -> bool:
    """True iff (param, default) describes a ``*<suffix>=None`` kwarg."""
    if default is None:
        return False
    if not param.arg.endswith(suffixes):
        return True
    return isinstance(default, ast.Constant) and default.value is None


def x__is_test_only_kwarg__mutmut_6(param: ast.arg, default: ast.expr | None, suffixes: tuple[str, ...]) -> bool:
    """True iff (param, default) describes a ``*<suffix>=None`` kwarg."""
    if default is None:
        return False
    if not param.arg.endswith(suffixes):
        return False
    return isinstance(default, ast.Constant) or default.value is None


def x__is_test_only_kwarg__mutmut_7(param: ast.arg, default: ast.expr | None, suffixes: tuple[str, ...]) -> bool:
    """True iff (param, default) describes a ``*<suffix>=None`` kwarg."""
    if default is None:
        return False
    if not param.arg.endswith(suffixes):
        return False
    return isinstance(default, ast.Constant) and default.value is not None

mutants_x__is_test_only_kwarg__mutmut['_mutmut_orig'] = x__is_test_only_kwarg__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_test_only_kwarg__mutmut['x__is_test_only_kwarg__mutmut_1'] = x__is_test_only_kwarg__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_test_only_kwarg__mutmut['x__is_test_only_kwarg__mutmut_2'] = x__is_test_only_kwarg__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_test_only_kwarg__mutmut['x__is_test_only_kwarg__mutmut_3'] = x__is_test_only_kwarg__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_test_only_kwarg__mutmut['x__is_test_only_kwarg__mutmut_4'] = x__is_test_only_kwarg__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_test_only_kwarg__mutmut['x__is_test_only_kwarg__mutmut_5'] = x__is_test_only_kwarg__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_test_only_kwarg__mutmut['x__is_test_only_kwarg__mutmut_6'] = x__is_test_only_kwarg__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_test_only_kwarg__mutmut['x__is_test_only_kwarg__mutmut_7'] = x__is_test_only_kwarg__mutmut_7 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__scan_function__mutmut)
def _scan_function(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_orig(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_1(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = None
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_2(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = None
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_3(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(None)
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_4(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(None, reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_5(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), None, strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_6(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=None))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_7(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_8(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_9(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), ))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_10(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(None), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_11(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(None), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_12(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=True))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_13(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = None
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_14(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(None)
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_15(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(None, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_16(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, None, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_17(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=None))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_18(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_19(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_20(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, ))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_21(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=True))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, suffixes)
    ]


def x__scan_function__mutmut_22(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(None, default, suffixes)
    ]


def x__scan_function__mutmut_23(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, None, suffixes)
    ]


def x__scan_function__mutmut_24(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, None)
    ]


def x__scan_function__mutmut_25(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(default, suffixes)
    ]


def x__scan_function__mutmut_26(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, suffixes)
    ]


def x__scan_function__mutmut_27(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    suffixes: tuple[str, ...],
) -> list[tuple[str, str, int]]:
    """Return the test-only kwargs declared on a single function."""
    args = node.args
    defaults_for_args = dict(zip(reversed(args.args), reversed(args.defaults), strict=False))
    kwonly_defaults = dict(zip(args.kwonlyargs, args.kw_defaults, strict=False))
    return [
        (node.name, param.arg, node.lineno)
        for param, default in {**defaults_for_args, **kwonly_defaults}.items()
        if _is_test_only_kwarg(param, default, )
    ]

mutants_x__scan_function__mutmut['_mutmut_orig'] = x__scan_function__mutmut_orig # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_1'] = x__scan_function__mutmut_1 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_2'] = x__scan_function__mutmut_2 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_3'] = x__scan_function__mutmut_3 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_4'] = x__scan_function__mutmut_4 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_5'] = x__scan_function__mutmut_5 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_6'] = x__scan_function__mutmut_6 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_7'] = x__scan_function__mutmut_7 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_8'] = x__scan_function__mutmut_8 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_9'] = x__scan_function__mutmut_9 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_10'] = x__scan_function__mutmut_10 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_11'] = x__scan_function__mutmut_11 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_12'] = x__scan_function__mutmut_12 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_13'] = x__scan_function__mutmut_13 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_14'] = x__scan_function__mutmut_14 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_15'] = x__scan_function__mutmut_15 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_16'] = x__scan_function__mutmut_16 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_17'] = x__scan_function__mutmut_17 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_18'] = x__scan_function__mutmut_18 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_19'] = x__scan_function__mutmut_19 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_20'] = x__scan_function__mutmut_20 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_21'] = x__scan_function__mutmut_21 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_22'] = x__scan_function__mutmut_22 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_23'] = x__scan_function__mutmut_23 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_24'] = x__scan_function__mutmut_24 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_25'] = x__scan_function__mutmut_25 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_26'] = x__scan_function__mutmut_26 # type: ignore # mutmut generated
mutants_x__scan_function__mutmut['x__scan_function__mutmut_27'] = x__scan_function__mutmut_27 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_find_test_only_kwargs_in_file__mutmut)
def find_test_only_kwargs_in_file(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_orig(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_1(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_2(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_3(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_4(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_5(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_6(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_7(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_8(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_9(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_10(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("XX<unreadable>XX", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_11(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<UNREADABLE>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_12(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "XX<source>XX", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_13(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<SOURCE>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_14(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 2)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_15(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_16(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(None):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_17(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                None
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_18(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(None) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_19(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_20(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(None):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_21(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or id(node) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_22(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(None) not in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_23(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) in class_func_ids:
            out.extend(_scan_function(node, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_24(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(None)
    return out


def x_find_test_only_kwargs_in_file__mutmut_25(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(None, suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_26(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, None))
    return out


def x_find_test_only_kwargs_in_file__mutmut_27(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(suffixes))
    return out


def x_find_test_only_kwargs_in_file__mutmut_28(path: Path, *, suffixes: tuple[str, ...]) -> list[tuple[str, str, int]]:
    """Return (function-name, param-name, lineno) for every seam parameter.

    Pure helper (the detection core): walks every free function (methods on a
    ``ClassDef`` are out of scope -- they are the canonical Deps shape). A
    syntax / decode / read error is a violation because the configured source
    could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return [("<unreadable>", "<source>", 1)]
    class_func_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_func_ids.update(
                id(child) for child in node.body if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    out: list[tuple[str, str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and id(node) not in class_func_ids:
            out.extend(_scan_function(node, ))
    return out

mutants_x_find_test_only_kwargs_in_file__mutmut['_mutmut_orig'] = x_find_test_only_kwargs_in_file__mutmut_orig # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_1'] = x_find_test_only_kwargs_in_file__mutmut_1 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_2'] = x_find_test_only_kwargs_in_file__mutmut_2 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_3'] = x_find_test_only_kwargs_in_file__mutmut_3 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_4'] = x_find_test_only_kwargs_in_file__mutmut_4 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_5'] = x_find_test_only_kwargs_in_file__mutmut_5 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_6'] = x_find_test_only_kwargs_in_file__mutmut_6 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_7'] = x_find_test_only_kwargs_in_file__mutmut_7 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_8'] = x_find_test_only_kwargs_in_file__mutmut_8 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_9'] = x_find_test_only_kwargs_in_file__mutmut_9 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_10'] = x_find_test_only_kwargs_in_file__mutmut_10 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_11'] = x_find_test_only_kwargs_in_file__mutmut_11 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_12'] = x_find_test_only_kwargs_in_file__mutmut_12 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_13'] = x_find_test_only_kwargs_in_file__mutmut_13 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_14'] = x_find_test_only_kwargs_in_file__mutmut_14 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_15'] = x_find_test_only_kwargs_in_file__mutmut_15 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_16'] = x_find_test_only_kwargs_in_file__mutmut_16 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_17'] = x_find_test_only_kwargs_in_file__mutmut_17 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_18'] = x_find_test_only_kwargs_in_file__mutmut_18 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_19'] = x_find_test_only_kwargs_in_file__mutmut_19 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_20'] = x_find_test_only_kwargs_in_file__mutmut_20 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_21'] = x_find_test_only_kwargs_in_file__mutmut_21 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_22'] = x_find_test_only_kwargs_in_file__mutmut_22 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_23'] = x_find_test_only_kwargs_in_file__mutmut_23 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_24'] = x_find_test_only_kwargs_in_file__mutmut_24 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_25'] = x_find_test_only_kwargs_in_file__mutmut_25 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_26'] = x_find_test_only_kwargs_in_file__mutmut_26 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_27'] = x_find_test_only_kwargs_in_file__mutmut_27 # type: ignore # mutmut generated
mutants_x_find_test_only_kwargs_in_file__mutmut['x_find_test_only_kwargs_in_file__mutmut_28'] = x_find_test_only_kwargs_in_file__mutmut_28 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoTestOnlyKwargsǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoTestOnlyKwargs(FitnessRule):
    """Flags production free functions with ``*_fn=None`` test seams."""

    name = "no-test-only-kwargs"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knobs.
    seam_suffixes: tuple[str, ...] = DEFAULT_SEAM_SUFFIXES

    @classmethod
    @_mutmut_mutated(mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("seam_suffixes")
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("seam_suffixes")
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = None
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("seam_suffixes")
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("seam_suffixes")
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("seam_suffixes")
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("seam_suffixes")
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, )
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("seam_suffixes")
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = None
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get(None)
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("XXseam_suffixesXX")
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("SEAM_SUFFIXES")
        rule.seam_suffixes = tuple(suffixes) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("seam_suffixes")
        rule.seam_suffixes = None
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("seam_suffixes")
        rule.seam_suffixes = tuple(None) if suffixes is not None else DEFAULT_SEAM_SUFFIXES
        return rule

    @classmethod
    def xǁNoTestOnlyKwargsǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestOnlyKwargs:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestOnlyKwargs)  # noqa: S101  # narrowing for mypy
        suffixes = config.get("seam_suffixes")
        rule.seam_suffixes = tuple(suffixes) if suffixes is None else DEFAULT_SEAM_SUFFIXES
        return rule

    @_mutmut_mutated(mutants_xǁNoTestOnlyKwargsǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return bool(find_test_only_kwargs_in_file(path, suffixes=self.seam_suffixes))

    def xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return bool(find_test_only_kwargs_in_file(path, suffixes=self.seam_suffixes))

    def xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return bool(None)

    def xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return bool(find_test_only_kwargs_in_file(None, suffixes=self.seam_suffixes))

    def xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return bool(find_test_only_kwargs_in_file(path, suffixes=None))

    def xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return bool(find_test_only_kwargs_in_file(suffixes=self.seam_suffixes))

    def xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        return bool(find_test_only_kwargs_in_file(path, ))

mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['_mutmut_orig'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_1'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_2'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_3'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_4'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_5'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_6'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_7'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_8'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_9'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_10'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_11'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfrom_config__mutmut['xǁNoTestOnlyKwargsǁfrom_config__mutmut_12'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfrom_config__mutmut_12 # type: ignore # mutmut generated

mutants_xǁNoTestOnlyKwargsǁfile_has_violation__mutmut['_mutmut_orig'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfile_has_violation__mutmut['xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_1'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfile_has_violation__mutmut['xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_2'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfile_has_violation__mutmut['xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_3'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfile_has_violation__mutmut['xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_4'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoTestOnlyKwargsǁfile_has_violation__mutmut['xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_5'] = NoTestOnlyKwargs.xǁNoTestOnlyKwargsǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestOnlyKwargs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestOnlyKwargs.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestOnlyKwargs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestOnlyKwargs.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestOnlyKwargs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestOnlyKwargs.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestOnlyKwargs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestOnlyKwargs.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestOnlyKwargs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestOnlyKwargs.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestOnlyKwargs:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestOnlyKwargs.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoTestOnlyKwargs, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoTestOnlyKwargs, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoTestOnlyKwargs, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoTestOnlyKwargs, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
