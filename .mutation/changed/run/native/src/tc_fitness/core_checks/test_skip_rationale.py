"""CORE check: test-skip-rationale — every skip mechanism carries a reason.

A silently-skipping test is a worse signal than a missing test: it looks
present, but never runs. This rule walks each in-scope test module via the
AST and flags any skip mechanism that lacks a documented rationale:

* ``@pytest.mark.skip`` / ``skipif`` / ``xfail`` MUST take a non-empty
  ``reason=`` kwarg (the bare attribute form fails).
* ``pytest.importorskip("X")`` MUST carry a ``reason=`` kwarg, an immediately
  preceding ``#`` comment block (within ``IMPORTORSKIP_COMMENT_LOOKBACK``
  lines, no blank gap), OR a same-line trailing ``#`` comment.
* A bare ``pytestmark = pytest.mark.skip`` module-level assignment fails too.

Ported from tc-agent-zone ``scripts/checks/test_skip_rationale.py`` (itself
kairix F11) and re-expressed as a configurable, repo-agnostic rule: the scan
roots (typically ``tests``) and file extensions arrive from the consumer's
``[tool.tc_fitness]`` config — NO repo paths are baked in. The only intrinsic
constant is the import-or-skip comment look-back window, which is the rule's
own shape and overridable.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: How many lines above an ``importorskip`` call to scan for a ``#`` comment.
#: The rule's own shape (not repo identity) — overridable via config.
DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK = 3

#: The skip decorators that require a ``reason=`` kwarg.
_REASON_REQUIRED_MARKS = ("skip", "skipif", "xfail")

REMEDIATION = _remediation(
    fix=(
        'add a non-empty reason="<why this skip is correct>" kwarg to every '
        "skip / skipif / xfail decorator, and either a reason= kwarg or an "
        "immediately-preceding # comment to every importorskip call. If the "
        "test is genuinely broken, delete the skip and fix the underlying "
        "issue instead -- a silent skip looks present but never runs."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.test_skip_rationale",
    passing='@pytest.mark.skip(reason="re-enabled once the upstream fix lands")',
    forbidden="@pytest.mark.skip  # bare -- no reason, silently never runs",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__pytest_import_names__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__pytest_import_names__mutmut)
def _pytest_import_names(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_orig(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_1(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = None
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_2(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = None
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_3(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_4(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(None):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_5(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(None)
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_6(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname and alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_7(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name != "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_8(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "XXpytestXX")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_9(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "PYTEST")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_10(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) or node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_11(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module != "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_12(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "XXpytestXX":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_13(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "PYTEST":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_14(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name != "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_15(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "XXmarkXX":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_16(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "MARK":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_17(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(None)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_18(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname and alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_19(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name != "importorskip":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_20(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "XXimportorskipXX":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_21(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "IMPORTORSKIP":
                    importorskip_names.add(alias.asname or alias.name)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_22(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(None)
    return pytest_names, mark_names, importorskip_names


def x__pytest_import_names__mutmut_23(tree: ast.AST) -> tuple[set[str], set[str], set[str]]:
    """Return module, mark, and importorskip aliases explicitly imported from pytest."""
    pytest_names: set[str] = set()
    mark_names: set[str] = set()
    importorskip_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            pytest_names.update(alias.asname or alias.name for alias in node.names if alias.name == "pytest")
        elif isinstance(node, ast.ImportFrom) and node.module == "pytest":
            for alias in node.names:
                if alias.name == "mark":
                    mark_names.add(alias.asname or alias.name)
                elif alias.name == "importorskip":
                    importorskip_names.add(alias.asname and alias.name)
    return pytest_names, mark_names, importorskip_names

mutants_x__pytest_import_names__mutmut['_mutmut_orig'] = x__pytest_import_names__mutmut_orig # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_1'] = x__pytest_import_names__mutmut_1 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_2'] = x__pytest_import_names__mutmut_2 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_3'] = x__pytest_import_names__mutmut_3 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_4'] = x__pytest_import_names__mutmut_4 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_5'] = x__pytest_import_names__mutmut_5 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_6'] = x__pytest_import_names__mutmut_6 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_7'] = x__pytest_import_names__mutmut_7 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_8'] = x__pytest_import_names__mutmut_8 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_9'] = x__pytest_import_names__mutmut_9 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_10'] = x__pytest_import_names__mutmut_10 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_11'] = x__pytest_import_names__mutmut_11 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_12'] = x__pytest_import_names__mutmut_12 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_13'] = x__pytest_import_names__mutmut_13 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_14'] = x__pytest_import_names__mutmut_14 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_15'] = x__pytest_import_names__mutmut_15 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_16'] = x__pytest_import_names__mutmut_16 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_17'] = x__pytest_import_names__mutmut_17 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_18'] = x__pytest_import_names__mutmut_18 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_19'] = x__pytest_import_names__mutmut_19 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_20'] = x__pytest_import_names__mutmut_20 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_21'] = x__pytest_import_names__mutmut_21 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_22'] = x__pytest_import_names__mutmut_22 # type: ignore # mutmut generated
mutants_x__pytest_import_names__mutmut['x__pytest_import_names__mutmut_23'] = x__pytest_import_names__mutmut_23 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_pytest_mark__mutmut)
def _is_pytest_mark(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_orig(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_1(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = None
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_2(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) or target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_3(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr != mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_4(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = None
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_5(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) or parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_6(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id not in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_7(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark"
            and isinstance(parent.value, ast.Name) or parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_8(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark" or isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_9(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute) or parent.attr == "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_10(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr != "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_11(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "XXmarkXX"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_12(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "MARK"
            and isinstance(parent.value, ast.Name)
            and parent.value.id in pytest_names
        ):
            return decorator
    return None


def x__is_pytest_mark__mutmut_13(
    decorator: ast.expr,
    mark_name: str,
    pytest_names: set[str],
    mark_names: set[str],
) -> ast.expr | None:
    """Return ``decorator`` if it is a ``pytest.mark.<mark_name>`` reference."""
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Attribute) and target.attr == mark_name:
        parent = target.value
        if isinstance(parent, ast.Name) and parent.id in mark_names:
            return decorator
        if (
            isinstance(parent, ast.Attribute)
            and parent.attr == "mark"
            and isinstance(parent.value, ast.Name)
            and parent.value.id not in pytest_names
        ):
            return decorator
    return None

mutants_x__is_pytest_mark__mutmut['_mutmut_orig'] = x__is_pytest_mark__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_1'] = x__is_pytest_mark__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_2'] = x__is_pytest_mark__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_3'] = x__is_pytest_mark__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_4'] = x__is_pytest_mark__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_5'] = x__is_pytest_mark__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_6'] = x__is_pytest_mark__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_7'] = x__is_pytest_mark__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_8'] = x__is_pytest_mark__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_9'] = x__is_pytest_mark__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_10'] = x__is_pytest_mark__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_11'] = x__is_pytest_mark__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_12'] = x__is_pytest_mark__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_pytest_mark__mutmut['x__is_pytest_mark__mutmut_13'] = x__is_pytest_mark__mutmut_13 # type: ignore # mutmut generated
mutants_x__has_reason_kwarg__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_reason_kwarg__mutmut)
def _has_reason_kwarg(call: ast.Call) -> bool:
    return any(
        kw.arg == "reason"
        and isinstance(kw.value, ast.Constant)
        and isinstance(kw.value.value, str)
        and kw.value.value.strip()
        for kw in call.keywords
    )


def x__has_reason_kwarg__mutmut_orig(call: ast.Call) -> bool:
    return any(
        kw.arg == "reason"
        and isinstance(kw.value, ast.Constant)
        and isinstance(kw.value.value, str)
        and kw.value.value.strip()
        for kw in call.keywords
    )


def x__has_reason_kwarg__mutmut_1(call: ast.Call) -> bool:
    return any(
        None
    )


def x__has_reason_kwarg__mutmut_2(call: ast.Call) -> bool:
    return any(
        kw.arg == "reason"
        and isinstance(kw.value, ast.Constant)
        and isinstance(kw.value.value, str) or kw.value.value.strip()
        for kw in call.keywords
    )


def x__has_reason_kwarg__mutmut_3(call: ast.Call) -> bool:
    return any(
        kw.arg == "reason"
        and isinstance(kw.value, ast.Constant) or isinstance(kw.value.value, str)
        and kw.value.value.strip()
        for kw in call.keywords
    )


def x__has_reason_kwarg__mutmut_4(call: ast.Call) -> bool:
    return any(
        kw.arg == "reason" or isinstance(kw.value, ast.Constant)
        and isinstance(kw.value.value, str)
        and kw.value.value.strip()
        for kw in call.keywords
    )


def x__has_reason_kwarg__mutmut_5(call: ast.Call) -> bool:
    return any(
        kw.arg != "reason"
        and isinstance(kw.value, ast.Constant)
        and isinstance(kw.value.value, str)
        and kw.value.value.strip()
        for kw in call.keywords
    )


def x__has_reason_kwarg__mutmut_6(call: ast.Call) -> bool:
    return any(
        kw.arg == "XXreasonXX"
        and isinstance(kw.value, ast.Constant)
        and isinstance(kw.value.value, str)
        and kw.value.value.strip()
        for kw in call.keywords
    )


def x__has_reason_kwarg__mutmut_7(call: ast.Call) -> bool:
    return any(
        kw.arg == "REASON"
        and isinstance(kw.value, ast.Constant)
        and isinstance(kw.value.value, str)
        and kw.value.value.strip()
        for kw in call.keywords
    )

mutants_x__has_reason_kwarg__mutmut['_mutmut_orig'] = x__has_reason_kwarg__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_reason_kwarg__mutmut['x__has_reason_kwarg__mutmut_1'] = x__has_reason_kwarg__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_reason_kwarg__mutmut['x__has_reason_kwarg__mutmut_2'] = x__has_reason_kwarg__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_reason_kwarg__mutmut['x__has_reason_kwarg__mutmut_3'] = x__has_reason_kwarg__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_reason_kwarg__mutmut['x__has_reason_kwarg__mutmut_4'] = x__has_reason_kwarg__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_reason_kwarg__mutmut['x__has_reason_kwarg__mutmut_5'] = x__has_reason_kwarg__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_reason_kwarg__mutmut['x__has_reason_kwarg__mutmut_6'] = x__has_reason_kwarg__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_reason_kwarg__mutmut['x__has_reason_kwarg__mutmut_7'] = x__has_reason_kwarg__mutmut_7 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__decorator_violates__mutmut)
def _decorator_violates(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_orig(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_1(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = None
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_2(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(None, mark_name, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_3(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, None, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_4(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, None, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_5(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, None)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_6(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(mark_name, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_7(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_8(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_9(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, )
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_10(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, mark_names)
        if match is not None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_11(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, mark_names)
        if match is None:
            break
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_12(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, mark_names)
        if match is None:
            continue
        if isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_13(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return False
        if not _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_14(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if _has_reason_kwarg(match):
            return True
    return False


def x__decorator_violates__mutmut_15(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(None):
            return True
    return False


def x__decorator_violates__mutmut_16(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return False
    return False


def x__decorator_violates__mutmut_17(
    decorator: ast.expr,
    pytest_names: set[str],
    mark_names: set[str],
) -> bool:
    for mark_name in _REASON_REQUIRED_MARKS:
        match = _is_pytest_mark(decorator, mark_name, pytest_names, mark_names)
        if match is None:
            continue
        if not isinstance(match, ast.Call):
            return True
        if not _has_reason_kwarg(match):
            return True
    return True

mutants_x__decorator_violates__mutmut['_mutmut_orig'] = x__decorator_violates__mutmut_orig # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_1'] = x__decorator_violates__mutmut_1 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_2'] = x__decorator_violates__mutmut_2 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_3'] = x__decorator_violates__mutmut_3 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_4'] = x__decorator_violates__mutmut_4 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_5'] = x__decorator_violates__mutmut_5 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_6'] = x__decorator_violates__mutmut_6 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_7'] = x__decorator_violates__mutmut_7 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_8'] = x__decorator_violates__mutmut_8 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_9'] = x__decorator_violates__mutmut_9 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_10'] = x__decorator_violates__mutmut_10 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_11'] = x__decorator_violates__mutmut_11 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_12'] = x__decorator_violates__mutmut_12 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_13'] = x__decorator_violates__mutmut_13 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_14'] = x__decorator_violates__mutmut_14 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_15'] = x__decorator_violates__mutmut_15 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_16'] = x__decorator_violates__mutmut_16 # type: ignore # mutmut generated
mutants_x__decorator_violates__mutmut['x__decorator_violates__mutmut_17'] = x__decorator_violates__mutmut_17 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_importorskip__mutmut)
def _is_importorskip(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr == "importorskip":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_orig(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr == "importorskip":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_1(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr == "importorskip":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_2(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = None
    if isinstance(target, ast.Attribute) and target.attr == "importorskip":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_3(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) or target.attr == "importorskip":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_4(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr != "importorskip":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_5(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr == "XXimportorskipXX":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_6(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr == "IMPORTORSKIP":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_7(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr == "importorskip":
        inner = None
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_8(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr == "importorskip":
        inner = target.value
        if isinstance(inner, ast.Name) or inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_9(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr == "importorskip":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id not in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_10(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr == "importorskip":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) or target.id in importorskip_names:
        return node
    return None


def x__is_importorskip__mutmut_11(
    node: ast.expr,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if not isinstance(node, ast.Call):
        return None
    target = node.func
    if isinstance(target, ast.Attribute) and target.attr == "importorskip":
        inner = target.value
        if isinstance(inner, ast.Name) and inner.id in pytest_names:
            return node
    if isinstance(target, ast.Name) and target.id not in importorskip_names:
        return node
    return None

mutants_x__is_importorskip__mutmut['_mutmut_orig'] = x__is_importorskip__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_1'] = x__is_importorskip__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_2'] = x__is_importorskip__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_3'] = x__is_importorskip__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_4'] = x__is_importorskip__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_5'] = x__is_importorskip__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_6'] = x__is_importorskip__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_7'] = x__is_importorskip__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_8'] = x__is_importorskip__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_9'] = x__is_importorskip__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_10'] = x__is_importorskip__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_importorskip__mutmut['x__is_importorskip__mutmut_11'] = x__is_importorskip__mutmut_11 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__importorskip_has_rationale__mutmut)
def _importorskip_has_rationale(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_orig(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_1(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(None):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_2(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return False
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_3(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = None
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_4(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno + 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_5(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 2
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_6(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = None
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_7(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "XX#XX" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_8(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" not in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_9(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = None
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_10(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split(None, 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_11(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", None)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_12(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split(1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_13(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", )[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_14(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.rsplit("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_15(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("XX#XX", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_16(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 2)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_17(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[2].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_18(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return False
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_19(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(None, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_20(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, None):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_21(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_22(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, ):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_23(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(2, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_24(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback - 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_25(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 2):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_26(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = None
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_27(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx + offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_28(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx <= 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_29(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 1:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_30(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return True
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_31(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = None
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_32(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped != "":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_33(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "XXXX":
            return False
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_34(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return True
        if stripped.startswith("#"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_35(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith(None):
            return True
    return False


def x__importorskip_has_rationale__mutmut_36(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("XX#XX"):
            return True
    return False


def x__importorskip_has_rationale__mutmut_37(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return False
    return False


def x__importorskip_has_rationale__mutmut_38(call: ast.Call, source_lines: list[str], lookback: int) -> bool:
    if _has_reason_kwarg(call):
        return True
    line_idx = call.lineno - 1
    line = source_lines[line_idx]
    if "#" in line:
        after_hash = line.split("#", 1)[1].strip()
        if after_hash:
            return True
    for offset in range(1, lookback + 1):
        prev_idx = line_idx - offset
        if prev_idx < 0:
            return False
        stripped = source_lines[prev_idx].strip()
        if stripped == "":
            return False
        if stripped.startswith("#"):
            return True
    return True

mutants_x__importorskip_has_rationale__mutmut['_mutmut_orig'] = x__importorskip_has_rationale__mutmut_orig # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_1'] = x__importorskip_has_rationale__mutmut_1 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_2'] = x__importorskip_has_rationale__mutmut_2 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_3'] = x__importorskip_has_rationale__mutmut_3 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_4'] = x__importorskip_has_rationale__mutmut_4 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_5'] = x__importorskip_has_rationale__mutmut_5 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_6'] = x__importorskip_has_rationale__mutmut_6 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_7'] = x__importorskip_has_rationale__mutmut_7 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_8'] = x__importorskip_has_rationale__mutmut_8 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_9'] = x__importorskip_has_rationale__mutmut_9 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_10'] = x__importorskip_has_rationale__mutmut_10 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_11'] = x__importorskip_has_rationale__mutmut_11 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_12'] = x__importorskip_has_rationale__mutmut_12 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_13'] = x__importorskip_has_rationale__mutmut_13 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_14'] = x__importorskip_has_rationale__mutmut_14 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_15'] = x__importorskip_has_rationale__mutmut_15 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_16'] = x__importorskip_has_rationale__mutmut_16 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_17'] = x__importorskip_has_rationale__mutmut_17 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_18'] = x__importorskip_has_rationale__mutmut_18 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_19'] = x__importorskip_has_rationale__mutmut_19 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_20'] = x__importorskip_has_rationale__mutmut_20 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_21'] = x__importorskip_has_rationale__mutmut_21 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_22'] = x__importorskip_has_rationale__mutmut_22 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_23'] = x__importorskip_has_rationale__mutmut_23 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_24'] = x__importorskip_has_rationale__mutmut_24 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_25'] = x__importorskip_has_rationale__mutmut_25 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_26'] = x__importorskip_has_rationale__mutmut_26 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_27'] = x__importorskip_has_rationale__mutmut_27 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_28'] = x__importorskip_has_rationale__mutmut_28 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_29'] = x__importorskip_has_rationale__mutmut_29 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_30'] = x__importorskip_has_rationale__mutmut_30 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_31'] = x__importorskip_has_rationale__mutmut_31 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_32'] = x__importorskip_has_rationale__mutmut_32 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_33'] = x__importorskip_has_rationale__mutmut_33 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_34'] = x__importorskip_has_rationale__mutmut_34 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_35'] = x__importorskip_has_rationale__mutmut_35 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_36'] = x__importorskip_has_rationale__mutmut_36 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_37'] = x__importorskip_has_rationale__mutmut_37 # type: ignore # mutmut generated
mutants_x__importorskip_has_rationale__mutmut['x__importorskip_has_rationale__mutmut_38'] = x__importorskip_has_rationale__mutmut_38 # type: ignore # mutmut generated
mutants_x__pytestmark_candidates__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__pytestmark_candidates__mutmut)
def _pytestmark_candidates(value: ast.expr) -> list[ast.expr]:
    if isinstance(value, ast.List | ast.Tuple):
        return list(value.elts)
    return [value]


def x__pytestmark_candidates__mutmut_orig(value: ast.expr) -> list[ast.expr]:
    if isinstance(value, ast.List | ast.Tuple):
        return list(value.elts)
    return [value]


def x__pytestmark_candidates__mutmut_1(value: ast.expr) -> list[ast.expr]:
    if isinstance(value, ast.List | ast.Tuple):
        return list(None)
    return [value]

mutants_x__pytestmark_candidates__mutmut['_mutmut_orig'] = x__pytestmark_candidates__mutmut_orig # type: ignore # mutmut generated
mutants_x__pytestmark_candidates__mutmut['x__pytestmark_candidates__mutmut_1'] = x__pytestmark_candidates__mutmut_1 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__pytestmark_violations__mutmut)
def _pytestmark_violations(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_orig(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_1(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = None
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_2(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = None
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_3(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = None
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_4(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = None
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_5(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = None
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_6(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_7(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) or target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_8(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id != "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_9(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "XXpytestmarkXX"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_10(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "PYTESTMARK"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_11(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            break
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_12(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is not None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_13(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            break
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_14(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(None):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_15(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(None, pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_16(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, None, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_17(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, None):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_18(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(pytest_names, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_19(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, mark_names):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_20(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, ):
                out.append(candidate.lineno)
    return out


def x__pytestmark_violations__mutmut_21(node: ast.AST, pytest_names: set[str], mark_names: set[str]) -> list[int]:
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = node.targets
        value: ast.expr | None = node.value
    elif isinstance(node, ast.AnnAssign):
        targets = [node.target]
        value = node.value
    else:
        return []
    out: list[int] = []
    for target in targets:
        if not (isinstance(target, ast.Name) and target.id == "pytestmark"):
            continue
        if value is None:
            continue
        for candidate in _pytestmark_candidates(value):
            if _decorator_violates(candidate, pytest_names, mark_names):
                out.append(None)
    return out

mutants_x__pytestmark_violations__mutmut['_mutmut_orig'] = x__pytestmark_violations__mutmut_orig # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_1'] = x__pytestmark_violations__mutmut_1 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_2'] = x__pytestmark_violations__mutmut_2 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_3'] = x__pytestmark_violations__mutmut_3 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_4'] = x__pytestmark_violations__mutmut_4 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_5'] = x__pytestmark_violations__mutmut_5 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_6'] = x__pytestmark_violations__mutmut_6 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_7'] = x__pytestmark_violations__mutmut_7 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_8'] = x__pytestmark_violations__mutmut_8 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_9'] = x__pytestmark_violations__mutmut_9 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_10'] = x__pytestmark_violations__mutmut_10 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_11'] = x__pytestmark_violations__mutmut_11 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_12'] = x__pytestmark_violations__mutmut_12 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_13'] = x__pytestmark_violations__mutmut_13 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_14'] = x__pytestmark_violations__mutmut_14 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_15'] = x__pytestmark_violations__mutmut_15 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_16'] = x__pytestmark_violations__mutmut_16 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_17'] = x__pytestmark_violations__mutmut_17 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_18'] = x__pytestmark_violations__mutmut_18 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_19'] = x__pytestmark_violations__mutmut_19 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_20'] = x__pytestmark_violations__mutmut_20 # type: ignore # mutmut generated
mutants_x__pytestmark_violations__mutmut['x__pytestmark_violations__mutmut_21'] = x__pytestmark_violations__mutmut_21 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__importorskip_call__mutmut)
def _importorskip_call(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_orig(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_1(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(None, pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_2(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, None, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_3(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, None)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_4(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_5(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_6(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, )
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_7(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is None:
            return _is_importorskip(node.value, pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_8(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(None, pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_9(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, None, importorskip_names)
    return None


def x__importorskip_call__mutmut_10(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, pytest_names, None)
    return None


def x__importorskip_call__mutmut_11(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(pytest_names, importorskip_names)
    return None


def x__importorskip_call__mutmut_12(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, importorskip_names)
    return None


def x__importorskip_call__mutmut_13(
    node: ast.AST,
    pytest_names: set[str],
    importorskip_names: set[str],
) -> ast.Call | None:
    if isinstance(node, ast.Expr):
        return _is_importorskip(node.value, pytest_names, importorskip_names)
    if isinstance(node, ast.Assign | ast.AnnAssign):
        if node.value is not None:
            return _is_importorskip(node.value, pytest_names, )
    return None

mutants_x__importorskip_call__mutmut['_mutmut_orig'] = x__importorskip_call__mutmut_orig # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_1'] = x__importorskip_call__mutmut_1 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_2'] = x__importorskip_call__mutmut_2 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_3'] = x__importorskip_call__mutmut_3 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_4'] = x__importorskip_call__mutmut_4 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_5'] = x__importorskip_call__mutmut_5 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_6'] = x__importorskip_call__mutmut_6 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_7'] = x__importorskip_call__mutmut_7 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_8'] = x__importorskip_call__mutmut_8 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_9'] = x__importorskip_call__mutmut_9 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_10'] = x__importorskip_call__mutmut_10 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_11'] = x__importorskip_call__mutmut_11 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_12'] = x__importorskip_call__mutmut_12 # type: ignore # mutmut generated
mutants_x__importorskip_call__mutmut['x__importorskip_call__mutmut_13'] = x__importorskip_call__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_has_skip_without_reason__mutmut)
def file_has_skip_without_reason(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_orig(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_1(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = None
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_2(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding=None)
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_3(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="XXutf-8XX")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_4(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="UTF-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_5(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_6(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_7(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_8(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_9(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_10(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_11(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_12(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = None
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_13(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_14(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(None)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_15(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(None):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_16(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) or any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_17(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            None
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_18(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(None, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_19(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, None, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_20(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, None) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_21(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_22(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_23(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, ) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_24(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return False
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_25(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(None, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_26(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, None, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_27(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, None):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_28(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_29(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_30(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, ):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_31(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return False
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_32(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = None
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_33(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(None, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_34(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, None, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_35(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, None)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_36(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_37(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_38(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, )
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_39(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None or not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_40(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_41(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_42(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(None, source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_43(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, None, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_44(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, None):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_45(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(source_lines, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_46(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, importorskip_lookback):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_47(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, ):
            return True
    return False


def x_file_has_skip_without_reason__mutmut_48(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return False
    return False


def x_file_has_skip_without_reason__mutmut_49(path: Path, *, importorskip_lookback: int) -> bool:
    """True iff ``path`` holds any skip mechanism that lacks a rationale.

    Pure helper (the detection core) so tests assert on it directly: parses
    the module, then checks every skip/skipif/xfail decorator, every bare
    ``pytestmark`` assignment, and every ``importorskip`` call. A syntax /
    decode / read error is a violation because the configured source could not
    be evaluated.
    """
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    source_lines = source.splitlines()
    pytest_names, mark_names, importorskip_names = _pytest_import_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and any(
            _decorator_violates(decorator, pytest_names, mark_names) for decorator in node.decorator_list
        ):
            return True
        if _pytestmark_violations(node, pytest_names, mark_names):
            return True
        call = _importorskip_call(node, pytest_names, importorskip_names)
        if call is not None and not _importorskip_has_rationale(call, source_lines, importorskip_lookback):
            return True
    return True

mutants_x_file_has_skip_without_reason__mutmut['_mutmut_orig'] = x_file_has_skip_without_reason__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_1'] = x_file_has_skip_without_reason__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_2'] = x_file_has_skip_without_reason__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_3'] = x_file_has_skip_without_reason__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_4'] = x_file_has_skip_without_reason__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_5'] = x_file_has_skip_without_reason__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_6'] = x_file_has_skip_without_reason__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_7'] = x_file_has_skip_without_reason__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_8'] = x_file_has_skip_without_reason__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_9'] = x_file_has_skip_without_reason__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_10'] = x_file_has_skip_without_reason__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_11'] = x_file_has_skip_without_reason__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_12'] = x_file_has_skip_without_reason__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_13'] = x_file_has_skip_without_reason__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_14'] = x_file_has_skip_without_reason__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_15'] = x_file_has_skip_without_reason__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_16'] = x_file_has_skip_without_reason__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_17'] = x_file_has_skip_without_reason__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_18'] = x_file_has_skip_without_reason__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_19'] = x_file_has_skip_without_reason__mutmut_19 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_20'] = x_file_has_skip_without_reason__mutmut_20 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_21'] = x_file_has_skip_without_reason__mutmut_21 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_22'] = x_file_has_skip_without_reason__mutmut_22 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_23'] = x_file_has_skip_without_reason__mutmut_23 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_24'] = x_file_has_skip_without_reason__mutmut_24 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_25'] = x_file_has_skip_without_reason__mutmut_25 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_26'] = x_file_has_skip_without_reason__mutmut_26 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_27'] = x_file_has_skip_without_reason__mutmut_27 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_28'] = x_file_has_skip_without_reason__mutmut_28 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_29'] = x_file_has_skip_without_reason__mutmut_29 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_30'] = x_file_has_skip_without_reason__mutmut_30 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_31'] = x_file_has_skip_without_reason__mutmut_31 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_32'] = x_file_has_skip_without_reason__mutmut_32 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_33'] = x_file_has_skip_without_reason__mutmut_33 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_34'] = x_file_has_skip_without_reason__mutmut_34 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_35'] = x_file_has_skip_without_reason__mutmut_35 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_36'] = x_file_has_skip_without_reason__mutmut_36 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_37'] = x_file_has_skip_without_reason__mutmut_37 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_38'] = x_file_has_skip_without_reason__mutmut_38 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_39'] = x_file_has_skip_without_reason__mutmut_39 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_40'] = x_file_has_skip_without_reason__mutmut_40 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_41'] = x_file_has_skip_without_reason__mutmut_41 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_42'] = x_file_has_skip_without_reason__mutmut_42 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_43'] = x_file_has_skip_without_reason__mutmut_43 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_44'] = x_file_has_skip_without_reason__mutmut_44 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_45'] = x_file_has_skip_without_reason__mutmut_45 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_46'] = x_file_has_skip_without_reason__mutmut_46 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_47'] = x_file_has_skip_without_reason__mutmut_47 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_48'] = x_file_has_skip_without_reason__mutmut_48 # type: ignore # mutmut generated
mutants_x_file_has_skip_without_reason__mutmut['x_file_has_skip_without_reason__mutmut_49'] = x_file_has_skip_without_reason__mutmut_49 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁTestSkipRationaleǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class TestSkipRationale(FitnessRule):
    """Flags test files with an undocumented skip/skipif/xfail/importorskip."""

    #: Tell pytest this is a rule class, not a test class (the ``Test`` prefix
    #: would otherwise trigger collection).
    __test__ = False

    name = "test-skip-rationale"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knob — the importorskip comment look-back window.
    importorskip_lookback: int = DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK

    @classmethod
    @_mutmut_mutated(mutants_xǁTestSkipRationaleǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("importorskip_lookback", DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("importorskip_lookback", DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = None
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("importorskip_lookback", DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("importorskip_lookback", DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("importorskip_lookback", DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("importorskip_lookback", DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, )
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("importorskip_lookback", DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = None
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            None
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get(None, DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("importorskip_lookback", None)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get(DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("importorskip_lookback", )
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("XXimportorskip_lookbackXX", DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @classmethod
    def xǁTestSkipRationaleǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> TestSkipRationale:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, TestSkipRationale)  # noqa: S101  # narrowing for mypy
        rule.importorskip_lookback = int(
            config.get("IMPORTORSKIP_LOOKBACK", DEFAULT_IMPORTORSKIP_COMMENT_LOOKBACK)
        )
        return rule

    @_mutmut_mutated(mutants_xǁTestSkipRationaleǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_has_skip_without_reason(path, importorskip_lookback=self.importorskip_lookback)

    def xǁTestSkipRationaleǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_has_skip_without_reason(path, importorskip_lookback=self.importorskip_lookback)

    def xǁTestSkipRationaleǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_has_skip_without_reason(None, importorskip_lookback=self.importorskip_lookback)

    def xǁTestSkipRationaleǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_has_skip_without_reason(path, importorskip_lookback=None)

    def xǁTestSkipRationaleǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_has_skip_without_reason(importorskip_lookback=self.importorskip_lookback)

    def xǁTestSkipRationaleǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_has_skip_without_reason(path, )

mutants_xǁTestSkipRationaleǁfrom_config__mutmut['_mutmut_orig'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_1'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_2'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_3'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_4'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_5'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_6'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_7'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_8'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_9'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_10'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_11'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_12'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfrom_config__mutmut['xǁTestSkipRationaleǁfrom_config__mutmut_13'] = TestSkipRationale.xǁTestSkipRationaleǁfrom_config__mutmut_13 # type: ignore # mutmut generated

mutants_xǁTestSkipRationaleǁfile_has_violation__mutmut['_mutmut_orig'] = TestSkipRationale.xǁTestSkipRationaleǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfile_has_violation__mutmut['xǁTestSkipRationaleǁfile_has_violation__mutmut_1'] = TestSkipRationale.xǁTestSkipRationaleǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfile_has_violation__mutmut['xǁTestSkipRationaleǁfile_has_violation__mutmut_2'] = TestSkipRationale.xǁTestSkipRationaleǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfile_has_violation__mutmut['xǁTestSkipRationaleǁfile_has_violation__mutmut_3'] = TestSkipRationale.xǁTestSkipRationaleǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁTestSkipRationaleǁfile_has_violation__mutmut['xǁTestSkipRationaleǁfile_has_violation__mutmut_4'] = TestSkipRationale.xǁTestSkipRationaleǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> TestSkipRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return TestSkipRationale.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> TestSkipRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return TestSkipRationale.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> TestSkipRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return TestSkipRationale.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> TestSkipRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return TestSkipRationale.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> TestSkipRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return TestSkipRationale.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> TestSkipRationale:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return TestSkipRationale.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(TestSkipRationale, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(TestSkipRationale, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(TestSkipRationale, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(TestSkipRationale, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
