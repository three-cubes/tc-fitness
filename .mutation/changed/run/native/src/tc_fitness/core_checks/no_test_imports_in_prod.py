"""CORE check: no-test-imports-in-prod — production never imports the test tree.

Production code MUST NOT import from the test package (``from tests.x import``
/ ``import tests``). The test tree is not shipped in the published wheel, so
any such import works in a local checkout (where the repo root is on
``sys.path`` via the test runner) but raises ``ModuleNotFoundError`` the
moment an end user installs the package and runs it.

Detection (AST over each in-scope production file):

* ``ast.ImportFrom`` whose ``module`` is a forbidden root or a dotted child.
* ``ast.Import`` where any alias name is a forbidden root or a dotted child.

The legitimate way to share a fake-like default is to ship it in the
production package itself (e.g. an ``InMemoryX`` / ``NullX``); the test tree
is for tests only -- by convention and by what the wheel actually ships.

Ported from kairix ``scripts/checks/check_no_test_imports_in_prod.py`` (F24)
and re-expressed as a configurable, repo-agnostic rule: the production scan
roots and the forbidden import roots arrive from config -- NO repo package
name is baked in. The forbidden root defaults to ``tests`` (the universal
test-tree convention), overridable per consumer.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The conventional test-tree package name -- not repo identity. Overridable.
DEFAULT_FORBIDDEN_IMPORT_ROOTS: tuple[str, ...] = ("tests",)

REMEDIATION = _remediation(
    fix=(
        "move the symbol you needed out of the test tree and into the shipped "
        "package (e.g. as a NullX / InMemoryX in the relevant domain module) "
        "so it is part of the wheel. If the import is for a test seam, the "
        "production code should not carry that seam at all -- inject via a "
        "constructor argument and let the test pass the fake explicitly."
    ),
    nxt="re-run this check, then install the wheel and import the module to "
    "confirm it works with no test tree on sys.path.",
    run="python -m tc_fitness.core_checks.no_test_imports_in_prod",
    passing="from myapp.core.vector.null import NullVectorRepository",
    forbidden="from tests.fakes import FakeVectorRepository  # test tree not in wheel",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__name_is_forbidden__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__name_is_forbidden__mutmut)
def _name_is_forbidden(name: str | None, roots: tuple[str, ...]) -> bool:
    """True if ``name`` is a forbidden root or any dotted child of one."""
    if name is None:
        return False
    return any(name == root or name.startswith(f"{root}.") for root in roots)


def x__name_is_forbidden__mutmut_orig(name: str | None, roots: tuple[str, ...]) -> bool:
    """True if ``name`` is a forbidden root or any dotted child of one."""
    if name is None:
        return False
    return any(name == root or name.startswith(f"{root}.") for root in roots)


def x__name_is_forbidden__mutmut_1(name: str | None, roots: tuple[str, ...]) -> bool:
    """True if ``name`` is a forbidden root or any dotted child of one."""
    if name is not None:
        return False
    return any(name == root or name.startswith(f"{root}.") for root in roots)


def x__name_is_forbidden__mutmut_2(name: str | None, roots: tuple[str, ...]) -> bool:
    """True if ``name`` is a forbidden root or any dotted child of one."""
    if name is None:
        return True
    return any(name == root or name.startswith(f"{root}.") for root in roots)


def x__name_is_forbidden__mutmut_3(name: str | None, roots: tuple[str, ...]) -> bool:
    """True if ``name`` is a forbidden root or any dotted child of one."""
    if name is None:
        return False
    return any(None)


def x__name_is_forbidden__mutmut_4(name: str | None, roots: tuple[str, ...]) -> bool:
    """True if ``name`` is a forbidden root or any dotted child of one."""
    if name is None:
        return False
    return any(name == root and name.startswith(f"{root}.") for root in roots)


def x__name_is_forbidden__mutmut_5(name: str | None, roots: tuple[str, ...]) -> bool:
    """True if ``name`` is a forbidden root or any dotted child of one."""
    if name is None:
        return False
    return any(name != root or name.startswith(f"{root}.") for root in roots)


def x__name_is_forbidden__mutmut_6(name: str | None, roots: tuple[str, ...]) -> bool:
    """True if ``name`` is a forbidden root or any dotted child of one."""
    if name is None:
        return False
    return any(name == root or name.startswith(None) for root in roots)

mutants_x__name_is_forbidden__mutmut['_mutmut_orig'] = x__name_is_forbidden__mutmut_orig # type: ignore # mutmut generated
mutants_x__name_is_forbidden__mutmut['x__name_is_forbidden__mutmut_1'] = x__name_is_forbidden__mutmut_1 # type: ignore # mutmut generated
mutants_x__name_is_forbidden__mutmut['x__name_is_forbidden__mutmut_2'] = x__name_is_forbidden__mutmut_2 # type: ignore # mutmut generated
mutants_x__name_is_forbidden__mutmut['x__name_is_forbidden__mutmut_3'] = x__name_is_forbidden__mutmut_3 # type: ignore # mutmut generated
mutants_x__name_is_forbidden__mutmut['x__name_is_forbidden__mutmut_4'] = x__name_is_forbidden__mutmut_4 # type: ignore # mutmut generated
mutants_x__name_is_forbidden__mutmut['x__name_is_forbidden__mutmut_5'] = x__name_is_forbidden__mutmut_5 # type: ignore # mutmut generated
mutants_x__name_is_forbidden__mutmut['x__name_is_forbidden__mutmut_6'] = x__name_is_forbidden__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_imports_test_tree__mutmut)
def file_imports_test_tree(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_orig(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_1(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_2(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_3(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_4(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_5(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_6(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_7(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_8(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_9(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_10(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_11(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(None):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_12(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) or _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_13(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(None, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_14(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, None):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_15(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_16(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, ):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_17(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return False
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_18(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(None, forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_19(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, None):
                    return True
    return False


def x_file_imports_test_tree__mutmut_20(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(forbidden_roots):
                    return True
    return False


def x_file_imports_test_tree__mutmut_21(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, ):
                    return True
    return False


def x_file_imports_test_tree__mutmut_22(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return False
    return False


def x_file_imports_test_tree__mutmut_23(path: Path, *, forbidden_roots: tuple[str, ...]) -> bool:
    """True iff ``path`` imports from a forbidden (test-tree) package.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and _name_is_forbidden(node.module, forbidden_roots):
            return True
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _name_is_forbidden(alias.name, forbidden_roots):
                    return True
    return True

mutants_x_file_imports_test_tree__mutmut['_mutmut_orig'] = x_file_imports_test_tree__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_1'] = x_file_imports_test_tree__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_2'] = x_file_imports_test_tree__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_3'] = x_file_imports_test_tree__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_4'] = x_file_imports_test_tree__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_5'] = x_file_imports_test_tree__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_6'] = x_file_imports_test_tree__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_7'] = x_file_imports_test_tree__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_8'] = x_file_imports_test_tree__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_9'] = x_file_imports_test_tree__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_10'] = x_file_imports_test_tree__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_11'] = x_file_imports_test_tree__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_12'] = x_file_imports_test_tree__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_13'] = x_file_imports_test_tree__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_14'] = x_file_imports_test_tree__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_15'] = x_file_imports_test_tree__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_16'] = x_file_imports_test_tree__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_17'] = x_file_imports_test_tree__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_18'] = x_file_imports_test_tree__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_19'] = x_file_imports_test_tree__mutmut_19 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_20'] = x_file_imports_test_tree__mutmut_20 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_21'] = x_file_imports_test_tree__mutmut_21 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_22'] = x_file_imports_test_tree__mutmut_22 # type: ignore # mutmut generated
mutants_x_file_imports_test_tree__mutmut['x_file_imports_test_tree__mutmut_23'] = x_file_imports_test_tree__mutmut_23 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoTestImportsInProdǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoTestImportsInProd(FitnessRule):
    """Flags production files that import from the test tree."""

    name = "no-test-imports-in-prod"
    remediation = REMEDIATION
    extensions = (".py",)

    #: The test-tree package roots production must never import.
    forbidden_import_roots: tuple[str, ...] = DEFAULT_FORBIDDEN_IMPORT_ROOTS

    @classmethod
    @_mutmut_mutated(mutants_xǁNoTestImportsInProdǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("forbidden_import_roots")
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("forbidden_import_roots")
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = None
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("forbidden_import_roots")
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("forbidden_import_roots")
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("forbidden_import_roots")
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("forbidden_import_roots")
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, )
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("forbidden_import_roots")
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = None
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get(None)
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("XXforbidden_import_rootsXX")
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("FORBIDDEN_IMPORT_ROOTS")
        rule.forbidden_import_roots = tuple(roots) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("forbidden_import_roots")
        rule.forbidden_import_roots = None
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("forbidden_import_roots")
        rule.forbidden_import_roots = tuple(None) if roots is not None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @classmethod
    def xǁNoTestImportsInProdǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestImportsInProd:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestImportsInProd)  # noqa: S101  # narrowing for mypy
        roots = config.get("forbidden_import_roots")
        rule.forbidden_import_roots = tuple(roots) if roots is None else DEFAULT_FORBIDDEN_IMPORT_ROOTS
        return rule

    @_mutmut_mutated(mutants_xǁNoTestImportsInProdǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_imports_test_tree(path, forbidden_roots=self.forbidden_import_roots)

    def xǁNoTestImportsInProdǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_imports_test_tree(path, forbidden_roots=self.forbidden_import_roots)

    def xǁNoTestImportsInProdǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_imports_test_tree(None, forbidden_roots=self.forbidden_import_roots)

    def xǁNoTestImportsInProdǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_imports_test_tree(path, forbidden_roots=None)

    def xǁNoTestImportsInProdǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_imports_test_tree(forbidden_roots=self.forbidden_import_roots)

    def xǁNoTestImportsInProdǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_imports_test_tree(path, )

mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['_mutmut_orig'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_1'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_2'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_3'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_4'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_5'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_6'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_7'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_8'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_9'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_10'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_11'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfrom_config__mutmut['xǁNoTestImportsInProdǁfrom_config__mutmut_12'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfrom_config__mutmut_12 # type: ignore # mutmut generated

mutants_xǁNoTestImportsInProdǁfile_has_violation__mutmut['_mutmut_orig'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfile_has_violation__mutmut['xǁNoTestImportsInProdǁfile_has_violation__mutmut_1'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfile_has_violation__mutmut['xǁNoTestImportsInProdǁfile_has_violation__mutmut_2'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfile_has_violation__mutmut['xǁNoTestImportsInProdǁfile_has_violation__mutmut_3'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoTestImportsInProdǁfile_has_violation__mutmut['xǁNoTestImportsInProdǁfile_has_violation__mutmut_4'] = NoTestImportsInProd.xǁNoTestImportsInProdǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestImportsInProd:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestImportsInProd.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestImportsInProd:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestImportsInProd.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestImportsInProd:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestImportsInProd.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestImportsInProd:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestImportsInProd.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestImportsInProd:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestImportsInProd.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestImportsInProd:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoTestImportsInProd.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoTestImportsInProd, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoTestImportsInProd, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoTestImportsInProd, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoTestImportsInProd, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
