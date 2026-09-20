"""CORE check: script-help-smoke — every argparse CLI answers ``--help``.

A single smoke that proves an argparse CLI is invocable AND wires every
declared long-flag through to its ``--help`` output -- catching the whole
"the script doesn't actually run / the parser fails to build" class of
regression with far less surface than enumerating every flag/state cell.

Contract: for every in-scope Python file that (1) defines a ``main()``
function AND (2) instantiates ``argparse.ArgumentParser(...)``, this gate
asserts both:

  - ``python <script> --help`` exits 0 within the configured timeout, AND
  - every long-form flag declared via ``add_argument("--name", ...)`` appears
    in the captured ``--help`` output.

A file that times out (work runs at import time before argparse fires) or
exits non-zero, or whose help omits a declared flag, is a violation.

Ported from tc-agent-zone ``scripts/checks/script_help_smoke.py`` and
re-expressed as a configurable, repo-agnostic rule: scan roots, the skipped
directory segments, the per-file exemptions, the help timeout, and the Python
interpreter all arrive from config -- NO repo path is baked in. The only
intrinsic constant is the ``--help`` invocation contract itself.
"""

from __future__ import annotations

import ast
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Default --help timeout. A CLI that cannot print help in this window is
#: broken for the smoke contract (it likely runs work at import time).
DEFAULT_HELP_TIMEOUT_SECONDS = 5
#: Directory segments never treated as a public CLI surface.
DEFAULT_SKIP_DIR_SEGMENTS: tuple[str, ...] = ("__pycache__", ".venv", "node_modules", "tests", "test")

REMEDIATION = _remediation(
    fix=(
        "make `python <script> --help` exit 0 and list every declared --flag. "
        "argparse renders all add_argument flags by default, so a missing flag "
        "means the parser fails to build or the script does work at import time "
        "before argparse fires -- move that work inside main()."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.script_help_smoke",
    passing="python scripts/my_cli.py --help  # exits 0, lists --agent --out-dir",
    forbidden="a CLI that imports a heavy dep at module top-level so --help times out",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__is_argument_parser_call__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_argument_parser_call__mutmut)
def _is_argument_parser_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_orig(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_1(node: ast.AST) -> bool:
    if isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_2(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return True
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_3(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = None
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_4(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = None
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_5(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) or func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_6(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id != "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_7(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "XXArgumentParserXX"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_8(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "argumentparser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_9(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ARGUMENTPARSER"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_10(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = None
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_11(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) or func.attr == "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_12(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr != "ArgumentParser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_13(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "XXArgumentParserXX"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_14(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "argumentparser"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_15(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ARGUMENTPARSER"
    return name_match or attr_match


def x__is_argument_parser_call__mutmut_16(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    name_match = isinstance(func, ast.Name) and func.id == "ArgumentParser"
    attr_match = isinstance(func, ast.Attribute) and func.attr == "ArgumentParser"
    return name_match and attr_match

mutants_x__is_argument_parser_call__mutmut['_mutmut_orig'] = x__is_argument_parser_call__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_1'] = x__is_argument_parser_call__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_2'] = x__is_argument_parser_call__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_3'] = x__is_argument_parser_call__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_4'] = x__is_argument_parser_call__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_5'] = x__is_argument_parser_call__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_6'] = x__is_argument_parser_call__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_7'] = x__is_argument_parser_call__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_8'] = x__is_argument_parser_call__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_9'] = x__is_argument_parser_call__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_10'] = x__is_argument_parser_call__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_11'] = x__is_argument_parser_call__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_12'] = x__is_argument_parser_call__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_13'] = x__is_argument_parser_call__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_14'] = x__is_argument_parser_call__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_15'] = x__is_argument_parser_call__mutmut_15 # type: ignore # mutmut generated
mutants_x__is_argument_parser_call__mutmut['x__is_argument_parser_call__mutmut_16'] = x__is_argument_parser_call__mutmut_16 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_main_and_argparse__mutmut)
def _has_main_and_argparse(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_orig(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_1(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = None
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_2(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = True
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_3(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_4(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = True
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_5(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(None):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_6(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_7(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name != "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_8(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "XXmainXX":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_9(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "MAIN":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_10(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = None
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_11(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = False
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_12(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(None):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_13(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = None
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_14(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = False
        if has_main and has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_15(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main or has_argparse:
            return True
    return False


def x__has_main_and_argparse__mutmut_16(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return False
    return False


def x__has_main_and_argparse__mutmut_17(tree: ast.AST) -> bool:
    """True iff the module declares ``def main()`` AND instantiates ``ArgumentParser``."""
    has_main = False
    has_argparse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
        elif _is_argument_parser_call(node):
            has_argparse = True
        if has_main and has_argparse:
            return True
    return True

mutants_x__has_main_and_argparse__mutmut['_mutmut_orig'] = x__has_main_and_argparse__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_1'] = x__has_main_and_argparse__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_2'] = x__has_main_and_argparse__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_3'] = x__has_main_and_argparse__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_4'] = x__has_main_and_argparse__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_5'] = x__has_main_and_argparse__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_6'] = x__has_main_and_argparse__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_7'] = x__has_main_and_argparse__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_8'] = x__has_main_and_argparse__mutmut_8 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_9'] = x__has_main_and_argparse__mutmut_9 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_10'] = x__has_main_and_argparse__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_11'] = x__has_main_and_argparse__mutmut_11 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_12'] = x__has_main_and_argparse__mutmut_12 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_13'] = x__has_main_and_argparse__mutmut_13 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_14'] = x__has_main_and_argparse__mutmut_14 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_15'] = x__has_main_and_argparse__mutmut_15 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_16'] = x__has_main_and_argparse__mutmut_16 # type: ignore # mutmut generated
mutants_x__has_main_and_argparse__mutmut['x__has_main_and_argparse__mutmut_17'] = x__has_main_and_argparse__mutmut_17 # type: ignore # mutmut generated
mutants_x__is_add_argument_call__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_add_argument_call__mutmut)
def _is_add_argument_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return isinstance(func, ast.Attribute) and func.attr == "add_argument"


def x__is_add_argument_call__mutmut_orig(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return isinstance(func, ast.Attribute) and func.attr == "add_argument"


def x__is_add_argument_call__mutmut_1(node: ast.AST) -> bool:
    if isinstance(node, ast.Call):
        return False
    func = node.func
    return isinstance(func, ast.Attribute) and func.attr == "add_argument"


def x__is_add_argument_call__mutmut_2(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return True
    func = node.func
    return isinstance(func, ast.Attribute) and func.attr == "add_argument"


def x__is_add_argument_call__mutmut_3(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = None
    return isinstance(func, ast.Attribute) and func.attr == "add_argument"


def x__is_add_argument_call__mutmut_4(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return isinstance(func, ast.Attribute) or func.attr == "add_argument"


def x__is_add_argument_call__mutmut_5(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return isinstance(func, ast.Attribute) and func.attr != "add_argument"


def x__is_add_argument_call__mutmut_6(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return isinstance(func, ast.Attribute) and func.attr == "XXadd_argumentXX"


def x__is_add_argument_call__mutmut_7(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    return isinstance(func, ast.Attribute) and func.attr == "ADD_ARGUMENT"

mutants_x__is_add_argument_call__mutmut['_mutmut_orig'] = x__is_add_argument_call__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_add_argument_call__mutmut['x__is_add_argument_call__mutmut_1'] = x__is_add_argument_call__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_add_argument_call__mutmut['x__is_add_argument_call__mutmut_2'] = x__is_add_argument_call__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_add_argument_call__mutmut['x__is_add_argument_call__mutmut_3'] = x__is_add_argument_call__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_add_argument_call__mutmut['x__is_add_argument_call__mutmut_4'] = x__is_add_argument_call__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_add_argument_call__mutmut['x__is_add_argument_call__mutmut_5'] = x__is_add_argument_call__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_add_argument_call__mutmut['x__is_add_argument_call__mutmut_6'] = x__is_add_argument_call__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_add_argument_call__mutmut['x__is_add_argument_call__mutmut_7'] = x__is_add_argument_call__mutmut_7 # type: ignore # mutmut generated
mutants_x__long_flag_arg__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__long_flag_arg__mutmut)
def _long_flag_arg(arg: ast.expr) -> str | None:
    if not (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
        return None
    return arg.value if arg.value.startswith("--") else None


def x__long_flag_arg__mutmut_orig(arg: ast.expr) -> str | None:
    if not (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
        return None
    return arg.value if arg.value.startswith("--") else None


def x__long_flag_arg__mutmut_1(arg: ast.expr) -> str | None:
    if (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
        return None
    return arg.value if arg.value.startswith("--") else None


def x__long_flag_arg__mutmut_2(arg: ast.expr) -> str | None:
    if not (isinstance(arg, ast.Constant) or isinstance(arg.value, str)):
        return None
    return arg.value if arg.value.startswith("--") else None


def x__long_flag_arg__mutmut_3(arg: ast.expr) -> str | None:
    if not (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
        return None
    return arg.value if arg.value.startswith(None) else None


def x__long_flag_arg__mutmut_4(arg: ast.expr) -> str | None:
    if not (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
        return None
    return arg.value if arg.value.startswith("XX--XX") else None

mutants_x__long_flag_arg__mutmut['_mutmut_orig'] = x__long_flag_arg__mutmut_orig # type: ignore # mutmut generated
mutants_x__long_flag_arg__mutmut['x__long_flag_arg__mutmut_1'] = x__long_flag_arg__mutmut_1 # type: ignore # mutmut generated
mutants_x__long_flag_arg__mutmut['x__long_flag_arg__mutmut_2'] = x__long_flag_arg__mutmut_2 # type: ignore # mutmut generated
mutants_x__long_flag_arg__mutmut['x__long_flag_arg__mutmut_3'] = x__long_flag_arg__mutmut_3 # type: ignore # mutmut generated
mutants_x__long_flag_arg__mutmut['x__long_flag_arg__mutmut_4'] = x__long_flag_arg__mutmut_4 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_extract_declared_flags__mutmut)
def extract_declared_flags(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_orig(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_1(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = None
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_2(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = None
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_3(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(None):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_4(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_5(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(None):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_6(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            break
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_7(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = None
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_8(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(None)
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_9(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name or name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_10(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name in seen:
                seen.add(name)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_11(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(None)
                flags.append(name)
    return tuple(flags)


def x_extract_declared_flags__mutmut_12(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(name)
                flags.append(None)
    return tuple(flags)


def x_extract_declared_flags__mutmut_13(tree: ast.AST) -> tuple[str, ...]:
    """Return every long-form flag declared via ``add_argument("--name", ...)``.

    Pure helper (the detection core): positional args and short flags are
    intentionally ignored -- the smoke contract is about long-form flags being
    wired through to the help surface.
    """
    flags: list[str] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not _is_add_argument_call(node):
            continue
        for arg in node.args:  # type: ignore[attr-defined]  # narrowed by _is_add_argument_call
            name = _long_flag_arg(arg)
            if name and name not in seen:
                seen.add(name)
                flags.append(name)
    return tuple(None)

mutants_x_extract_declared_flags__mutmut['_mutmut_orig'] = x_extract_declared_flags__mutmut_orig # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_1'] = x_extract_declared_flags__mutmut_1 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_2'] = x_extract_declared_flags__mutmut_2 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_3'] = x_extract_declared_flags__mutmut_3 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_4'] = x_extract_declared_flags__mutmut_4 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_5'] = x_extract_declared_flags__mutmut_5 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_6'] = x_extract_declared_flags__mutmut_6 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_7'] = x_extract_declared_flags__mutmut_7 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_8'] = x_extract_declared_flags__mutmut_8 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_9'] = x_extract_declared_flags__mutmut_9 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_10'] = x_extract_declared_flags__mutmut_10 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_11'] = x_extract_declared_flags__mutmut_11 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_12'] = x_extract_declared_flags__mutmut_12 # type: ignore # mutmut generated
mutants_x_extract_declared_flags__mutmut['x_extract_declared_flags__mutmut_13'] = x_extract_declared_flags__mutmut_13 # type: ignore # mutmut generated
mutants_x__parse__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__parse__mutmut)
def _parse(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError):
        return None


def x__parse__mutmut_orig(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError):
        return None


def x__parse__mutmut_1(path: Path) -> ast.AST | None:
    try:
        return ast.parse(None, filename=str(path))
    except (OSError, SyntaxError):
        return None


def x__parse__mutmut_2(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (OSError, SyntaxError):
        return None


def x__parse__mutmut_3(path: Path) -> ast.AST | None:
    try:
        return ast.parse(filename=str(path))
    except (OSError, SyntaxError):
        return None


def x__parse__mutmut_4(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), )
    except (OSError, SyntaxError):
        return None


def x__parse__mutmut_5(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding=None), filename=str(path))
    except (OSError, SyntaxError):
        return None


def x__parse__mutmut_6(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (OSError, SyntaxError):
        return None


def x__parse__mutmut_7(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (OSError, SyntaxError):
        return None


def x__parse__mutmut_8(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (OSError, SyntaxError):
        return None

mutants_x__parse__mutmut['_mutmut_orig'] = x__parse__mutmut_orig # type: ignore # mutmut generated
mutants_x__parse__mutmut['x__parse__mutmut_1'] = x__parse__mutmut_1 # type: ignore # mutmut generated
mutants_x__parse__mutmut['x__parse__mutmut_2'] = x__parse__mutmut_2 # type: ignore # mutmut generated
mutants_x__parse__mutmut['x__parse__mutmut_3'] = x__parse__mutmut_3 # type: ignore # mutmut generated
mutants_x__parse__mutmut['x__parse__mutmut_4'] = x__parse__mutmut_4 # type: ignore # mutmut generated
mutants_x__parse__mutmut['x__parse__mutmut_5'] = x__parse__mutmut_5 # type: ignore # mutmut generated
mutants_x__parse__mutmut['x__parse__mutmut_6'] = x__parse__mutmut_6 # type: ignore # mutmut generated
mutants_x__parse__mutmut['x__parse__mutmut_7'] = x__parse__mutmut_7 # type: ignore # mutmut generated
mutants_x__parse__mutmut['x__parse__mutmut_8'] = x__parse__mutmut_8 # type: ignore # mutmut generated
mutants_x__run_help__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__run_help__mutmut)
def _run_help(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_orig(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_1(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = None
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_2(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_3(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=None,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_4(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=None,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_5(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=None,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_6(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=None,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_7(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_8(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_9(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_10(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_11(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_12(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(None), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_13(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "XX--helpXX"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_14(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--HELP"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_15(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=False,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_16(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=False,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_17(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_18(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, "XXXX"
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def x__run_help__mutmut_19(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") - (result.stderr or "")


def x__run_help__mutmut_20(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout and "") + (result.stderr or "")


def x__run_help__mutmut_21(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "XXXX") + (result.stderr or "")


def x__run_help__mutmut_22(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr and "")


def x__run_help__mutmut_23(script: Path, *, python: str, timeout: int) -> tuple[int | None, str]:
    """Invoke ``<python> <script> --help`` with a hard timeout.

    Returns (exit_code, combined_output); ``exit_code is None`` on timeout.
    """
    try:
        result = subprocess.run(  # noqa: S603  # args are repo-internal script paths
            [python, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None, ""
    return result.returncode, (result.stdout or "") + (result.stderr or "XXXX")

mutants_x__run_help__mutmut['_mutmut_orig'] = x__run_help__mutmut_orig # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_1'] = x__run_help__mutmut_1 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_2'] = x__run_help__mutmut_2 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_3'] = x__run_help__mutmut_3 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_4'] = x__run_help__mutmut_4 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_5'] = x__run_help__mutmut_5 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_6'] = x__run_help__mutmut_6 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_7'] = x__run_help__mutmut_7 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_8'] = x__run_help__mutmut_8 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_9'] = x__run_help__mutmut_9 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_10'] = x__run_help__mutmut_10 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_11'] = x__run_help__mutmut_11 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_12'] = x__run_help__mutmut_12 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_13'] = x__run_help__mutmut_13 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_14'] = x__run_help__mutmut_14 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_15'] = x__run_help__mutmut_15 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_16'] = x__run_help__mutmut_16 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_17'] = x__run_help__mutmut_17 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_18'] = x__run_help__mutmut_18 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_19'] = x__run_help__mutmut_19 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_20'] = x__run_help__mutmut_20 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_21'] = x__run_help__mutmut_21 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_22'] = x__run_help__mutmut_22 # type: ignore # mutmut generated
mutants_x__run_help__mutmut['x__run_help__mutmut_23'] = x__run_help__mutmut_23 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_script_help_violates__mutmut)
def script_help_violates(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_orig(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_1(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = None
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_2(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(None)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_3(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None and not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_4(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is not None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_5(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_6(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(None):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_7(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return True
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_8(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = None
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_9(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(None)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_10(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = None
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_11(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(None, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_12(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=None, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_13(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=None)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_14(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_15(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_16(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, )
    if code is None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_17(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None and code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_18(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is not None or code != 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_19(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code == 0:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_20(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 1:
        return True
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_21(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return False
    return any(flag not in output for flag in declared)


def x_script_help_violates__mutmut_22(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(None)


def x_script_help_violates__mutmut_23(script: Path, *, python: str, timeout: int) -> bool:
    """True iff ``--help`` times out, exits non-zero, or omits a declared flag.

    Pure helper (the detection core) so tests can drive it against a fixture
    script without going through the gate machinery.
    """
    tree = _parse(script)
    if tree is None or not _has_main_and_argparse(tree):
        return False
    declared = extract_declared_flags(tree)
    code, output = _run_help(script, python=python, timeout=timeout)
    if code is None or code != 0:
        return True
    return any(flag in output for flag in declared)

mutants_x_script_help_violates__mutmut['_mutmut_orig'] = x_script_help_violates__mutmut_orig # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_1'] = x_script_help_violates__mutmut_1 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_2'] = x_script_help_violates__mutmut_2 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_3'] = x_script_help_violates__mutmut_3 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_4'] = x_script_help_violates__mutmut_4 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_5'] = x_script_help_violates__mutmut_5 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_6'] = x_script_help_violates__mutmut_6 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_7'] = x_script_help_violates__mutmut_7 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_8'] = x_script_help_violates__mutmut_8 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_9'] = x_script_help_violates__mutmut_9 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_10'] = x_script_help_violates__mutmut_10 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_11'] = x_script_help_violates__mutmut_11 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_12'] = x_script_help_violates__mutmut_12 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_13'] = x_script_help_violates__mutmut_13 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_14'] = x_script_help_violates__mutmut_14 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_15'] = x_script_help_violates__mutmut_15 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_16'] = x_script_help_violates__mutmut_16 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_17'] = x_script_help_violates__mutmut_17 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_18'] = x_script_help_violates__mutmut_18 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_19'] = x_script_help_violates__mutmut_19 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_20'] = x_script_help_violates__mutmut_20 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_21'] = x_script_help_violates__mutmut_21 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_22'] = x_script_help_violates__mutmut_22 # type: ignore # mutmut generated
mutants_x_script_help_violates__mutmut['x_script_help_violates__mutmut_23'] = x_script_help_violates__mutmut_23 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁScriptHelpSmokeǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁScriptHelpSmokeǁrun__mutmut: MutantDict = {}  # type: ignore


class ScriptHelpSmoke(FitnessRule):
    """Flags argparse CLIs whose ``--help`` is broken or omits a declared flag."""

    name = "script-help-smoke"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knobs.
    help_timeout_seconds: int = DEFAULT_HELP_TIMEOUT_SECONDS
    python_executable: str = sys.executable

    @classmethod
    @_mutmut_mutated(mutants_xǁScriptHelpSmokeǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = None
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, )
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = None
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(None)
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get(None, DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", None))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get(DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", ))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("XXhelp_timeout_secondsXX", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("HELP_TIMEOUT_SECONDS", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = None
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("python_executable") and sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get(None) or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("XXpython_executableXX") or sys.executable
        return rule

    @classmethod
    def xǁScriptHelpSmokeǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> ScriptHelpSmoke:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, ScriptHelpSmoke)  # noqa: S101  # narrowing for mypy
        rule.help_timeout_seconds = int(config.get("help_timeout_seconds", DEFAULT_HELP_TIMEOUT_SECONDS))
        rule.python_executable = config.get("PYTHON_EXECUTABLE") or sys.executable
        return rule

    @_mutmut_mutated(mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        if super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_2(self, rel: str) -> bool:
        if not super().is_in_scope(None):
            return False
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_3(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return True
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_4(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = None
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_5(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(None).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_6(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(None):
            return False
        return not Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_7(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(seg not in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_8(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return True
        return not Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_9(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return Path(rel).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_10(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith(None)

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_11(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(None).name.startswith("test_")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_12(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith("XXtest_XX")

    def xǁScriptHelpSmokeǁis_in_scope__mutmut_13(self, rel: str) -> bool:
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(seg in parts for seg in DEFAULT_SKIP_DIR_SEGMENTS):
            return False
        return not Path(rel).name.startswith("TEST_")

    @_mutmut_mutated(mutants_xǁScriptHelpSmokeǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return script_help_violates(
            path,
            python=self.python_executable,
            timeout=self.help_timeout_seconds,
        )

    def xǁScriptHelpSmokeǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return script_help_violates(
            path,
            python=self.python_executable,
            timeout=self.help_timeout_seconds,
        )

    def xǁScriptHelpSmokeǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return script_help_violates(
            None,
            python=self.python_executable,
            timeout=self.help_timeout_seconds,
        )

    def xǁScriptHelpSmokeǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return script_help_violates(
            path,
            python=None,
            timeout=self.help_timeout_seconds,
        )

    def xǁScriptHelpSmokeǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return script_help_violates(
            path,
            python=self.python_executable,
            timeout=None,
        )

    def xǁScriptHelpSmokeǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return script_help_violates(
            python=self.python_executable,
            timeout=self.help_timeout_seconds,
        )

    def xǁScriptHelpSmokeǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        return script_help_violates(
            path,
            timeout=self.help_timeout_seconds,
        )

    def xǁScriptHelpSmokeǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        return script_help_violates(
            path,
            python=self.python_executable,
            )

    @_mutmut_mutated(mutants_xǁScriptHelpSmokeǁrun__mutmut)
    def run(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_orig(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_1(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(None) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_2(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is not None:
            report_finding(
                "dependency-unavailable",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_3(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                None,
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_4(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                None,
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_5(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                None,
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_6(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status=None,
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_7(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_8(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_9(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_10(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_11(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "XXdependency-unavailableXX",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_12(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "DEPENDENCY-UNAVAILABLE",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_13(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                "XX.XX",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_14(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="XXerrorXX",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_15(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="ERROR",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_16(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(None)
            return 2
        return super().run()

    def xǁScriptHelpSmokeǁrun__mutmut_17(self) -> int:
        """Reject an unavailable configured interpreter as structured evidence."""
        if shutil.which(self.python_executable) is None:
            report_finding(
                "dependency-unavailable",
                ".",
                f"required interpreter unavailable: {self.python_executable}",
                status="error",
            )
            print(f"ERROR script-help-smoke: required interpreter unavailable: {self.python_executable}")
            return 3
        return super().run()

mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['_mutmut_orig'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_1'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_2'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_3'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_4'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_5'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_6'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_7'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_8'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_9'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_10'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_11'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_12'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_13'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_14'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_15'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_16'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_17'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfrom_config__mutmut['xǁScriptHelpSmokeǁfrom_config__mutmut_18'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfrom_config__mutmut_18 # type: ignore # mutmut generated

mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['_mutmut_orig'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_1'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_2'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_3'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_3 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_4'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_4 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_5'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_5 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_6'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_6 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_7'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_7 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_8'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_8 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_9'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_9 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_10'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_10 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_11'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_11 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_12'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_12 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁis_in_scope__mutmut['xǁScriptHelpSmokeǁis_in_scope__mutmut_13'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁis_in_scope__mutmut_13 # type: ignore # mutmut generated

mutants_xǁScriptHelpSmokeǁfile_has_violation__mutmut['_mutmut_orig'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfile_has_violation__mutmut['xǁScriptHelpSmokeǁfile_has_violation__mutmut_1'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfile_has_violation__mutmut['xǁScriptHelpSmokeǁfile_has_violation__mutmut_2'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfile_has_violation__mutmut['xǁScriptHelpSmokeǁfile_has_violation__mutmut_3'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfile_has_violation__mutmut['xǁScriptHelpSmokeǁfile_has_violation__mutmut_4'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfile_has_violation__mutmut['xǁScriptHelpSmokeǁfile_has_violation__mutmut_5'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁfile_has_violation__mutmut['xǁScriptHelpSmokeǁfile_has_violation__mutmut_6'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated

mutants_xǁScriptHelpSmokeǁrun__mutmut['_mutmut_orig'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_1'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_2'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_3'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_4'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_5'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_6'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_7'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_8'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_9'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_10'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_11'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_12'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_13'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_14'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_15'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_16'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁScriptHelpSmokeǁrun__mutmut['xǁScriptHelpSmokeǁrun__mutmut_17'] = ScriptHelpSmoke.xǁScriptHelpSmokeǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ScriptHelpSmoke:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ScriptHelpSmoke.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ScriptHelpSmoke:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ScriptHelpSmoke.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ScriptHelpSmoke:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ScriptHelpSmoke.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ScriptHelpSmoke:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ScriptHelpSmoke.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ScriptHelpSmoke:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ScriptHelpSmoke.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> ScriptHelpSmoke:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return ScriptHelpSmoke.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ScriptHelpSmoke, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ScriptHelpSmoke, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ScriptHelpSmoke, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(ScriptHelpSmoke, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys as _sys

    _sys.exit(main())
