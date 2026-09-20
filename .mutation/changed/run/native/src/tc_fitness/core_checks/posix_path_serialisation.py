"""CORE check: posix_path_serialisation — repo-relative paths serialised as POSIX.

A repo-relative path stringified with ``str(path.relative_to(root))`` carries the
HOST-native separator: backslashes on Windows, forward slashes on Linux. A
generated/consumed artefact committed cross-platform and read on Linux CI then
ships ``a\\b\\c`` where the consumer expects ``a/b/c`` — a bug invisible until CI
runs on the other OS. This rule bans the OS-native ``str(...)`` idiom; the single
sanctioned form is ``.relative_to(root).as_posix()``.

Detection is AST-based: it flags any ``str(...)`` call whose argument subtree
contains a ``.relative_to(...)`` call that is NOT immediately ``.as_posix()``-
terminated. The compliant forms (``p.relative_to(r).as_posix()`` and the
redundant ``str(p.relative_to(r).as_posix())``) are not flagged.

Ported from tc-agent-zone ``scripts/checks/posix_path_serialisation.py`` and
re-expressed as a configurable, repo-agnostic rule: the scan roots, in-scope
extensions, and exempt path SEGMENTS all arrive from the consumer's
``[tool.tc_fitness]`` config — NO repo paths or globs are baked in. Domain-
intrinsic defaults (the ``.py`` extension, ``__pycache__``/``.venv`` cache
segments) are the rule's own shape, overridable via config.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: Path SEGMENTS that take a file out of scope by default — cache/build dirs and
#: test trees that legitimately stringify ephemeral OS paths. Domain-intrinsic,
#: NOT repo identity; a consumer narrows or widens this via config.
DEFAULT_EXCLUDED_SEGMENTS: tuple[str, ...] = (
    "tests",
    "test",
    "node_modules",
    ".venv",
    "__pycache__",
)

REMEDIATION = _remediation(
    fix=(
        "replace `str(path.relative_to(root))` with "
        "`path.relative_to(root).as_posix()` (or build the value from a "
        "PurePosixPath); bare str() emits OS-native separators that break "
        "Linux CI when serialised on Windows."
    ),
    nxt="re-run this check to confirm the offending line is gone.",
    run="python -m tc_fitness.core_checks.posix_path_serialisation",
    passing="rel = path.relative_to(root).as_posix()   # always forward-slash",
    forbidden="rel = str(path.relative_to(root))         # OS-native separators leak",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__compliant_relative_to_nodes__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__compliant_relative_to_nodes__mutmut)
def _compliant_relative_to_nodes(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_orig(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_1(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = None
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_2(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(None):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_3(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute) or node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_4(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call) or isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_5(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix" or isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_6(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute) or node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_7(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call) or isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_8(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr != "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_9(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "XXas_posixXX"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_10(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "AS_POSIX"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_11(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr != "relative_to"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_12(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "XXrelative_toXX"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_13(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "RELATIVE_TO"
        ):
            compliant.add(id(node.func.value))
    return compliant


def x__compliant_relative_to_nodes__mutmut_14(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(None)
    return compliant


def x__compliant_relative_to_nodes__mutmut_15(tree: ast.AST) -> set[int]:
    """Object-ids of ``relative_to(...)`` calls immediately ``.as_posix()``'d.

    ``path.relative_to(root).as_posix()`` is the sanctioned form, so the inner
    ``relative_to`` call must never be treated as a violation even inside a
    ``str(...)`` (the redundant-but-compliant ``str(p.relative_to(r).as_posix())``).
    """
    compliant: set[int] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "as_posix"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Attribute)
            and node.func.value.func.attr == "relative_to"
        ):
            compliant.add(id(None))
    return compliant

mutants_x__compliant_relative_to_nodes__mutmut['_mutmut_orig'] = x__compliant_relative_to_nodes__mutmut_orig # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_1'] = x__compliant_relative_to_nodes__mutmut_1 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_2'] = x__compliant_relative_to_nodes__mutmut_2 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_3'] = x__compliant_relative_to_nodes__mutmut_3 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_4'] = x__compliant_relative_to_nodes__mutmut_4 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_5'] = x__compliant_relative_to_nodes__mutmut_5 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_6'] = x__compliant_relative_to_nodes__mutmut_6 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_7'] = x__compliant_relative_to_nodes__mutmut_7 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_8'] = x__compliant_relative_to_nodes__mutmut_8 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_9'] = x__compliant_relative_to_nodes__mutmut_9 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_10'] = x__compliant_relative_to_nodes__mutmut_10 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_11'] = x__compliant_relative_to_nodes__mutmut_11 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_12'] = x__compliant_relative_to_nodes__mutmut_12 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_13'] = x__compliant_relative_to_nodes__mutmut_13 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_14'] = x__compliant_relative_to_nodes__mutmut_14 # type: ignore # mutmut generated
mutants_x__compliant_relative_to_nodes__mutmut['x__compliant_relative_to_nodes__mutmut_15'] = x__compliant_relative_to_nodes__mutmut_15 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_uncompliant_relative_to__mutmut)
def _has_uncompliant_relative_to(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "relative_to"
            and id(child) not in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_orig(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "relative_to"
            and id(child) not in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_1(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(None):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "relative_to"
            and id(child) not in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_2(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "relative_to" or id(child) not in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_3(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute) or child.func.attr == "relative_to"
            and id(child) not in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_4(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call) or isinstance(child.func, ast.Attribute)
            and child.func.attr == "relative_to"
            and id(child) not in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_5(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr != "relative_to"
            and id(child) not in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_6(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "XXrelative_toXX"
            and id(child) not in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_7(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "RELATIVE_TO"
            and id(child) not in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_8(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "relative_to"
            and id(None) not in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_9(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "relative_to"
            and id(child) in compliant
        ):
            return True
    return False


def x__has_uncompliant_relative_to__mutmut_10(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "relative_to"
            and id(child) not in compliant
        ):
            return False
    return False


def x__has_uncompliant_relative_to__mutmut_11(node: ast.AST, compliant: set[int]) -> bool:
    for child in ast.walk(node):
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "relative_to"
            and id(child) not in compliant
        ):
            return True
    return True

mutants_x__has_uncompliant_relative_to__mutmut['_mutmut_orig'] = x__has_uncompliant_relative_to__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_1'] = x__has_uncompliant_relative_to__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_2'] = x__has_uncompliant_relative_to__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_3'] = x__has_uncompliant_relative_to__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_4'] = x__has_uncompliant_relative_to__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_5'] = x__has_uncompliant_relative_to__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_6'] = x__has_uncompliant_relative_to__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_7'] = x__has_uncompliant_relative_to__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_8'] = x__has_uncompliant_relative_to__mutmut_8 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_9'] = x__has_uncompliant_relative_to__mutmut_9 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_10'] = x__has_uncompliant_relative_to__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_uncompliant_relative_to__mutmut['x__has_uncompliant_relative_to__mutmut_11'] = x__has_uncompliant_relative_to__mutmut_11 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_module_has_os_native_serialisation__mutmut)
def module_has_os_native_serialisation(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_orig(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_1(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = None
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_2(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_3(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=None)
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_4(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_5(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), )
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_6(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding=None, errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_7(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors=None), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_8(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_9(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", ), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_10(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_11(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_12(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="XXreplaceXX"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_13(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="REPLACE"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_14(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(None))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_15(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return False
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_16(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = None
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_17(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(None)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_18(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(None):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_19(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args or _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_20(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str" or node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_21(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name) or node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_22(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call) or isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_23(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id != "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_24(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "XXstrXX"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_25(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "STR"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_26(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(None, compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_27(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], None)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_28(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_29(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], )
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_30(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[1], compliant)
        ):
            return True
    return False


def x_module_has_os_native_serialisation__mutmut_31(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return False
    return False


def x_module_has_os_native_serialisation__mutmut_32(path: Path) -> bool:
    """True iff ``path`` stringifies a non-``as_posix`` ``relative_to`` result.

    Pure helper (the detection core) so tests can assert on it directly. Flags a
    ``str(...)`` call whose argument subtree holds a ``relative_to(...)`` that is
    not ``.as_posix()``-terminated. A syntax/read error is a violation because
    the configured source could not be evaluated.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
    except (SyntaxError, ValueError, OSError):
        return True
    compliant = _compliant_relative_to_nodes(tree)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "str"
            and node.args
            and _has_uncompliant_relative_to(node.args[0], compliant)
        ):
            return True
    return True

mutants_x_module_has_os_native_serialisation__mutmut['_mutmut_orig'] = x_module_has_os_native_serialisation__mutmut_orig # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_1'] = x_module_has_os_native_serialisation__mutmut_1 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_2'] = x_module_has_os_native_serialisation__mutmut_2 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_3'] = x_module_has_os_native_serialisation__mutmut_3 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_4'] = x_module_has_os_native_serialisation__mutmut_4 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_5'] = x_module_has_os_native_serialisation__mutmut_5 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_6'] = x_module_has_os_native_serialisation__mutmut_6 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_7'] = x_module_has_os_native_serialisation__mutmut_7 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_8'] = x_module_has_os_native_serialisation__mutmut_8 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_9'] = x_module_has_os_native_serialisation__mutmut_9 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_10'] = x_module_has_os_native_serialisation__mutmut_10 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_11'] = x_module_has_os_native_serialisation__mutmut_11 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_12'] = x_module_has_os_native_serialisation__mutmut_12 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_13'] = x_module_has_os_native_serialisation__mutmut_13 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_14'] = x_module_has_os_native_serialisation__mutmut_14 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_15'] = x_module_has_os_native_serialisation__mutmut_15 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_16'] = x_module_has_os_native_serialisation__mutmut_16 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_17'] = x_module_has_os_native_serialisation__mutmut_17 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_18'] = x_module_has_os_native_serialisation__mutmut_18 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_19'] = x_module_has_os_native_serialisation__mutmut_19 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_20'] = x_module_has_os_native_serialisation__mutmut_20 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_21'] = x_module_has_os_native_serialisation__mutmut_21 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_22'] = x_module_has_os_native_serialisation__mutmut_22 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_23'] = x_module_has_os_native_serialisation__mutmut_23 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_24'] = x_module_has_os_native_serialisation__mutmut_24 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_25'] = x_module_has_os_native_serialisation__mutmut_25 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_26'] = x_module_has_os_native_serialisation__mutmut_26 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_27'] = x_module_has_os_native_serialisation__mutmut_27 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_28'] = x_module_has_os_native_serialisation__mutmut_28 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_29'] = x_module_has_os_native_serialisation__mutmut_29 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_30'] = x_module_has_os_native_serialisation__mutmut_30 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_31'] = x_module_has_os_native_serialisation__mutmut_31 # type: ignore # mutmut generated
mutants_x_module_has_os_native_serialisation__mutmut['x_module_has_os_native_serialisation__mutmut_32'] = x_module_has_os_native_serialisation__mutmut_32 # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPosixPathSerialisationǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPosixPathSerialisationǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class PosixPathSerialisation(FitnessRule):
    """Flags OS-native ``str(path.relative_to(root))`` serialisation."""

    name = "posix-path-serialisation"
    remediation = REMEDIATION
    extensions = (".py",)

    @classmethod
    @_mutmut_mutated(mutants_xǁPosixPathSerialisationǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PosixPathSerialisation:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PosixPathSerialisation)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁPosixPathSerialisationǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PosixPathSerialisation:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, PosixPathSerialisation)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁPosixPathSerialisationǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PosixPathSerialisation:
        rule = None
        assert isinstance(rule, PosixPathSerialisation)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁPosixPathSerialisationǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PosixPathSerialisation:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, PosixPathSerialisation)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁPosixPathSerialisationǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PosixPathSerialisation:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, PosixPathSerialisation)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁPosixPathSerialisationǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PosixPathSerialisation:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, PosixPathSerialisation)  # noqa: S101  # narrowing for mypy
        return rule

    @classmethod
    def xǁPosixPathSerialisationǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> PosixPathSerialisation:
        rule = super().from_config(config, )
        assert isinstance(rule, PosixPathSerialisation)  # noqa: S101  # narrowing for mypy
        return rule

    @_mutmut_mutated(mutants_xǁPosixPathSerialisationǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXCLUDED_SEGMENTS for seg in rel.split("/")):
            return False
        return super().is_in_scope(rel)

    def xǁPosixPathSerialisationǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXCLUDED_SEGMENTS for seg in rel.split("/")):
            return False
        return super().is_in_scope(rel)

    def xǁPosixPathSerialisationǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        if any(None):
            return False
        return super().is_in_scope(rel)

    def xǁPosixPathSerialisationǁis_in_scope__mutmut_2(self, rel: str) -> bool:
        if any(seg not in DEFAULT_EXCLUDED_SEGMENTS for seg in rel.split("/")):
            return False
        return super().is_in_scope(rel)

    def xǁPosixPathSerialisationǁis_in_scope__mutmut_3(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXCLUDED_SEGMENTS for seg in rel.split(None)):
            return False
        return super().is_in_scope(rel)

    def xǁPosixPathSerialisationǁis_in_scope__mutmut_4(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXCLUDED_SEGMENTS for seg in rel.split("XX/XX")):
            return False
        return super().is_in_scope(rel)

    def xǁPosixPathSerialisationǁis_in_scope__mutmut_5(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXCLUDED_SEGMENTS for seg in rel.split("/")):
            return True
        return super().is_in_scope(rel)

    def xǁPosixPathSerialisationǁis_in_scope__mutmut_6(self, rel: str) -> bool:
        if any(seg in DEFAULT_EXCLUDED_SEGMENTS for seg in rel.split("/")):
            return False
        return super().is_in_scope(None)

    @_mutmut_mutated(mutants_xǁPosixPathSerialisationǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return module_has_os_native_serialisation(path)

    def xǁPosixPathSerialisationǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return module_has_os_native_serialisation(path)

    def xǁPosixPathSerialisationǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return module_has_os_native_serialisation(None)

mutants_xǁPosixPathSerialisationǁfrom_config__mutmut['_mutmut_orig'] = PosixPathSerialisation.xǁPosixPathSerialisationǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁfrom_config__mutmut['xǁPosixPathSerialisationǁfrom_config__mutmut_1'] = PosixPathSerialisation.xǁPosixPathSerialisationǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁfrom_config__mutmut['xǁPosixPathSerialisationǁfrom_config__mutmut_2'] = PosixPathSerialisation.xǁPosixPathSerialisationǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁfrom_config__mutmut['xǁPosixPathSerialisationǁfrom_config__mutmut_3'] = PosixPathSerialisation.xǁPosixPathSerialisationǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁfrom_config__mutmut['xǁPosixPathSerialisationǁfrom_config__mutmut_4'] = PosixPathSerialisation.xǁPosixPathSerialisationǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁfrom_config__mutmut['xǁPosixPathSerialisationǁfrom_config__mutmut_5'] = PosixPathSerialisation.xǁPosixPathSerialisationǁfrom_config__mutmut_5 # type: ignore # mutmut generated

mutants_xǁPosixPathSerialisationǁis_in_scope__mutmut['_mutmut_orig'] = PosixPathSerialisation.xǁPosixPathSerialisationǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁis_in_scope__mutmut['xǁPosixPathSerialisationǁis_in_scope__mutmut_1'] = PosixPathSerialisation.xǁPosixPathSerialisationǁis_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁis_in_scope__mutmut['xǁPosixPathSerialisationǁis_in_scope__mutmut_2'] = PosixPathSerialisation.xǁPosixPathSerialisationǁis_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁis_in_scope__mutmut['xǁPosixPathSerialisationǁis_in_scope__mutmut_3'] = PosixPathSerialisation.xǁPosixPathSerialisationǁis_in_scope__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁis_in_scope__mutmut['xǁPosixPathSerialisationǁis_in_scope__mutmut_4'] = PosixPathSerialisation.xǁPosixPathSerialisationǁis_in_scope__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁis_in_scope__mutmut['xǁPosixPathSerialisationǁis_in_scope__mutmut_5'] = PosixPathSerialisation.xǁPosixPathSerialisationǁis_in_scope__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁis_in_scope__mutmut['xǁPosixPathSerialisationǁis_in_scope__mutmut_6'] = PosixPathSerialisation.xǁPosixPathSerialisationǁis_in_scope__mutmut_6 # type: ignore # mutmut generated

mutants_xǁPosixPathSerialisationǁfile_has_violation__mutmut['_mutmut_orig'] = PosixPathSerialisation.xǁPosixPathSerialisationǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPosixPathSerialisationǁfile_has_violation__mutmut['xǁPosixPathSerialisationǁfile_has_violation__mutmut_1'] = PosixPathSerialisation.xǁPosixPathSerialisationǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PosixPathSerialisation:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PosixPathSerialisation.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PosixPathSerialisation:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PosixPathSerialisation.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PosixPathSerialisation:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PosixPathSerialisation.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PosixPathSerialisation:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PosixPathSerialisation.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PosixPathSerialisation:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PosixPathSerialisation.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> PosixPathSerialisation:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return PosixPathSerialisation.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PosixPathSerialisation, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PosixPathSerialisation, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PosixPathSerialisation, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(PosixPathSerialisation, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
