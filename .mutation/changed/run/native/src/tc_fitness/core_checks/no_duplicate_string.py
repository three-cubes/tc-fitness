"""CORE check: no_duplicate_string — Sonar S1192 (the exemplar CORE module).

A string literal of >= ``min_length`` chars duplicated >= ``min_occurrences``
times in a single Python module is a refactor smell — the reader can't tell
whether the sites are coupled or coincidentally identical. Extracting to a
module-level ``UPPER_SNAKE_CASE`` constant makes the coupling explicit.

This is the COPY-PATTERN every other CORE check follows (the Port agents lift
this shape): a :class:`tc_fitness.fitness_rule.FitnessRule` subclass that reads
its repo-specific knobs (``min_length`` / ``min_occurrences`` and the
inherited ``roots`` / ``extensions`` / ``exempt_files``) from the consumer's
config, plus a ``build()`` factory and a ``main()`` wired through
:func:`tc_fitness.core_checks.run_core_check`.

Ported from tc-agent-zone ``scripts/checks/no_duplicate_string.py`` (itself
kairix F17) and re-expressed as a configurable, repo-agnostic rule: NO repo
paths, globs, or threshold literals are baked in — the defaults are
domain-intrinsic (S1192's own 10-char / 3-occurrence shape) and every one is
overridable via ``[tool.tc_fitness]``.
"""

from __future__ import annotations

import ast
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: S1192's own defaults — domain-intrinsic, not repo identity. Overridable.
DEFAULT_MIN_LENGTH = 10
DEFAULT_MIN_OCCURRENCES = 3

REMEDIATION = _remediation(
    fix=(
        'declare `_<NAME> = "<the literal>"` near the top of the module and '
        "replace every occurrence of the literal with the constant — this makes "
        "the coupling between sites explicit and gives renames a single edit site."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.no_duplicate_string",
    passing='_ERROR_BAD_QUERY = "search query must be a non-empty string"  # used 3x',
    forbidden='raise ValueError("search query must be a non-empty string")  # repeated 3x inline',
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__collect_docstring_ids__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__collect_docstring_ids__mutmut)
def _collect_docstring_ids(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                out.add(id(first.value))
    return out


def x__collect_docstring_ids__mutmut_orig(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                out.add(id(first.value))
    return out


def x__collect_docstring_ids__mutmut_1(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                out.add(id(first.value))
    return out


def x__collect_docstring_ids__mutmut_2(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = set()
    for node in ast.walk(None):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                out.add(id(first.value))
    return out


def x__collect_docstring_ids__mutmut_3(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) or node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                out.add(id(first.value))
    return out


def x__collect_docstring_ids__mutmut_4(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = None
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                out.add(id(first.value))
    return out


def x__collect_docstring_ids__mutmut_5(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[1]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                out.add(id(first.value))
    return out


def x__collect_docstring_ids__mutmut_6(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant) or isinstance(first.value.value, str)
            ):
                out.add(id(first.value))
    return out


def x__collect_docstring_ids__mutmut_7(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr) or isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                out.add(id(first.value))
    return out


def x__collect_docstring_ids__mutmut_8(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                out.add(None)
    return out


def x__collect_docstring_ids__mutmut_9(tree: ast.AST) -> set[int]:
    """Object-ids of the docstring Constant nodes (excluded from counting)."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                out.add(id(None))
    return out

mutants_x__collect_docstring_ids__mutmut['_mutmut_orig'] = x__collect_docstring_ids__mutmut_orig # type: ignore # mutmut generated
mutants_x__collect_docstring_ids__mutmut['x__collect_docstring_ids__mutmut_1'] = x__collect_docstring_ids__mutmut_1 # type: ignore # mutmut generated
mutants_x__collect_docstring_ids__mutmut['x__collect_docstring_ids__mutmut_2'] = x__collect_docstring_ids__mutmut_2 # type: ignore # mutmut generated
mutants_x__collect_docstring_ids__mutmut['x__collect_docstring_ids__mutmut_3'] = x__collect_docstring_ids__mutmut_3 # type: ignore # mutmut generated
mutants_x__collect_docstring_ids__mutmut['x__collect_docstring_ids__mutmut_4'] = x__collect_docstring_ids__mutmut_4 # type: ignore # mutmut generated
mutants_x__collect_docstring_ids__mutmut['x__collect_docstring_ids__mutmut_5'] = x__collect_docstring_ids__mutmut_5 # type: ignore # mutmut generated
mutants_x__collect_docstring_ids__mutmut['x__collect_docstring_ids__mutmut_6'] = x__collect_docstring_ids__mutmut_6 # type: ignore # mutmut generated
mutants_x__collect_docstring_ids__mutmut['x__collect_docstring_ids__mutmut_7'] = x__collect_docstring_ids__mutmut_7 # type: ignore # mutmut generated
mutants_x__collect_docstring_ids__mutmut['x__collect_docstring_ids__mutmut_8'] = x__collect_docstring_ids__mutmut_8 # type: ignore # mutmut generated
mutants_x__collect_docstring_ids__mutmut['x__collect_docstring_ids__mutmut_9'] = x__collect_docstring_ids__mutmut_9 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_module_has_duplicate__mutmut)
def module_has_duplicate(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_orig(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_1(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_2(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_3(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_4(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_5(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_6(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_7(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_8(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_9(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_10(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return True
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_11(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = None
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_12(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(None)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_13(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = None
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_14(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(None):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_15(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) and not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_16(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_17(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_18(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            break
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_19(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(None) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_20(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) not in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_21(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            break
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_22(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = None
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_23(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length and not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_24(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) <= min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_25(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or value.strip():
            continue
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_26(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            break
        counts[value] += 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_27(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] = 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_28(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] -= 1
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_29(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 2
    return any(c >= min_occurrences for c in counts.values())


def x_module_has_duplicate__mutmut_30(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(None)


def x_module_has_duplicate__mutmut_31(path: Path, *, min_length: int, min_occurrences: int) -> bool:
    """True iff ``path`` holds a str literal >= ``min_length`` repeated >= ``min_occurrences`` times.

    Pure helper (the detection core) so tests can assert on it directly:
    parses the module, counts non-docstring non-blank string Constants, and
    flags the file when any value crosses the occurrence threshold. A syntax /
    decode error is treated as "no violation" (another check owns unparseable
    files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return False
    docstring_ids = _collect_docstring_ids(tree)
    counts: Counter[str] = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstring_ids:
            continue
        value = node.value
        if len(value) < min_length or not value.strip():
            continue
        counts[value] += 1
    return any(c > min_occurrences for c in counts.values())

mutants_x_module_has_duplicate__mutmut['_mutmut_orig'] = x_module_has_duplicate__mutmut_orig # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_1'] = x_module_has_duplicate__mutmut_1 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_2'] = x_module_has_duplicate__mutmut_2 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_3'] = x_module_has_duplicate__mutmut_3 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_4'] = x_module_has_duplicate__mutmut_4 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_5'] = x_module_has_duplicate__mutmut_5 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_6'] = x_module_has_duplicate__mutmut_6 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_7'] = x_module_has_duplicate__mutmut_7 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_8'] = x_module_has_duplicate__mutmut_8 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_9'] = x_module_has_duplicate__mutmut_9 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_10'] = x_module_has_duplicate__mutmut_10 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_11'] = x_module_has_duplicate__mutmut_11 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_12'] = x_module_has_duplicate__mutmut_12 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_13'] = x_module_has_duplicate__mutmut_13 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_14'] = x_module_has_duplicate__mutmut_14 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_15'] = x_module_has_duplicate__mutmut_15 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_16'] = x_module_has_duplicate__mutmut_16 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_17'] = x_module_has_duplicate__mutmut_17 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_18'] = x_module_has_duplicate__mutmut_18 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_19'] = x_module_has_duplicate__mutmut_19 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_20'] = x_module_has_duplicate__mutmut_20 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_21'] = x_module_has_duplicate__mutmut_21 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_22'] = x_module_has_duplicate__mutmut_22 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_23'] = x_module_has_duplicate__mutmut_23 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_24'] = x_module_has_duplicate__mutmut_24 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_25'] = x_module_has_duplicate__mutmut_25 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_26'] = x_module_has_duplicate__mutmut_26 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_27'] = x_module_has_duplicate__mutmut_27 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_28'] = x_module_has_duplicate__mutmut_28 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_29'] = x_module_has_duplicate__mutmut_29 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_30'] = x_module_has_duplicate__mutmut_30 # type: ignore # mutmut generated
mutants_x_module_has_duplicate__mutmut['x_module_has_duplicate__mutmut_31'] = x_module_has_duplicate__mutmut_31 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoDuplicateStringǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoDuplicateString(FitnessRule):
    """Flags modules with a duplicated string literal (Sonar S1192)."""

    name = "no-duplicate-string"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific thresholds. Instance attributes so ``from_config`` can
    #: override them per consumer; class defaults are S1192's own shape.
    min_length: int = DEFAULT_MIN_LENGTH
    min_occurrences: int = DEFAULT_MIN_OCCURRENCES

    @classmethod
    @_mutmut_mutated(mutants_xǁNoDuplicateStringǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = None
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, )
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = None
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(None)
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get(None, DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", None))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get(DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", ))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("XXmin_lengthXX", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("MIN_LENGTH", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = None
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(None)
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get(None, DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", None))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get(DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("min_occurrences", ))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("XXmin_occurrencesXX", DEFAULT_MIN_OCCURRENCES))
        return rule

    @classmethod
    def xǁNoDuplicateStringǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoDuplicateString:
        """Build from config, also reading the two rule-specific thresholds.

        Extends the base ``from_config`` (which handles ``roots`` /
        ``extensions`` / ``exempt_files`` / ``name``) with ``min_length`` and
        ``min_occurrences``.
        """
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoDuplicateString)  # noqa: S101  # narrowing for mypy
        rule.min_length = int(config.get("min_length", DEFAULT_MIN_LENGTH))
        rule.min_occurrences = int(config.get("MIN_OCCURRENCES", DEFAULT_MIN_OCCURRENCES))
        return rule

    @_mutmut_mutated(mutants_xǁNoDuplicateStringǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return module_has_duplicate(
            path,
            min_length=self.min_length,
            min_occurrences=self.min_occurrences,
        )

    def xǁNoDuplicateStringǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return module_has_duplicate(
            path,
            min_length=self.min_length,
            min_occurrences=self.min_occurrences,
        )

    def xǁNoDuplicateStringǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return module_has_duplicate(
            None,
            min_length=self.min_length,
            min_occurrences=self.min_occurrences,
        )

    def xǁNoDuplicateStringǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return module_has_duplicate(
            path,
            min_length=None,
            min_occurrences=self.min_occurrences,
        )

    def xǁNoDuplicateStringǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return module_has_duplicate(
            path,
            min_length=self.min_length,
            min_occurrences=None,
        )

    def xǁNoDuplicateStringǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return module_has_duplicate(
            min_length=self.min_length,
            min_occurrences=self.min_occurrences,
        )

    def xǁNoDuplicateStringǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        return module_has_duplicate(
            path,
            min_occurrences=self.min_occurrences,
        )

    def xǁNoDuplicateStringǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        return module_has_duplicate(
            path,
            min_length=self.min_length,
            )

mutants_xǁNoDuplicateStringǁfrom_config__mutmut['_mutmut_orig'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_1'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_2'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_3'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_4'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_5'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_6'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_7'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_8'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_9'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_10'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_11'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_12'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_13'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_14'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_15'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_16'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_17'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_18'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_19'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_20'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfrom_config__mutmut['xǁNoDuplicateStringǁfrom_config__mutmut_21'] = NoDuplicateString.xǁNoDuplicateStringǁfrom_config__mutmut_21 # type: ignore # mutmut generated

mutants_xǁNoDuplicateStringǁfile_has_violation__mutmut['_mutmut_orig'] = NoDuplicateString.xǁNoDuplicateStringǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfile_has_violation__mutmut['xǁNoDuplicateStringǁfile_has_violation__mutmut_1'] = NoDuplicateString.xǁNoDuplicateStringǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfile_has_violation__mutmut['xǁNoDuplicateStringǁfile_has_violation__mutmut_2'] = NoDuplicateString.xǁNoDuplicateStringǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfile_has_violation__mutmut['xǁNoDuplicateStringǁfile_has_violation__mutmut_3'] = NoDuplicateString.xǁNoDuplicateStringǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfile_has_violation__mutmut['xǁNoDuplicateStringǁfile_has_violation__mutmut_4'] = NoDuplicateString.xǁNoDuplicateStringǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfile_has_violation__mutmut['xǁNoDuplicateStringǁfile_has_violation__mutmut_5'] = NoDuplicateString.xǁNoDuplicateStringǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoDuplicateStringǁfile_has_violation__mutmut['xǁNoDuplicateStringǁfile_has_violation__mutmut_6'] = NoDuplicateString.xǁNoDuplicateStringǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoDuplicateString:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoDuplicateString.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoDuplicateString:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoDuplicateString.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoDuplicateString:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoDuplicateString.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoDuplicateString:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoDuplicateString.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoDuplicateString:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoDuplicateString.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoDuplicateString:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoDuplicateString.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoDuplicateString, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoDuplicateString, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoDuplicateString, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoDuplicateString, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
