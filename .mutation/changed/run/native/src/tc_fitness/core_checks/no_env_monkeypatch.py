"""CORE check: no-env-monkeypatch — no env-var monkeypatch on owned keys.

A test that does ``monkeypatch.setenv("MYAPP_DATA_DIR", ...)`` to influence a
production env-var read couples the test to a global side-channel and hides
the boundary. The boundary-only pattern reads each owned env var ONCE inside a
``Paths``-style class; tests construct that object directly and inject it.

This rule walks each in-scope test file via the AST and flags any
``monkeypatch.{setenv,setattr,delenv}(...)`` call whose first positional
argument is a string literal beginning with one of the configured env-var
prefixes.

Ported from kairix ``scripts/checks/check_no_env_monkeypatch.py`` (F2) and
re-expressed as a configurable, repo-agnostic rule: the env-var prefixes that
identify an owned key arrive from config -- NO repo-specific prefix is baked
in. (A rule bound with no prefixes matches nothing.)
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The monkeypatch methods that mutate env / attribute state.
_TARGET_METHODS = frozenset({"setenv", "setattr", "delenv"})

REMEDIATION = _remediation(
    fix=(
        'replace monkeypatch.setenv("<PREFIX>_...", ...) with explicit '
        "construction of a Paths-style boundary object and pass it as an "
        "argument to the use case. If production reads the env var directly, "
        "refactor it to accept that boundary object as an explicit argument."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.no_env_monkeypatch",
    passing="paths = FakePaths(data_dir=tmp_path); result = use_case(paths=paths)",
    forbidden='monkeypatch.setenv("MYAPP_DATA_DIR", str(tmp_path)); result = use_case()',
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__is_monkeypatch_call__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_monkeypatch_call__mutmut)
def _is_monkeypatch_call(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = call.func
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr not in _TARGET_METHODS:
        return False
    return isinstance(func.value, ast.Name) and func.value.id == "monkeypatch"


def x__is_monkeypatch_call__mutmut_orig(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = call.func
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr not in _TARGET_METHODS:
        return False
    return isinstance(func.value, ast.Name) and func.value.id == "monkeypatch"


def x__is_monkeypatch_call__mutmut_1(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = None
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr not in _TARGET_METHODS:
        return False
    return isinstance(func.value, ast.Name) and func.value.id == "monkeypatch"


def x__is_monkeypatch_call__mutmut_2(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = call.func
    if isinstance(func, ast.Attribute):
        return False
    if func.attr not in _TARGET_METHODS:
        return False
    return isinstance(func.value, ast.Name) and func.value.id == "monkeypatch"


def x__is_monkeypatch_call__mutmut_3(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = call.func
    if not isinstance(func, ast.Attribute):
        return True
    if func.attr not in _TARGET_METHODS:
        return False
    return isinstance(func.value, ast.Name) and func.value.id == "monkeypatch"


def x__is_monkeypatch_call__mutmut_4(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = call.func
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr in _TARGET_METHODS:
        return False
    return isinstance(func.value, ast.Name) and func.value.id == "monkeypatch"


def x__is_monkeypatch_call__mutmut_5(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = call.func
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr not in _TARGET_METHODS:
        return True
    return isinstance(func.value, ast.Name) and func.value.id == "monkeypatch"


def x__is_monkeypatch_call__mutmut_6(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = call.func
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr not in _TARGET_METHODS:
        return False
    return isinstance(func.value, ast.Name) or func.value.id == "monkeypatch"


def x__is_monkeypatch_call__mutmut_7(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = call.func
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr not in _TARGET_METHODS:
        return False
    return isinstance(func.value, ast.Name) and func.value.id != "monkeypatch"


def x__is_monkeypatch_call__mutmut_8(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = call.func
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr not in _TARGET_METHODS:
        return False
    return isinstance(func.value, ast.Name) and func.value.id == "XXmonkeypatchXX"


def x__is_monkeypatch_call__mutmut_9(call: ast.Call) -> bool:
    """``monkeypatch.{setenv,setattr,delenv}(...)`` on the bare receiver name."""
    func = call.func
    if not isinstance(func, ast.Attribute):
        return False
    if func.attr not in _TARGET_METHODS:
        return False
    return isinstance(func.value, ast.Name) and func.value.id == "MONKEYPATCH"

mutants_x__is_monkeypatch_call__mutmut['_mutmut_orig'] = x__is_monkeypatch_call__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_monkeypatch_call__mutmut['x__is_monkeypatch_call__mutmut_1'] = x__is_monkeypatch_call__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_call__mutmut['x__is_monkeypatch_call__mutmut_2'] = x__is_monkeypatch_call__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_call__mutmut['x__is_monkeypatch_call__mutmut_3'] = x__is_monkeypatch_call__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_call__mutmut['x__is_monkeypatch_call__mutmut_4'] = x__is_monkeypatch_call__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_call__mutmut['x__is_monkeypatch_call__mutmut_5'] = x__is_monkeypatch_call__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_call__mutmut['x__is_monkeypatch_call__mutmut_6'] = x__is_monkeypatch_call__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_call__mutmut['x__is_monkeypatch_call__mutmut_7'] = x__is_monkeypatch_call__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_call__mutmut['x__is_monkeypatch_call__mutmut_8'] = x__is_monkeypatch_call__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_call__mutmut['x__is_monkeypatch_call__mutmut_9'] = x__is_monkeypatch_call__mutmut_9 # type: ignore # mutmut generated
mutants_x__first_arg_has_prefix__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__first_arg_has_prefix__mutmut)
def _first_arg_has_prefix(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if not call.args or not prefixes:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.startswith(prefixes)
    return False


def x__first_arg_has_prefix__mutmut_orig(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if not call.args or not prefixes:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.startswith(prefixes)
    return False


def x__first_arg_has_prefix__mutmut_1(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if not call.args and not prefixes:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.startswith(prefixes)
    return False


def x__first_arg_has_prefix__mutmut_2(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if call.args or not prefixes:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.startswith(prefixes)
    return False


def x__first_arg_has_prefix__mutmut_3(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if not call.args or prefixes:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.startswith(prefixes)
    return False


def x__first_arg_has_prefix__mutmut_4(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if not call.args or not prefixes:
        return True
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.startswith(prefixes)
    return False


def x__first_arg_has_prefix__mutmut_5(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if not call.args or not prefixes:
        return False
    first = None
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.startswith(prefixes)
    return False


def x__first_arg_has_prefix__mutmut_6(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if not call.args or not prefixes:
        return False
    first = call.args[1]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.startswith(prefixes)
    return False


def x__first_arg_has_prefix__mutmut_7(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if not call.args or not prefixes:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) or isinstance(first.value, str):
        return first.value.startswith(prefixes)
    return False


def x__first_arg_has_prefix__mutmut_8(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if not call.args or not prefixes:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.startswith(None)
    return False


def x__first_arg_has_prefix__mutmut_9(call: ast.Call, prefixes: tuple[str, ...]) -> bool:
    """First positional arg is a string literal starting with a configured prefix."""
    if not call.args or not prefixes:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.startswith(prefixes)
    return True

mutants_x__first_arg_has_prefix__mutmut['_mutmut_orig'] = x__first_arg_has_prefix__mutmut_orig # type: ignore # mutmut generated
mutants_x__first_arg_has_prefix__mutmut['x__first_arg_has_prefix__mutmut_1'] = x__first_arg_has_prefix__mutmut_1 # type: ignore # mutmut generated
mutants_x__first_arg_has_prefix__mutmut['x__first_arg_has_prefix__mutmut_2'] = x__first_arg_has_prefix__mutmut_2 # type: ignore # mutmut generated
mutants_x__first_arg_has_prefix__mutmut['x__first_arg_has_prefix__mutmut_3'] = x__first_arg_has_prefix__mutmut_3 # type: ignore # mutmut generated
mutants_x__first_arg_has_prefix__mutmut['x__first_arg_has_prefix__mutmut_4'] = x__first_arg_has_prefix__mutmut_4 # type: ignore # mutmut generated
mutants_x__first_arg_has_prefix__mutmut['x__first_arg_has_prefix__mutmut_5'] = x__first_arg_has_prefix__mutmut_5 # type: ignore # mutmut generated
mutants_x__first_arg_has_prefix__mutmut['x__first_arg_has_prefix__mutmut_6'] = x__first_arg_has_prefix__mutmut_6 # type: ignore # mutmut generated
mutants_x__first_arg_has_prefix__mutmut['x__first_arg_has_prefix__mutmut_7'] = x__first_arg_has_prefix__mutmut_7 # type: ignore # mutmut generated
mutants_x__first_arg_has_prefix__mutmut['x__first_arg_has_prefix__mutmut_8'] = x__first_arg_has_prefix__mutmut_8 # type: ignore # mutmut generated
mutants_x__first_arg_has_prefix__mutmut['x__first_arg_has_prefix__mutmut_9'] = x__first_arg_has_prefix__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_has_env_monkeypatch__mutmut)
def file_has_env_monkeypatch(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_orig(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_1(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_2(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_3(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_4(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_5(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_6(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_7(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_8(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_9(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_10(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_11(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(None):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_12(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node) or _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_13(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call) or _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_14(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(None)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_15(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(None, prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_16(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, None)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_17(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(prefixes)
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_18(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, )
        ):
            return True
    return False


def x_file_has_env_monkeypatch__mutmut_19(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return False
    return False


def x_file_has_env_monkeypatch__mutmut_20(path: Path, *, prefixes: tuple[str, ...]) -> bool:
    """True iff ``path`` monkeypatches an env/attr key matching a prefix.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and _is_monkeypatch_call(node)
            and _first_arg_has_prefix(node, prefixes)
        ):
            return True
    return True

mutants_x_file_has_env_monkeypatch__mutmut['_mutmut_orig'] = x_file_has_env_monkeypatch__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_1'] = x_file_has_env_monkeypatch__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_2'] = x_file_has_env_monkeypatch__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_3'] = x_file_has_env_monkeypatch__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_4'] = x_file_has_env_monkeypatch__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_5'] = x_file_has_env_monkeypatch__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_6'] = x_file_has_env_monkeypatch__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_7'] = x_file_has_env_monkeypatch__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_8'] = x_file_has_env_monkeypatch__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_9'] = x_file_has_env_monkeypatch__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_10'] = x_file_has_env_monkeypatch__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_11'] = x_file_has_env_monkeypatch__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_12'] = x_file_has_env_monkeypatch__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_13'] = x_file_has_env_monkeypatch__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_14'] = x_file_has_env_monkeypatch__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_15'] = x_file_has_env_monkeypatch__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_16'] = x_file_has_env_monkeypatch__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_17'] = x_file_has_env_monkeypatch__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_18'] = x_file_has_env_monkeypatch__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_19'] = x_file_has_env_monkeypatch__mutmut_19 # type: ignore # mutmut generated
mutants_x_file_has_env_monkeypatch__mutmut['x_file_has_env_monkeypatch__mutmut_20'] = x_file_has_env_monkeypatch__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoEnvMonkeypatchǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoEnvMonkeypatch(FitnessRule):
    """Flags test files that monkeypatch an owned env-var key."""

    name = "no-env-monkeypatch"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Owned env-var prefixes -- repo-supplied, no default identity.
    env_prefixes: tuple[str, ...] = ()

    @classmethod
    @_mutmut_mutated(mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("env_prefixes")
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("env_prefixes")
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = None
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("env_prefixes")
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("env_prefixes")
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("env_prefixes")
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("env_prefixes")
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, )
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("env_prefixes")
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = None
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get(None)
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("XXenv_prefixesXX")
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("ENV_PREFIXES")
        rule.env_prefixes = tuple(prefixes) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("env_prefixes")
        rule.env_prefixes = None
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("env_prefixes")
        rule.env_prefixes = tuple(None) if prefixes is not None else ()
        return rule

    @classmethod
    def xǁNoEnvMonkeypatchǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoEnvMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoEnvMonkeypatch)  # noqa: S101  # narrowing for mypy
        prefixes = config.get("env_prefixes")
        rule.env_prefixes = tuple(prefixes) if prefixes is None else ()
        return rule

    @_mutmut_mutated(mutants_xǁNoEnvMonkeypatchǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_has_env_monkeypatch(path, prefixes=self.env_prefixes)

    def xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_has_env_monkeypatch(path, prefixes=self.env_prefixes)

    def xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_has_env_monkeypatch(None, prefixes=self.env_prefixes)

    def xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_has_env_monkeypatch(path, prefixes=None)

    def xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_has_env_monkeypatch(prefixes=self.env_prefixes)

    def xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_has_env_monkeypatch(path, )

mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['_mutmut_orig'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_1'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_2'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_3'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_4'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_5'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_6'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_7'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_8'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_9'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_10'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_11'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfrom_config__mutmut['xǁNoEnvMonkeypatchǁfrom_config__mutmut_12'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfrom_config__mutmut_12 # type: ignore # mutmut generated

mutants_xǁNoEnvMonkeypatchǁfile_has_violation__mutmut['_mutmut_orig'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfile_has_violation__mutmut['xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_1'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfile_has_violation__mutmut['xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_2'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfile_has_violation__mutmut['xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_3'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoEnvMonkeypatchǁfile_has_violation__mutmut['xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_4'] = NoEnvMonkeypatch.xǁNoEnvMonkeypatchǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoEnvMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoEnvMonkeypatch.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoEnvMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoEnvMonkeypatch.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoEnvMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoEnvMonkeypatch.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoEnvMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoEnvMonkeypatch.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoEnvMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoEnvMonkeypatch.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoEnvMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoEnvMonkeypatch.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoEnvMonkeypatch, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoEnvMonkeypatch, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoEnvMonkeypatch, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoEnvMonkeypatch, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
