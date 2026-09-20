"""CORE check: no-internal-monkeypatch — no patching of own internals in tests.

A test that patches its OWN package's internals (``@patch("myapp.x.y")``,
``monkeypatch.setattr(myapp.x, "y", fake)``, or a direct
``myapp.x.y = fake`` assignment) tests the fake, not the composition. The
canonical seam is constructor injection of a fake at a boundary class. This
rule walks each in-scope test file via the AST and flags six shapes that
substitute an internal implementation:

1. ``@patch("<pkg>.X.Y", ...)`` decorator
2. ``with patch("<pkg>.X.Y", ...):`` context manager
3. ``<pkg>.X.Y = <expr>`` full-path attribute assignment
4. ``<alias>.Y = <expr>`` where ``<alias>`` resolves to an internal module
5. ``monkeypatch.setattr("<pkg>.X.Y", ...)`` string-target form
6. ``monkeypatch.setattr(<internal module ref>, "attr", fake)`` ref-target form

Stdlib and external-SDK roots are exempt -- patching those is fixturing
genuinely external state at the application edge. An assignment inside a
``with pytest.raises(...):`` block is exempt too: that pins that the patch
path is BLOCKED (e.g. a frozen dataclass), the opposite of monkey-patching.

Ported from kairix ``scripts/checks/check_no_internal_patches.py`` (F1) and
re-expressed as a configurable, repo-agnostic rule: the internal package
roots and the exempt (stdlib / SDK) roots arrive from config -- NO repo
package name is baked in. (A rule bound with no internal packages matches
nothing.)
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

REMEDIATION = _remediation(
    fix=(
        "rewrite the test to construct the unit under test with a fake "
        "injected at a boundary (e.g. SearchPipeline(retriever=FakeRetriever(...))). "
        "If the production class lacks a constructor seam, add one. When "
        "production resolves dependencies via call-time local imports, move "
        "that resolution to construction time via a Deps dataclass with "
        "default_factory and inject the fake there."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.no_internal_monkeypatch",
    passing="pipeline = SearchPipeline(retriever=FakeRetriever(hits=[...]))",
    forbidden='@patch("myapp.core.search.run")  # patches own internals',
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__matches_internal__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__matches_internal__mutmut)
def _matches_internal(name: str, internal_packages: tuple[str, ...]) -> bool:
    """True iff ``name`` is one of the internal packages or a dotted child."""
    return any(name == pkg or name.startswith(f"{pkg}.") for pkg in internal_packages)


def x__matches_internal__mutmut_orig(name: str, internal_packages: tuple[str, ...]) -> bool:
    """True iff ``name`` is one of the internal packages or a dotted child."""
    return any(name == pkg or name.startswith(f"{pkg}.") for pkg in internal_packages)


def x__matches_internal__mutmut_1(name: str, internal_packages: tuple[str, ...]) -> bool:
    """True iff ``name`` is one of the internal packages or a dotted child."""
    return any(None)


def x__matches_internal__mutmut_2(name: str, internal_packages: tuple[str, ...]) -> bool:
    """True iff ``name`` is one of the internal packages or a dotted child."""
    return any(name == pkg and name.startswith(f"{pkg}.") for pkg in internal_packages)


def x__matches_internal__mutmut_3(name: str, internal_packages: tuple[str, ...]) -> bool:
    """True iff ``name`` is one of the internal packages or a dotted child."""
    return any(name != pkg or name.startswith(f"{pkg}.") for pkg in internal_packages)


def x__matches_internal__mutmut_4(name: str, internal_packages: tuple[str, ...]) -> bool:
    """True iff ``name`` is one of the internal packages or a dotted child."""
    return any(name == pkg or name.startswith(None) for pkg in internal_packages)

mutants_x__matches_internal__mutmut['_mutmut_orig'] = x__matches_internal__mutmut_orig # type: ignore # mutmut generated
mutants_x__matches_internal__mutmut['x__matches_internal__mutmut_1'] = x__matches_internal__mutmut_1 # type: ignore # mutmut generated
mutants_x__matches_internal__mutmut['x__matches_internal__mutmut_2'] = x__matches_internal__mutmut_2 # type: ignore # mutmut generated
mutants_x__matches_internal__mutmut['x__matches_internal__mutmut_3'] = x__matches_internal__mutmut_3 # type: ignore # mutmut generated
mutants_x__matches_internal__mutmut['x__matches_internal__mutmut_4'] = x__matches_internal__mutmut_4 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__resolve_internal_aliases__mutmut)
def _resolve_internal_aliases(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_orig(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_1(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_2(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(None):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_3(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_4(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(None, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_5(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, None):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_6(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_7(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, ):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_8(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    break
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_9(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = None
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_10(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = None
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_11(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(None)[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_12(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split("XX.XX")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_13(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[1]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_14(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = None
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_15(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = None
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_16(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module and ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_17(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or "XXXX"
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_18(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_19(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(None, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_20(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, None):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_21(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_22(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, ):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_23(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                break
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_24(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = None
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_25(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname and alias.name
                aliases[local] = f"{mod}.{alias.name}" if mod else alias.name
    return aliases


def x__resolve_internal_aliases__mutmut_26(tree: ast.AST, internal_packages: tuple[str, ...]) -> dict[str, str]:
    """Map local name -> fully-qualified internal path from the file's imports."""
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _matches_internal(alias.name, internal_packages):
                    continue
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.split(".")[0]
                    aliases[root] = root
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not _matches_internal(mod, internal_packages):
                continue
            for alias in node.names:
                local = alias.asname or alias.name
                aliases[local] = None
    return aliases

mutants_x__resolve_internal_aliases__mutmut['_mutmut_orig'] = x__resolve_internal_aliases__mutmut_orig # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_1'] = x__resolve_internal_aliases__mutmut_1 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_2'] = x__resolve_internal_aliases__mutmut_2 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_3'] = x__resolve_internal_aliases__mutmut_3 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_4'] = x__resolve_internal_aliases__mutmut_4 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_5'] = x__resolve_internal_aliases__mutmut_5 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_6'] = x__resolve_internal_aliases__mutmut_6 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_7'] = x__resolve_internal_aliases__mutmut_7 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_8'] = x__resolve_internal_aliases__mutmut_8 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_9'] = x__resolve_internal_aliases__mutmut_9 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_10'] = x__resolve_internal_aliases__mutmut_10 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_11'] = x__resolve_internal_aliases__mutmut_11 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_12'] = x__resolve_internal_aliases__mutmut_12 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_13'] = x__resolve_internal_aliases__mutmut_13 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_14'] = x__resolve_internal_aliases__mutmut_14 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_15'] = x__resolve_internal_aliases__mutmut_15 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_16'] = x__resolve_internal_aliases__mutmut_16 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_17'] = x__resolve_internal_aliases__mutmut_17 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_18'] = x__resolve_internal_aliases__mutmut_18 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_19'] = x__resolve_internal_aliases__mutmut_19 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_20'] = x__resolve_internal_aliases__mutmut_20 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_21'] = x__resolve_internal_aliases__mutmut_21 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_22'] = x__resolve_internal_aliases__mutmut_22 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_23'] = x__resolve_internal_aliases__mutmut_23 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_24'] = x__resolve_internal_aliases__mutmut_24 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_25'] = x__resolve_internal_aliases__mutmut_25 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut['x__resolve_internal_aliases__mutmut_26'] = x__resolve_internal_aliases__mutmut_26 # type: ignore # mutmut generated
mutants_x__attribute_root_name__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__attribute_root_name__mutmut)
def _attribute_root_name(node: ast.expr) -> str | None:
    cur = node
    while isinstance(cur, ast.Attribute):
        cur = cur.value
    if isinstance(cur, ast.Name):
        return cur.id
    return None


def x__attribute_root_name__mutmut_orig(node: ast.expr) -> str | None:
    cur = node
    while isinstance(cur, ast.Attribute):
        cur = cur.value
    if isinstance(cur, ast.Name):
        return cur.id
    return None


def x__attribute_root_name__mutmut_1(node: ast.expr) -> str | None:
    cur = None
    while isinstance(cur, ast.Attribute):
        cur = cur.value
    if isinstance(cur, ast.Name):
        return cur.id
    return None


def x__attribute_root_name__mutmut_2(node: ast.expr) -> str | None:
    cur = node
    while isinstance(cur, ast.Attribute):
        cur = None
    if isinstance(cur, ast.Name):
        return cur.id
    return None

mutants_x__attribute_root_name__mutmut['_mutmut_orig'] = x__attribute_root_name__mutmut_orig # type: ignore # mutmut generated
mutants_x__attribute_root_name__mutmut['x__attribute_root_name__mutmut_1'] = x__attribute_root_name__mutmut_1 # type: ignore # mutmut generated
mutants_x__attribute_root_name__mutmut['x__attribute_root_name__mutmut_2'] = x__attribute_root_name__mutmut_2 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__resolves_to_internal__mutmut)
def _resolves_to_internal(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_orig(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_1(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = None
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_2(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(None)[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_3(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split("XX.XX")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_4(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[1] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_5(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id not in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_6(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return False
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_7(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases or _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_8(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id not in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_9(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(None, internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_10(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], None)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_11(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_12(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], )
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_13(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = None
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_14(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(None)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_15(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is not None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_16(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return True
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_17(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root not in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_18(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return False
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_19(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases or _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_20(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root not in aliases and _matches_internal(aliases[root], internal_packages)
    return False


def x__resolves_to_internal__mutmut_21(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(None, internal_packages)
    return False


def x__resolves_to_internal__mutmut_22(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], None)
    return False


def x__resolves_to_internal__mutmut_23(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(internal_packages)
    return False


def x__resolves_to_internal__mutmut_24(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], )
    return False


def x__resolves_to_internal__mutmut_25(
    expr: ast.expr,
    aliases: dict[str, str],
    internal_packages: tuple[str, ...],
) -> bool:
    """Does ``expr`` (a Name or Attribute) resolve to an internal module?"""
    package_roots = {pkg.split(".")[0] for pkg in internal_packages}
    if isinstance(expr, ast.Name):
        if expr.id in package_roots:
            return True
        return expr.id in aliases and _matches_internal(aliases[expr.id], internal_packages)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        if root is None:
            return False
        if root in package_roots:
            return True
        return root in aliases and _matches_internal(aliases[root], internal_packages)
    return True

mutants_x__resolves_to_internal__mutmut['_mutmut_orig'] = x__resolves_to_internal__mutmut_orig # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_1'] = x__resolves_to_internal__mutmut_1 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_2'] = x__resolves_to_internal__mutmut_2 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_3'] = x__resolves_to_internal__mutmut_3 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_4'] = x__resolves_to_internal__mutmut_4 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_5'] = x__resolves_to_internal__mutmut_5 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_6'] = x__resolves_to_internal__mutmut_6 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_7'] = x__resolves_to_internal__mutmut_7 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_8'] = x__resolves_to_internal__mutmut_8 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_9'] = x__resolves_to_internal__mutmut_9 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_10'] = x__resolves_to_internal__mutmut_10 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_11'] = x__resolves_to_internal__mutmut_11 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_12'] = x__resolves_to_internal__mutmut_12 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_13'] = x__resolves_to_internal__mutmut_13 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_14'] = x__resolves_to_internal__mutmut_14 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_15'] = x__resolves_to_internal__mutmut_15 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_16'] = x__resolves_to_internal__mutmut_16 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_17'] = x__resolves_to_internal__mutmut_17 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_18'] = x__resolves_to_internal__mutmut_18 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_19'] = x__resolves_to_internal__mutmut_19 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_20'] = x__resolves_to_internal__mutmut_20 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_21'] = x__resolves_to_internal__mutmut_21 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_22'] = x__resolves_to_internal__mutmut_22 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_23'] = x__resolves_to_internal__mutmut_23 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_24'] = x__resolves_to_internal__mutmut_24 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut['x__resolves_to_internal__mutmut_25'] = x__resolves_to_internal__mutmut_25 # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_patch_call__mutmut)
def _is_patch_call(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_orig(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_1(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_2(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return True
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_3(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return False
    func = None
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_4(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id != "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_5(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "XXpatchXX"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_6(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "PATCH"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_7(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr != "patch"
    return False


def x__is_patch_call__mutmut_8(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "XXpatchXX"
    return False


def x__is_patch_call__mutmut_9(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "PATCH"
    return False


def x__is_patch_call__mutmut_10(node: ast.expr) -> bool:
    """Call to ``patch`` / ``mock.patch`` etc. (NOT ``patch.dict`` / ``patch.object``)."""
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return True

mutants_x__is_patch_call__mutmut['_mutmut_orig'] = x__is_patch_call__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut['x__is_patch_call__mutmut_1'] = x__is_patch_call__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut['x__is_patch_call__mutmut_2'] = x__is_patch_call__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut['x__is_patch_call__mutmut_3'] = x__is_patch_call__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut['x__is_patch_call__mutmut_4'] = x__is_patch_call__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut['x__is_patch_call__mutmut_5'] = x__is_patch_call__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut['x__is_patch_call__mutmut_6'] = x__is_patch_call__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut['x__is_patch_call__mutmut_7'] = x__is_patch_call__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut['x__is_patch_call__mutmut_8'] = x__is_patch_call__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut['x__is_patch_call__mutmut_9'] = x__is_patch_call__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_patch_call__mutmut['x__is_patch_call__mutmut_10'] = x__is_patch_call__mutmut_10 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__first_arg_is_internal_string__mutmut)
def _first_arg_is_internal_string(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_orig(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_1(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) and not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_2(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_3(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_4(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return True
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_5(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = None
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_6(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[1]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_7(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) or isinstance(first.value, str):
        return _matches_internal(first.value, internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_8(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(None, internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_9(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, None)
    return False


def x__first_arg_is_internal_string__mutmut_10(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(internal_packages)
    return False


def x__first_arg_is_internal_string__mutmut_11(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, )
    return False


def x__first_arg_is_internal_string__mutmut_12(call: ast.expr, internal_packages: tuple[str, ...]) -> bool:
    """First positional arg is a string literal naming an internal module."""
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return _matches_internal(first.value, internal_packages)
    return True

mutants_x__first_arg_is_internal_string__mutmut['_mutmut_orig'] = x__first_arg_is_internal_string__mutmut_orig # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_1'] = x__first_arg_is_internal_string__mutmut_1 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_2'] = x__first_arg_is_internal_string__mutmut_2 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_3'] = x__first_arg_is_internal_string__mutmut_3 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_4'] = x__first_arg_is_internal_string__mutmut_4 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_5'] = x__first_arg_is_internal_string__mutmut_5 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_6'] = x__first_arg_is_internal_string__mutmut_6 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_7'] = x__first_arg_is_internal_string__mutmut_7 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_8'] = x__first_arg_is_internal_string__mutmut_8 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_9'] = x__first_arg_is_internal_string__mutmut_9 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_10'] = x__first_arg_is_internal_string__mutmut_10 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_11'] = x__first_arg_is_internal_string__mutmut_11 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_12'] = x__first_arg_is_internal_string__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_monkeypatch_setattr__mutmut)
def _is_monkeypatch_setattr(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "setattr"
        and isinstance(func.value, ast.Name)
        and func.value.id == "monkeypatch"
    )


def x__is_monkeypatch_setattr__mutmut_orig(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "setattr"
        and isinstance(func.value, ast.Name)
        and func.value.id == "monkeypatch"
    )


def x__is_monkeypatch_setattr__mutmut_1(node: ast.Call) -> bool:
    func = None
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "setattr"
        and isinstance(func.value, ast.Name)
        and func.value.id == "monkeypatch"
    )


def x__is_monkeypatch_setattr__mutmut_2(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "setattr"
        and isinstance(func.value, ast.Name) or func.value.id == "monkeypatch"
    )


def x__is_monkeypatch_setattr__mutmut_3(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "setattr" or isinstance(func.value, ast.Name)
        and func.value.id == "monkeypatch"
    )


def x__is_monkeypatch_setattr__mutmut_4(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute) or func.attr == "setattr"
        and isinstance(func.value, ast.Name)
        and func.value.id == "monkeypatch"
    )


def x__is_monkeypatch_setattr__mutmut_5(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr != "setattr"
        and isinstance(func.value, ast.Name)
        and func.value.id == "monkeypatch"
    )


def x__is_monkeypatch_setattr__mutmut_6(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "XXsetattrXX"
        and isinstance(func.value, ast.Name)
        and func.value.id == "monkeypatch"
    )


def x__is_monkeypatch_setattr__mutmut_7(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "SETATTR"
        and isinstance(func.value, ast.Name)
        and func.value.id == "monkeypatch"
    )


def x__is_monkeypatch_setattr__mutmut_8(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "setattr"
        and isinstance(func.value, ast.Name)
        and func.value.id != "monkeypatch"
    )


def x__is_monkeypatch_setattr__mutmut_9(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "setattr"
        and isinstance(func.value, ast.Name)
        and func.value.id == "XXmonkeypatchXX"
    )


def x__is_monkeypatch_setattr__mutmut_10(node: ast.Call) -> bool:
    func = node.func
    return (
        isinstance(func, ast.Attribute)
        and func.attr == "setattr"
        and isinstance(func.value, ast.Name)
        and func.value.id == "MONKEYPATCH"
    )

mutants_x__is_monkeypatch_setattr__mutmut['_mutmut_orig'] = x__is_monkeypatch_setattr__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut['x__is_monkeypatch_setattr__mutmut_1'] = x__is_monkeypatch_setattr__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut['x__is_monkeypatch_setattr__mutmut_2'] = x__is_monkeypatch_setattr__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut['x__is_monkeypatch_setattr__mutmut_3'] = x__is_monkeypatch_setattr__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut['x__is_monkeypatch_setattr__mutmut_4'] = x__is_monkeypatch_setattr__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut['x__is_monkeypatch_setattr__mutmut_5'] = x__is_monkeypatch_setattr__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut['x__is_monkeypatch_setattr__mutmut_6'] = x__is_monkeypatch_setattr__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut['x__is_monkeypatch_setattr__mutmut_7'] = x__is_monkeypatch_setattr__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut['x__is_monkeypatch_setattr__mutmut_8'] = x__is_monkeypatch_setattr__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut['x__is_monkeypatch_setattr__mutmut_9'] = x__is_monkeypatch_setattr__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_monkeypatch_setattr__mutmut['x__is_monkeypatch_setattr__mutmut_10'] = x__is_monkeypatch_setattr__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_inside_pytest_raises__mutmut)
def _is_inside_pytest_raises(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_orig(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_1(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = None
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_2(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_3(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = None
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_4(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = None
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_5(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) or func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_6(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr != "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_7(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "XXraisesXX":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_8(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "RAISES":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_9(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return False
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_10(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) or func.id == "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_11(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id != "raises":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_12(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "XXraisesXX":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_13(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "RAISES":
                        return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_14(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return False
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_15(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = None
    return False


def x__is_inside_pytest_raises__mutmut_16(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(None)
    return False


def x__is_inside_pytest_raises__mutmut_17(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    """True iff ``node`` is lexically inside a ``with pytest.raises(...):`` block."""
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With):
            for item in current.items:
                ctx = item.context_expr
                if isinstance(ctx, ast.Call):
                    func = ctx.func
                    if isinstance(func, ast.Attribute) and func.attr == "raises":
                        return True
                    if isinstance(func, ast.Name) and func.id == "raises":
                        return True
        current = parent_map.get(current)
    return True

mutants_x__is_inside_pytest_raises__mutmut['_mutmut_orig'] = x__is_inside_pytest_raises__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_1'] = x__is_inside_pytest_raises__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_2'] = x__is_inside_pytest_raises__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_3'] = x__is_inside_pytest_raises__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_4'] = x__is_inside_pytest_raises__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_5'] = x__is_inside_pytest_raises__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_6'] = x__is_inside_pytest_raises__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_7'] = x__is_inside_pytest_raises__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_8'] = x__is_inside_pytest_raises__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_9'] = x__is_inside_pytest_raises__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_10'] = x__is_inside_pytest_raises__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_11'] = x__is_inside_pytest_raises__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_12'] = x__is_inside_pytest_raises__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_13'] = x__is_inside_pytest_raises__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_14'] = x__is_inside_pytest_raises__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_15'] = x__is_inside_pytest_raises__mutmut_15 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_16'] = x__is_inside_pytest_raises__mutmut_16 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut['x__is_inside_pytest_raises__mutmut_17'] = x__is_inside_pytest_raises__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_has_internal_patch__mutmut)
def file_has_internal_patch(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_orig(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_1(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_2(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return True
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_3(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_4(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_5(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_6(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_7(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_8(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_9(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_10(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_11(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_12(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_13(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = None
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_14(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(None, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_15(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, None)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_16(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_17(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, )
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_18(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = None
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_19(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(None):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_20(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(None):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_21(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_22(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(None):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_23(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) or _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_24(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(None) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_25(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(None, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_26(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, None):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_27(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_28(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, ):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_29(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return False

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_30(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = None
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_31(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) or _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_32(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(None) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_33(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(None, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_34(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, None):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_35(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_36(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, ):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_37(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return False

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_38(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages) or not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_39(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute) or _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_40(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(None, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_41(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, None, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_42(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, None)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_43(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_44(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_45(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, )
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_46(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_47(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(None, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_48(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, None)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_49(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_50(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, )
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_51(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return False

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_52(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) or _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_53(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(None):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_54(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(None, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_55(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, None):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_56(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_57(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, ):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_58(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return False
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_59(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args or _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_60(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(None, aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_61(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], None, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_62(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, None):
                return True

    return False


def x_file_has_internal_patch__mutmut_63(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_64(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_65(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, ):
                return True

    return False


def x_file_has_internal_patch__mutmut_66(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[1], aliases, internal_packages):
                return True

    return False


def x_file_has_internal_patch__mutmut_67(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return False

    return False


def x_file_has_internal_patch__mutmut_68(
    path: Path,
    *,
    internal_packages: tuple[str, ...],
) -> bool:
    """True iff ``path`` contains any of the six internal-patch shapes.

    Pure helper (the detection core). A syntax / decode error is treated as
    "no violation" (another check owns unparseable files).
    """
    if not internal_packages:
        return False
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False

    aliases = _resolve_internal_aliases(tree, internal_packages)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            for deco in node.decorator_list:
                if _is_patch_call(deco) and _first_arg_is_internal_string(deco, internal_packages):
                    return True

        if isinstance(node, ast.With):
            for item in node.items:
                ctx = item.context_expr
                if _is_patch_call(ctx) and _first_arg_is_internal_string(ctx, internal_packages):
                    return True

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and _resolves_to_internal(target, aliases, internal_packages)
                    and not _is_inside_pytest_raises(parent_map, node)
                ):
                    return True

        if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
            if _first_arg_is_internal_string(node, internal_packages):
                return True
            if node.args and _resolves_to_internal(node.args[0], aliases, internal_packages):
                return True

    return True

mutants_x_file_has_internal_patch__mutmut['_mutmut_orig'] = x_file_has_internal_patch__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_1'] = x_file_has_internal_patch__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_2'] = x_file_has_internal_patch__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_3'] = x_file_has_internal_patch__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_4'] = x_file_has_internal_patch__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_5'] = x_file_has_internal_patch__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_6'] = x_file_has_internal_patch__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_7'] = x_file_has_internal_patch__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_8'] = x_file_has_internal_patch__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_9'] = x_file_has_internal_patch__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_10'] = x_file_has_internal_patch__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_11'] = x_file_has_internal_patch__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_12'] = x_file_has_internal_patch__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_13'] = x_file_has_internal_patch__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_14'] = x_file_has_internal_patch__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_15'] = x_file_has_internal_patch__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_16'] = x_file_has_internal_patch__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_17'] = x_file_has_internal_patch__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_18'] = x_file_has_internal_patch__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_19'] = x_file_has_internal_patch__mutmut_19 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_20'] = x_file_has_internal_patch__mutmut_20 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_21'] = x_file_has_internal_patch__mutmut_21 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_22'] = x_file_has_internal_patch__mutmut_22 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_23'] = x_file_has_internal_patch__mutmut_23 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_24'] = x_file_has_internal_patch__mutmut_24 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_25'] = x_file_has_internal_patch__mutmut_25 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_26'] = x_file_has_internal_patch__mutmut_26 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_27'] = x_file_has_internal_patch__mutmut_27 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_28'] = x_file_has_internal_patch__mutmut_28 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_29'] = x_file_has_internal_patch__mutmut_29 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_30'] = x_file_has_internal_patch__mutmut_30 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_31'] = x_file_has_internal_patch__mutmut_31 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_32'] = x_file_has_internal_patch__mutmut_32 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_33'] = x_file_has_internal_patch__mutmut_33 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_34'] = x_file_has_internal_patch__mutmut_34 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_35'] = x_file_has_internal_patch__mutmut_35 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_36'] = x_file_has_internal_patch__mutmut_36 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_37'] = x_file_has_internal_patch__mutmut_37 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_38'] = x_file_has_internal_patch__mutmut_38 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_39'] = x_file_has_internal_patch__mutmut_39 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_40'] = x_file_has_internal_patch__mutmut_40 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_41'] = x_file_has_internal_patch__mutmut_41 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_42'] = x_file_has_internal_patch__mutmut_42 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_43'] = x_file_has_internal_patch__mutmut_43 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_44'] = x_file_has_internal_patch__mutmut_44 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_45'] = x_file_has_internal_patch__mutmut_45 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_46'] = x_file_has_internal_patch__mutmut_46 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_47'] = x_file_has_internal_patch__mutmut_47 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_48'] = x_file_has_internal_patch__mutmut_48 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_49'] = x_file_has_internal_patch__mutmut_49 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_50'] = x_file_has_internal_patch__mutmut_50 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_51'] = x_file_has_internal_patch__mutmut_51 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_52'] = x_file_has_internal_patch__mutmut_52 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_53'] = x_file_has_internal_patch__mutmut_53 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_54'] = x_file_has_internal_patch__mutmut_54 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_55'] = x_file_has_internal_patch__mutmut_55 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_56'] = x_file_has_internal_patch__mutmut_56 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_57'] = x_file_has_internal_patch__mutmut_57 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_58'] = x_file_has_internal_patch__mutmut_58 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_59'] = x_file_has_internal_patch__mutmut_59 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_60'] = x_file_has_internal_patch__mutmut_60 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_61'] = x_file_has_internal_patch__mutmut_61 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_62'] = x_file_has_internal_patch__mutmut_62 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_63'] = x_file_has_internal_patch__mutmut_63 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_64'] = x_file_has_internal_patch__mutmut_64 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_65'] = x_file_has_internal_patch__mutmut_65 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_66'] = x_file_has_internal_patch__mutmut_66 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_67'] = x_file_has_internal_patch__mutmut_67 # type: ignore # mutmut generated
mutants_x_file_has_internal_patch__mutmut['x_file_has_internal_patch__mutmut_68'] = x_file_has_internal_patch__mutmut_68 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoInternalMonkeypatchǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoInternalMonkeypatch(FitnessRule):
    """Flags test files that patch their own package's internals."""

    name = "no-internal-monkeypatch"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Internal package roots to protect -- repo-supplied, no default identity.
    internal_packages: tuple[str, ...] = ()

    @classmethod
    @_mutmut_mutated(mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("internal_packages")
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("internal_packages")
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = None
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("internal_packages")
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("internal_packages")
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("internal_packages")
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("internal_packages")
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, )
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("internal_packages")
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = None
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get(None)
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("XXinternal_packagesXX")
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("INTERNAL_PACKAGES")
        rule.internal_packages = tuple(packages) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("internal_packages")
        rule.internal_packages = None
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("internal_packages")
        rule.internal_packages = tuple(None) if packages is not None else ()
        return rule

    @classmethod
    def xǁNoInternalMonkeypatchǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalMonkeypatch:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalMonkeypatch)  # noqa: S101  # narrowing for mypy
        packages = config.get("internal_packages")
        rule.internal_packages = tuple(packages) if packages is None else ()
        return rule

    @_mutmut_mutated(mutants_xǁNoInternalMonkeypatchǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_has_internal_patch(
            path,
            internal_packages=self.internal_packages,
        )

    def xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_has_internal_patch(
            path,
            internal_packages=self.internal_packages,
        )

    def xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_has_internal_patch(
            None,
            internal_packages=self.internal_packages,
        )

    def xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_has_internal_patch(
            path,
            internal_packages=None,
        )

    def xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_has_internal_patch(
            internal_packages=self.internal_packages,
        )

    def xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_has_internal_patch(
            path,
            )

mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['_mutmut_orig'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_1'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_2'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_3'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_4'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_5'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_6'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_7'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_8'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_9'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_10'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_11'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfrom_config__mutmut['xǁNoInternalMonkeypatchǁfrom_config__mutmut_12'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfrom_config__mutmut_12 # type: ignore # mutmut generated

mutants_xǁNoInternalMonkeypatchǁfile_has_violation__mutmut['_mutmut_orig'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfile_has_violation__mutmut['xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_1'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfile_has_violation__mutmut['xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_2'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfile_has_violation__mutmut['xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_3'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoInternalMonkeypatchǁfile_has_violation__mutmut['xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_4'] = NoInternalMonkeypatch.xǁNoInternalMonkeypatchǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoInternalMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalMonkeypatch.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoInternalMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalMonkeypatch.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoInternalMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalMonkeypatch.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoInternalMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalMonkeypatch.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoInternalMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalMonkeypatch.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoInternalMonkeypatch:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalMonkeypatch.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalMonkeypatch, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalMonkeypatch, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalMonkeypatch, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalMonkeypatch, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
