"""CORE check: no_internal_patches — tests must not substitute internal modules.

A test that ``monkeypatch.setattr`` / ``unittest.mock.patch`` / assigns onto an
INTERNAL module is inappropriate intimacy: it simulates composition instead of
exercising it, so the suite stays green while production wiring rots. (The
canonical example: ~1583 monkeypatched tests inflating coverage 47%->82%
without adding defect-catching power.) The right unit of work is to construct
the unit under test with explicit fakes passed through its constructor / call
signature — adding a DI seam to production code when one is missing.

Ported from tc-agent-zone ``scripts/checks/no_internal_patches.py`` (itself
kairix F1) and re-expressed as a configurable, repo-agnostic rule. The AST
anti-pattern detection is domain-intrinsic; the two sets that decide what
"internal" means (``internal_roots`` — patching these is the smell) and what is
a legitimate boundary fake (stdlib or an external SDK module root) is
consumer config. The engine ships NO repo package names.
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
        "rewrite the test to inject a fake (subprocess runner, filesystem "
        "adapter, etc.) through the function/class signature; if the production "
        "code lacks a DI seam, add one. Patching internal modules hides "
        "composition failures."
    ),
    nxt="re-run this check to confirm the file falls off the violator list.",
    run="python -m tc_fitness.core_checks.no_internal_patches",
    passing="runner = ScorecardRunner(subprocess_run=fake_run, fs=FakeFs(...))",
    forbidden="monkeypatch.setattr('scripts.checks.x.PATH', tmp_path)",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__is_internal__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_internal__mutmut)
def _is_internal(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.split(".", 1)[0] in internal_roots


def x__is_internal__mutmut_orig(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.split(".", 1)[0] in internal_roots


def x__is_internal__mutmut_1(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.split(None, 1)[0] in internal_roots


def x__is_internal__mutmut_2(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.split(".", None)[0] in internal_roots


def x__is_internal__mutmut_3(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.split(1)[0] in internal_roots


def x__is_internal__mutmut_4(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.split(".", )[0] in internal_roots


def x__is_internal__mutmut_5(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.rsplit(".", 1)[0] in internal_roots


def x__is_internal__mutmut_6(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.split("XX.XX", 1)[0] in internal_roots


def x__is_internal__mutmut_7(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.split(".", 2)[0] in internal_roots


def x__is_internal__mutmut_8(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.split(".", 1)[1] in internal_roots


def x__is_internal__mutmut_9(dotted: str, internal_roots: frozenset[str]) -> bool:
    return dotted.split(".", 1)[0] not in internal_roots

mutants_x__is_internal__mutmut['_mutmut_orig'] = x__is_internal__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_internal__mutmut['x__is_internal__mutmut_1'] = x__is_internal__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_internal__mutmut['x__is_internal__mutmut_2'] = x__is_internal__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_internal__mutmut['x__is_internal__mutmut_3'] = x__is_internal__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_internal__mutmut['x__is_internal__mutmut_4'] = x__is_internal__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_internal__mutmut['x__is_internal__mutmut_5'] = x__is_internal__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_internal__mutmut['x__is_internal__mutmut_6'] = x__is_internal__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_internal__mutmut['x__is_internal__mutmut_7'] = x__is_internal__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_internal__mutmut['x__is_internal__mutmut_8'] = x__is_internal__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_internal__mutmut['x__is_internal__mutmut_9'] = x__is_internal__mutmut_9 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__record_import_aliases__mutmut)
def _record_import_aliases(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_orig(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_1(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_2(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(None, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_3(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, None):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_4(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_5(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, ):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_6(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            break
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_7(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = None
        else:
            root = alias.name.split(".", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_8(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = None
            aliases[root] = root


def x__record_import_aliases__mutmut_9(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(None, 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_10(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", None)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_11(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_12(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", )[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_13(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.rsplit(".", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_14(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split("XX.XX", 1)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_15(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 2)[0]
            aliases[root] = root


def x__record_import_aliases__mutmut_16(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 1)[1]
            aliases[root] = root


def x__record_import_aliases__mutmut_17(node: ast.Import, aliases: dict[str, str], internal_roots: frozenset[str]) -> None:
    for alias in node.names:
        if not _is_internal(alias.name, internal_roots):
            continue
        if alias.asname:
            aliases[alias.asname] = alias.name
        else:
            root = alias.name.split(".", 1)[0]
            aliases[root] = None

mutants_x__record_import_aliases__mutmut['_mutmut_orig'] = x__record_import_aliases__mutmut_orig # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_1'] = x__record_import_aliases__mutmut_1 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_2'] = x__record_import_aliases__mutmut_2 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_3'] = x__record_import_aliases__mutmut_3 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_4'] = x__record_import_aliases__mutmut_4 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_5'] = x__record_import_aliases__mutmut_5 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_6'] = x__record_import_aliases__mutmut_6 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_7'] = x__record_import_aliases__mutmut_7 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_8'] = x__record_import_aliases__mutmut_8 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_9'] = x__record_import_aliases__mutmut_9 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_10'] = x__record_import_aliases__mutmut_10 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_11'] = x__record_import_aliases__mutmut_11 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_12'] = x__record_import_aliases__mutmut_12 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_13'] = x__record_import_aliases__mutmut_13 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_14'] = x__record_import_aliases__mutmut_14 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_15'] = x__record_import_aliases__mutmut_15 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_16'] = x__record_import_aliases__mutmut_16 # type: ignore # mutmut generated
mutants_x__record_import_aliases__mutmut['x__record_import_aliases__mutmut_17'] = x__record_import_aliases__mutmut_17 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__record_import_from_aliases__mutmut)
def _record_import_from_aliases(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or ""
    if not _is_internal(mod, internal_roots):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_orig(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or ""
    if not _is_internal(mod, internal_roots):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_1(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = None
    if not _is_internal(mod, internal_roots):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_2(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module and ""
    if not _is_internal(mod, internal_roots):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_3(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or "XXXX"
    if not _is_internal(mod, internal_roots):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_4(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or ""
    if _is_internal(mod, internal_roots):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_5(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or ""
    if not _is_internal(None, internal_roots):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_6(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or ""
    if not _is_internal(mod, None):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_7(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or ""
    if not _is_internal(internal_roots):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_8(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or ""
    if not _is_internal(mod, ):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_9(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or ""
    if not _is_internal(mod, internal_roots):
        return
    for alias in node.names:
        local = None
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_10(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or ""
    if not _is_internal(mod, internal_roots):
        return
    for alias in node.names:
        local = alias.asname and alias.name
        aliases[local] = f"{mod}.{alias.name}" if mod else alias.name


def x__record_import_from_aliases__mutmut_11(
    node: ast.ImportFrom, aliases: dict[str, str], internal_roots: frozenset[str]
) -> None:
    mod = node.module or ""
    if not _is_internal(mod, internal_roots):
        return
    for alias in node.names:
        local = alias.asname or alias.name
        aliases[local] = None

mutants_x__record_import_from_aliases__mutmut['_mutmut_orig'] = x__record_import_from_aliases__mutmut_orig # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_1'] = x__record_import_from_aliases__mutmut_1 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_2'] = x__record_import_from_aliases__mutmut_2 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_3'] = x__record_import_from_aliases__mutmut_3 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_4'] = x__record_import_from_aliases__mutmut_4 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_5'] = x__record_import_from_aliases__mutmut_5 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_6'] = x__record_import_from_aliases__mutmut_6 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_7'] = x__record_import_from_aliases__mutmut_7 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_8'] = x__record_import_from_aliases__mutmut_8 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_9'] = x__record_import_from_aliases__mutmut_9 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_10'] = x__record_import_from_aliases__mutmut_10 # type: ignore # mutmut generated
mutants_x__record_import_from_aliases__mutmut['x__record_import_from_aliases__mutmut_11'] = x__record_import_from_aliases__mutmut_11 # type: ignore # mutmut generated
mutants_x__resolve_internal_aliases__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__resolve_internal_aliases__mutmut)
def _resolve_internal_aliases(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_orig(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_1(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_2(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(None):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_3(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(None, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_4(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, None, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_5(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, None)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_6(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_7(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_8(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, )
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_9(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(None, aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_10(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, None, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_11(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, None)
    return aliases


def x__resolve_internal_aliases__mutmut_12(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(aliases, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_13(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, internal_roots)
    return aliases


def x__resolve_internal_aliases__mutmut_14(tree: ast.AST, internal_roots: frozenset[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            _record_import_aliases(node, aliases, internal_roots)
        elif isinstance(node, ast.ImportFrom):
            _record_import_from_aliases(node, aliases, )
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
mutants_x__is_dynamic_module_load__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_dynamic_module_load__mutmut)
def _is_dynamic_module_load(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr == "module_from_spec":
        return True
    return isinstance(func, ast.Name) and func.id == "_load"


def x__is_dynamic_module_load__mutmut_orig(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr == "module_from_spec":
        return True
    return isinstance(func, ast.Name) and func.id == "_load"


def x__is_dynamic_module_load__mutmut_1(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = None
    if isinstance(func, ast.Attribute) and func.attr == "module_from_spec":
        return True
    return isinstance(func, ast.Name) and func.id == "_load"


def x__is_dynamic_module_load__mutmut_2(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) or func.attr == "module_from_spec":
        return True
    return isinstance(func, ast.Name) and func.id == "_load"


def x__is_dynamic_module_load__mutmut_3(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr != "module_from_spec":
        return True
    return isinstance(func, ast.Name) and func.id == "_load"


def x__is_dynamic_module_load__mutmut_4(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr == "XXmodule_from_specXX":
        return True
    return isinstance(func, ast.Name) and func.id == "_load"


def x__is_dynamic_module_load__mutmut_5(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr == "MODULE_FROM_SPEC":
        return True
    return isinstance(func, ast.Name) and func.id == "_load"


def x__is_dynamic_module_load__mutmut_6(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr == "module_from_spec":
        return False
    return isinstance(func, ast.Name) and func.id == "_load"


def x__is_dynamic_module_load__mutmut_7(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr == "module_from_spec":
        return True
    return isinstance(func, ast.Name) or func.id == "_load"


def x__is_dynamic_module_load__mutmut_8(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr == "module_from_spec":
        return True
    return isinstance(func, ast.Name) and func.id != "_load"


def x__is_dynamic_module_load__mutmut_9(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr == "module_from_spec":
        return True
    return isinstance(func, ast.Name) and func.id == "XX_loadXX"


def x__is_dynamic_module_load__mutmut_10(call: ast.Call) -> bool:
    """True iff ``call`` returns a dynamically-loaded module reference.

    ``importlib.util.module_from_spec(spec)`` (canonical) or a ``_load()``
    helper (a common test-file convention). Tests that load a private module
    this way and then patch attributes on the result are the dominant theatre
    shape.
    """
    func = call.func
    if isinstance(func, ast.Attribute) and func.attr == "module_from_spec":
        return True
    return isinstance(func, ast.Name) and func.id == "_LOAD"

mutants_x__is_dynamic_module_load__mutmut['_mutmut_orig'] = x__is_dynamic_module_load__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_dynamic_module_load__mutmut['x__is_dynamic_module_load__mutmut_1'] = x__is_dynamic_module_load__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_dynamic_module_load__mutmut['x__is_dynamic_module_load__mutmut_2'] = x__is_dynamic_module_load__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_dynamic_module_load__mutmut['x__is_dynamic_module_load__mutmut_3'] = x__is_dynamic_module_load__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_dynamic_module_load__mutmut['x__is_dynamic_module_load__mutmut_4'] = x__is_dynamic_module_load__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_dynamic_module_load__mutmut['x__is_dynamic_module_load__mutmut_5'] = x__is_dynamic_module_load__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_dynamic_module_load__mutmut['x__is_dynamic_module_load__mutmut_6'] = x__is_dynamic_module_load__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_dynamic_module_load__mutmut['x__is_dynamic_module_load__mutmut_7'] = x__is_dynamic_module_load__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_dynamic_module_load__mutmut['x__is_dynamic_module_load__mutmut_8'] = x__is_dynamic_module_load__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_dynamic_module_load__mutmut['x__is_dynamic_module_load__mutmut_9'] = x__is_dynamic_module_load__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_dynamic_module_load__mutmut['x__is_dynamic_module_load__mutmut_10'] = x__is_dynamic_module_load__mutmut_10 # type: ignore # mutmut generated
mutants_x__resolve_dynamic_module_vars__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__resolve_dynamic_module_vars__mutmut)
def _resolve_dynamic_module_vars(tree: ast.AST) -> set[str]:
    dyn: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        if not _is_dynamic_module_load(node.value):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(target.id)
    return dyn


def x__resolve_dynamic_module_vars__mutmut_orig(tree: ast.AST) -> set[str]:
    dyn: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        if not _is_dynamic_module_load(node.value):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(target.id)
    return dyn


def x__resolve_dynamic_module_vars__mutmut_1(tree: ast.AST) -> set[str]:
    dyn: set[str] = None
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        if not _is_dynamic_module_load(node.value):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(target.id)
    return dyn


def x__resolve_dynamic_module_vars__mutmut_2(tree: ast.AST) -> set[str]:
    dyn: set[str] = set()
    for node in ast.walk(None):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        if not _is_dynamic_module_load(node.value):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(target.id)
    return dyn


def x__resolve_dynamic_module_vars__mutmut_3(tree: ast.AST) -> set[str]:
    dyn: set[str] = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        if not _is_dynamic_module_load(node.value):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(target.id)
    return dyn


def x__resolve_dynamic_module_vars__mutmut_4(tree: ast.AST) -> set[str]:
    dyn: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) or isinstance(node.value, ast.Call)):
            continue
        if not _is_dynamic_module_load(node.value):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(target.id)
    return dyn


def x__resolve_dynamic_module_vars__mutmut_5(tree: ast.AST) -> set[str]:
    dyn: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            break
        if not _is_dynamic_module_load(node.value):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(target.id)
    return dyn


def x__resolve_dynamic_module_vars__mutmut_6(tree: ast.AST) -> set[str]:
    dyn: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        if _is_dynamic_module_load(node.value):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(target.id)
    return dyn


def x__resolve_dynamic_module_vars__mutmut_7(tree: ast.AST) -> set[str]:
    dyn: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        if not _is_dynamic_module_load(None):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(target.id)
    return dyn


def x__resolve_dynamic_module_vars__mutmut_8(tree: ast.AST) -> set[str]:
    dyn: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        if not _is_dynamic_module_load(node.value):
            break
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(target.id)
    return dyn


def x__resolve_dynamic_module_vars__mutmut_9(tree: ast.AST) -> set[str]:
    dyn: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
            continue
        if not _is_dynamic_module_load(node.value):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                dyn.add(None)
    return dyn

mutants_x__resolve_dynamic_module_vars__mutmut['_mutmut_orig'] = x__resolve_dynamic_module_vars__mutmut_orig # type: ignore # mutmut generated
mutants_x__resolve_dynamic_module_vars__mutmut['x__resolve_dynamic_module_vars__mutmut_1'] = x__resolve_dynamic_module_vars__mutmut_1 # type: ignore # mutmut generated
mutants_x__resolve_dynamic_module_vars__mutmut['x__resolve_dynamic_module_vars__mutmut_2'] = x__resolve_dynamic_module_vars__mutmut_2 # type: ignore # mutmut generated
mutants_x__resolve_dynamic_module_vars__mutmut['x__resolve_dynamic_module_vars__mutmut_3'] = x__resolve_dynamic_module_vars__mutmut_3 # type: ignore # mutmut generated
mutants_x__resolve_dynamic_module_vars__mutmut['x__resolve_dynamic_module_vars__mutmut_4'] = x__resolve_dynamic_module_vars__mutmut_4 # type: ignore # mutmut generated
mutants_x__resolve_dynamic_module_vars__mutmut['x__resolve_dynamic_module_vars__mutmut_5'] = x__resolve_dynamic_module_vars__mutmut_5 # type: ignore # mutmut generated
mutants_x__resolve_dynamic_module_vars__mutmut['x__resolve_dynamic_module_vars__mutmut_6'] = x__resolve_dynamic_module_vars__mutmut_6 # type: ignore # mutmut generated
mutants_x__resolve_dynamic_module_vars__mutmut['x__resolve_dynamic_module_vars__mutmut_7'] = x__resolve_dynamic_module_vars__mutmut_7 # type: ignore # mutmut generated
mutants_x__resolve_dynamic_module_vars__mutmut['x__resolve_dynamic_module_vars__mutmut_8'] = x__resolve_dynamic_module_vars__mutmut_8 # type: ignore # mutmut generated
mutants_x__resolve_dynamic_module_vars__mutmut['x__resolve_dynamic_module_vars__mutmut_9'] = x__resolve_dynamic_module_vars__mutmut_9 # type: ignore # mutmut generated
mutants_x__attribute_root_name__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__attribute_root_name__mutmut)
def _attribute_root_name(node: ast.expr) -> str | None:
    cur: ast.expr = node
    while isinstance(cur, ast.Attribute):
        cur = cur.value
    if isinstance(cur, ast.Name):
        return cur.id
    return None


def x__attribute_root_name__mutmut_orig(node: ast.expr) -> str | None:
    cur: ast.expr = node
    while isinstance(cur, ast.Attribute):
        cur = cur.value
    if isinstance(cur, ast.Name):
        return cur.id
    return None


def x__attribute_root_name__mutmut_1(node: ast.expr) -> str | None:
    cur: ast.expr = None
    while isinstance(cur, ast.Attribute):
        cur = cur.value
    if isinstance(cur, ast.Name):
        return cur.id
    return None


def x__attribute_root_name__mutmut_2(node: ast.expr) -> str | None:
    cur: ast.expr = node
    while isinstance(cur, ast.Attribute):
        cur = None
    if isinstance(cur, ast.Name):
        return cur.id
    return None

mutants_x__attribute_root_name__mutmut['_mutmut_orig'] = x__attribute_root_name__mutmut_orig # type: ignore # mutmut generated
mutants_x__attribute_root_name__mutmut['x__attribute_root_name__mutmut_1'] = x__attribute_root_name__mutmut_1 # type: ignore # mutmut generated
mutants_x__attribute_root_name__mutmut['x__attribute_root_name__mutmut_2'] = x__attribute_root_name__mutmut_2 # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__name_resolves_to_internal__mutmut)
def _name_resolves_to_internal(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots or name in dyn_vars:
        return True
    return name in aliases and _is_internal(aliases[name], internal_roots)


def x__name_resolves_to_internal__mutmut_orig(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots or name in dyn_vars:
        return True
    return name in aliases and _is_internal(aliases[name], internal_roots)


def x__name_resolves_to_internal__mutmut_1(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots and name in dyn_vars:
        return True
    return name in aliases and _is_internal(aliases[name], internal_roots)


def x__name_resolves_to_internal__mutmut_2(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name not in internal_roots or name in dyn_vars:
        return True
    return name in aliases and _is_internal(aliases[name], internal_roots)


def x__name_resolves_to_internal__mutmut_3(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots or name not in dyn_vars:
        return True
    return name in aliases and _is_internal(aliases[name], internal_roots)


def x__name_resolves_to_internal__mutmut_4(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots or name in dyn_vars:
        return False
    return name in aliases and _is_internal(aliases[name], internal_roots)


def x__name_resolves_to_internal__mutmut_5(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots or name in dyn_vars:
        return True
    return name in aliases or _is_internal(aliases[name], internal_roots)


def x__name_resolves_to_internal__mutmut_6(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots or name in dyn_vars:
        return True
    return name not in aliases and _is_internal(aliases[name], internal_roots)


def x__name_resolves_to_internal__mutmut_7(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots or name in dyn_vars:
        return True
    return name in aliases and _is_internal(None, internal_roots)


def x__name_resolves_to_internal__mutmut_8(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots or name in dyn_vars:
        return True
    return name in aliases and _is_internal(aliases[name], None)


def x__name_resolves_to_internal__mutmut_9(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots or name in dyn_vars:
        return True
    return name in aliases and _is_internal(internal_roots)


def x__name_resolves_to_internal__mutmut_10(
    name: str, aliases: dict[str, str], dyn_vars: set[str], internal_roots: frozenset[str]
) -> bool:
    if name in internal_roots or name in dyn_vars:
        return True
    return name in aliases and _is_internal(aliases[name], )

mutants_x__name_resolves_to_internal__mutmut['_mutmut_orig'] = x__name_resolves_to_internal__mutmut_orig # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut['x__name_resolves_to_internal__mutmut_1'] = x__name_resolves_to_internal__mutmut_1 # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut['x__name_resolves_to_internal__mutmut_2'] = x__name_resolves_to_internal__mutmut_2 # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut['x__name_resolves_to_internal__mutmut_3'] = x__name_resolves_to_internal__mutmut_3 # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut['x__name_resolves_to_internal__mutmut_4'] = x__name_resolves_to_internal__mutmut_4 # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut['x__name_resolves_to_internal__mutmut_5'] = x__name_resolves_to_internal__mutmut_5 # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut['x__name_resolves_to_internal__mutmut_6'] = x__name_resolves_to_internal__mutmut_6 # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut['x__name_resolves_to_internal__mutmut_7'] = x__name_resolves_to_internal__mutmut_7 # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut['x__name_resolves_to_internal__mutmut_8'] = x__name_resolves_to_internal__mutmut_8 # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut['x__name_resolves_to_internal__mutmut_9'] = x__name_resolves_to_internal__mutmut_9 # type: ignore # mutmut generated
mutants_x__name_resolves_to_internal__mutmut['x__name_resolves_to_internal__mutmut_10'] = x__name_resolves_to_internal__mutmut_10 # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__root_resolves_to_internal__mutmut)
def _root_resolves_to_internal(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots or root in dyn_vars:
        return True
    return root in aliases and _is_internal(aliases[root], internal_roots)


def x__root_resolves_to_internal__mutmut_orig(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots or root in dyn_vars:
        return True
    return root in aliases and _is_internal(aliases[root], internal_roots)


def x__root_resolves_to_internal__mutmut_1(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots and root in dyn_vars:
        return True
    return root in aliases and _is_internal(aliases[root], internal_roots)


def x__root_resolves_to_internal__mutmut_2(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root not in internal_roots or root in dyn_vars:
        return True
    return root in aliases and _is_internal(aliases[root], internal_roots)


def x__root_resolves_to_internal__mutmut_3(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots or root not in dyn_vars:
        return True
    return root in aliases and _is_internal(aliases[root], internal_roots)


def x__root_resolves_to_internal__mutmut_4(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots or root in dyn_vars:
        return False
    return root in aliases and _is_internal(aliases[root], internal_roots)


def x__root_resolves_to_internal__mutmut_5(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots or root in dyn_vars:
        return True
    return root in aliases or _is_internal(aliases[root], internal_roots)


def x__root_resolves_to_internal__mutmut_6(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots or root in dyn_vars:
        return True
    return root not in aliases and _is_internal(aliases[root], internal_roots)


def x__root_resolves_to_internal__mutmut_7(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots or root in dyn_vars:
        return True
    return root in aliases and _is_internal(None, internal_roots)


def x__root_resolves_to_internal__mutmut_8(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots or root in dyn_vars:
        return True
    return root in aliases and _is_internal(aliases[root], None)


def x__root_resolves_to_internal__mutmut_9(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots or root in dyn_vars:
        return True
    return root in aliases and _is_internal(internal_roots)


def x__root_resolves_to_internal__mutmut_10(
    root: str,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if root in internal_roots or root in dyn_vars:
        return True
    return root in aliases and _is_internal(aliases[root], )

mutants_x__root_resolves_to_internal__mutmut['_mutmut_orig'] = x__root_resolves_to_internal__mutmut_orig # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut['x__root_resolves_to_internal__mutmut_1'] = x__root_resolves_to_internal__mutmut_1 # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut['x__root_resolves_to_internal__mutmut_2'] = x__root_resolves_to_internal__mutmut_2 # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut['x__root_resolves_to_internal__mutmut_3'] = x__root_resolves_to_internal__mutmut_3 # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut['x__root_resolves_to_internal__mutmut_4'] = x__root_resolves_to_internal__mutmut_4 # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut['x__root_resolves_to_internal__mutmut_5'] = x__root_resolves_to_internal__mutmut_5 # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut['x__root_resolves_to_internal__mutmut_6'] = x__root_resolves_to_internal__mutmut_6 # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut['x__root_resolves_to_internal__mutmut_7'] = x__root_resolves_to_internal__mutmut_7 # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut['x__root_resolves_to_internal__mutmut_8'] = x__root_resolves_to_internal__mutmut_8 # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut['x__root_resolves_to_internal__mutmut_9'] = x__root_resolves_to_internal__mutmut_9 # type: ignore # mutmut generated
mutants_x__root_resolves_to_internal__mutmut['x__root_resolves_to_internal__mutmut_10'] = x__root_resolves_to_internal__mutmut_10 # type: ignore # mutmut generated
mutants_x__resolves_to_internal__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__resolves_to_internal__mutmut)
def _resolves_to_internal(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_orig(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_1(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(None, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_2(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, None, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_3(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, None, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_4(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, None)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_5(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_6(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_7(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_8(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, )
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_9(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = None
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_10(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(None)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_11(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None or _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_12(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_13(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(None, aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_14(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, None, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_15(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, None, internal_roots)
    return False


def x__resolves_to_internal__mutmut_16(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, None)
    return False


def x__resolves_to_internal__mutmut_17(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(aliases, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_18(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, dyn_vars, internal_roots)
    return False


def x__resolves_to_internal__mutmut_19(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, internal_roots)
    return False


def x__resolves_to_internal__mutmut_20(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, )
    return False


def x__resolves_to_internal__mutmut_21(
    expr: ast.expr,
    aliases: dict[str, str],
    dyn_vars: set[str],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(expr, ast.Name):
        return _name_resolves_to_internal(expr.id, aliases, dyn_vars, internal_roots)
    if isinstance(expr, ast.Attribute):
        root = _attribute_root_name(expr)
        return root is not None and _root_resolves_to_internal(root, aliases, dyn_vars, internal_roots)
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
mutants_x__is_patch_call__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_patch_call__mutmut)
def _is_patch_call(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_orig(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_1(node: ast.expr) -> bool:
    if isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_2(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return True
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_3(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = None
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_4(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id != "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_5(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "XXpatchXX"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_6(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "PATCH"
    if isinstance(func, ast.Attribute):
        return func.attr == "patch"
    return False


def x__is_patch_call__mutmut_7(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr != "patch"
    return False


def x__is_patch_call__mutmut_8(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "XXpatchXX"
    return False


def x__is_patch_call__mutmut_9(node: ast.expr) -> bool:
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id == "patch"
    if isinstance(func, ast.Attribute):
        return func.attr == "PATCH"
    return False


def x__is_patch_call__mutmut_10(node: ast.expr) -> bool:
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
def _first_arg_is_internal_string(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_orig(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_1(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) and not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_2(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_3(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_4(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return True
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_5(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = None
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_6(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[1]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_7(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) or isinstance(first.value, str):
        return first.value.split(".", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_8(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(None, 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_9(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", None)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_10(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_11(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", )[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_12(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.rsplit(".", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_13(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split("XX.XX", 1)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_14(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 2)[0] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_15(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[1] in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_16(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[0] not in internal_roots
    return False


def x__first_arg_is_internal_string__mutmut_17(call: ast.expr, internal_roots: frozenset[str]) -> bool:
    if not isinstance(call, ast.Call) or not call.args:
        return False
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return first.value.split(".", 1)[0] in internal_roots
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
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_13'] = x__first_arg_is_internal_string__mutmut_13 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_14'] = x__first_arg_is_internal_string__mutmut_14 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_15'] = x__first_arg_is_internal_string__mutmut_15 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_16'] = x__first_arg_is_internal_string__mutmut_16 # type: ignore # mutmut generated
mutants_x__first_arg_is_internal_string__mutmut['x__first_arg_is_internal_string__mutmut_17'] = x__first_arg_is_internal_string__mutmut_17 # type: ignore # mutmut generated
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
mutants_x__is_pytest_raises_call__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_pytest_raises_call__mutmut)
def _is_pytest_raises_call(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "raises":
        return True
    return isinstance(func, ast.Name) and func.id == "raises"


def x__is_pytest_raises_call__mutmut_orig(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "raises":
        return True
    return isinstance(func, ast.Name) and func.id == "raises"


def x__is_pytest_raises_call__mutmut_1(ctx: ast.expr) -> bool:
    if isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "raises":
        return True
    return isinstance(func, ast.Name) and func.id == "raises"


def x__is_pytest_raises_call__mutmut_2(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return True
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "raises":
        return True
    return isinstance(func, ast.Name) and func.id == "raises"


def x__is_pytest_raises_call__mutmut_3(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = None
    if isinstance(func, ast.Attribute) and func.attr == "raises":
        return True
    return isinstance(func, ast.Name) and func.id == "raises"


def x__is_pytest_raises_call__mutmut_4(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) or func.attr == "raises":
        return True
    return isinstance(func, ast.Name) and func.id == "raises"


def x__is_pytest_raises_call__mutmut_5(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr != "raises":
        return True
    return isinstance(func, ast.Name) and func.id == "raises"


def x__is_pytest_raises_call__mutmut_6(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "XXraisesXX":
        return True
    return isinstance(func, ast.Name) and func.id == "raises"


def x__is_pytest_raises_call__mutmut_7(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "RAISES":
        return True
    return isinstance(func, ast.Name) and func.id == "raises"


def x__is_pytest_raises_call__mutmut_8(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "raises":
        return False
    return isinstance(func, ast.Name) and func.id == "raises"


def x__is_pytest_raises_call__mutmut_9(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "raises":
        return True
    return isinstance(func, ast.Name) or func.id == "raises"


def x__is_pytest_raises_call__mutmut_10(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "raises":
        return True
    return isinstance(func, ast.Name) and func.id != "raises"


def x__is_pytest_raises_call__mutmut_11(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "raises":
        return True
    return isinstance(func, ast.Name) and func.id == "XXraisesXX"


def x__is_pytest_raises_call__mutmut_12(ctx: ast.expr) -> bool:
    if not isinstance(ctx, ast.Call):
        return False
    func = ctx.func
    if isinstance(func, ast.Attribute) and func.attr == "raises":
        return True
    return isinstance(func, ast.Name) and func.id == "RAISES"

mutants_x__is_pytest_raises_call__mutmut['_mutmut_orig'] = x__is_pytest_raises_call__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_1'] = x__is_pytest_raises_call__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_2'] = x__is_pytest_raises_call__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_3'] = x__is_pytest_raises_call__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_4'] = x__is_pytest_raises_call__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_5'] = x__is_pytest_raises_call__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_6'] = x__is_pytest_raises_call__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_7'] = x__is_pytest_raises_call__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_8'] = x__is_pytest_raises_call__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_9'] = x__is_pytest_raises_call__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_10'] = x__is_pytest_raises_call__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_11'] = x__is_pytest_raises_call__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_pytest_raises_call__mutmut['x__is_pytest_raises_call__mutmut_12'] = x__is_pytest_raises_call__mutmut_12 # type: ignore # mutmut generated
mutants_x__with_block_is_pytest_raises__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__with_block_is_pytest_raises__mutmut)
def _with_block_is_pytest_raises(with_node: ast.With) -> bool:
    return any(_is_pytest_raises_call(item.context_expr) for item in with_node.items)


def x__with_block_is_pytest_raises__mutmut_orig(with_node: ast.With) -> bool:
    return any(_is_pytest_raises_call(item.context_expr) for item in with_node.items)


def x__with_block_is_pytest_raises__mutmut_1(with_node: ast.With) -> bool:
    return any(None)


def x__with_block_is_pytest_raises__mutmut_2(with_node: ast.With) -> bool:
    return any(_is_pytest_raises_call(None) for item in with_node.items)

mutants_x__with_block_is_pytest_raises__mutmut['_mutmut_orig'] = x__with_block_is_pytest_raises__mutmut_orig # type: ignore # mutmut generated
mutants_x__with_block_is_pytest_raises__mutmut['x__with_block_is_pytest_raises__mutmut_1'] = x__with_block_is_pytest_raises__mutmut_1 # type: ignore # mutmut generated
mutants_x__with_block_is_pytest_raises__mutmut['x__with_block_is_pytest_raises__mutmut_2'] = x__with_block_is_pytest_raises__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_inside_pytest_raises__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_inside_pytest_raises__mutmut)
def _is_inside_pytest_raises(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With) and _with_block_is_pytest_raises(current):
            return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_orig(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With) and _with_block_is_pytest_raises(current):
            return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_1(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    current: ast.AST | None = None
    while current is not None:
        if isinstance(current, ast.With) and _with_block_is_pytest_raises(current):
            return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_2(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    current: ast.AST | None = node
    while current is None:
        if isinstance(current, ast.With) and _with_block_is_pytest_raises(current):
            return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_3(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With) or _with_block_is_pytest_raises(current):
            return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_4(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With) and _with_block_is_pytest_raises(None):
            return True
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_5(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With) and _with_block_is_pytest_raises(current):
            return False
        current = parent_map.get(current)
    return False


def x__is_inside_pytest_raises__mutmut_6(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With) and _with_block_is_pytest_raises(current):
            return True
        current = None
    return False


def x__is_inside_pytest_raises__mutmut_7(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With) and _with_block_is_pytest_raises(current):
            return True
        current = parent_map.get(None)
    return False


def x__is_inside_pytest_raises__mutmut_8(parent_map: dict[ast.AST, ast.AST], node: ast.AST) -> bool:
    current: ast.AST | None = node
    while current is not None:
        if isinstance(current, ast.With) and _with_block_is_pytest_raises(current):
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
mutants_x__node_violates__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__node_violates__mutmut)
def _node_violates(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_orig(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_1(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            None
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_2(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) or _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_3(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(None) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_4(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(None, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_5(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, None)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_6(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_7(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, )
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_8(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return False
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_9(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            None
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_10(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr) or _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_11(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(None)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_12(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(None, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_13(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, None)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_14(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_15(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, )
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_16(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return False
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_17(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) or not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_18(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_19(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(None, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_20(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, None):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_21(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_22(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, ):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_23(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            None
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_24(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) or _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_25(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(None, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_26(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, None, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_27(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, None, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_28(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, None)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_29(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_30(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_31(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_32(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, )
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_33(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return False
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_34(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) or _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_35(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(None):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_36(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(None, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_37(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, None):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_38(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_39(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, ):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_40(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return False
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_41(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args or _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_42(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(None, aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_43(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], None, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_44(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, None, internal_roots):
            return True
    return False


def x__node_violates__mutmut_45(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, None):
            return True
    return False


def x__node_violates__mutmut_46(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_47(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_48(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, internal_roots):
            return True
    return False


def x__node_violates__mutmut_49(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, ):
            return True
    return False


def x__node_violates__mutmut_50(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[1], aliases, dyn_vars, internal_roots):
            return True
    return False


def x__node_violates__mutmut_51(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return False
    return False


def x__node_violates__mutmut_52(
    node: ast.AST,
    aliases: dict[str, str],
    dyn_vars: set[str],
    parent_map: dict[ast.AST, ast.AST],
    internal_roots: frozenset[str],
) -> bool:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        if any(
            _is_patch_call(d) and _first_arg_is_internal_string(d, internal_roots)
            for d in node.decorator_list
        ):
            return True
    if isinstance(node, ast.With):
        if any(
            _is_patch_call(item.context_expr)
            and _first_arg_is_internal_string(item.context_expr, internal_roots)
            for item in node.items
        ):
            return True
    if isinstance(node, ast.Assign) and not _is_inside_pytest_raises(parent_map, node):
        if any(
            isinstance(t, ast.Attribute) and _resolves_to_internal(t, aliases, dyn_vars, internal_roots)
            for t in node.targets
        ):
            return True
    if isinstance(node, ast.Call) and _is_monkeypatch_setattr(node):
        if _first_arg_is_internal_string(node, internal_roots):
            return True
        if node.args and _resolves_to_internal(node.args[0], aliases, dyn_vars, internal_roots):
            return True
    return True

mutants_x__node_violates__mutmut['_mutmut_orig'] = x__node_violates__mutmut_orig # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_1'] = x__node_violates__mutmut_1 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_2'] = x__node_violates__mutmut_2 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_3'] = x__node_violates__mutmut_3 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_4'] = x__node_violates__mutmut_4 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_5'] = x__node_violates__mutmut_5 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_6'] = x__node_violates__mutmut_6 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_7'] = x__node_violates__mutmut_7 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_8'] = x__node_violates__mutmut_8 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_9'] = x__node_violates__mutmut_9 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_10'] = x__node_violates__mutmut_10 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_11'] = x__node_violates__mutmut_11 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_12'] = x__node_violates__mutmut_12 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_13'] = x__node_violates__mutmut_13 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_14'] = x__node_violates__mutmut_14 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_15'] = x__node_violates__mutmut_15 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_16'] = x__node_violates__mutmut_16 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_17'] = x__node_violates__mutmut_17 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_18'] = x__node_violates__mutmut_18 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_19'] = x__node_violates__mutmut_19 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_20'] = x__node_violates__mutmut_20 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_21'] = x__node_violates__mutmut_21 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_22'] = x__node_violates__mutmut_22 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_23'] = x__node_violates__mutmut_23 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_24'] = x__node_violates__mutmut_24 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_25'] = x__node_violates__mutmut_25 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_26'] = x__node_violates__mutmut_26 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_27'] = x__node_violates__mutmut_27 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_28'] = x__node_violates__mutmut_28 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_29'] = x__node_violates__mutmut_29 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_30'] = x__node_violates__mutmut_30 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_31'] = x__node_violates__mutmut_31 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_32'] = x__node_violates__mutmut_32 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_33'] = x__node_violates__mutmut_33 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_34'] = x__node_violates__mutmut_34 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_35'] = x__node_violates__mutmut_35 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_36'] = x__node_violates__mutmut_36 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_37'] = x__node_violates__mutmut_37 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_38'] = x__node_violates__mutmut_38 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_39'] = x__node_violates__mutmut_39 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_40'] = x__node_violates__mutmut_40 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_41'] = x__node_violates__mutmut_41 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_42'] = x__node_violates__mutmut_42 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_43'] = x__node_violates__mutmut_43 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_44'] = x__node_violates__mutmut_44 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_45'] = x__node_violates__mutmut_45 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_46'] = x__node_violates__mutmut_46 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_47'] = x__node_violates__mutmut_47 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_48'] = x__node_violates__mutmut_48 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_49'] = x__node_violates__mutmut_49 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_50'] = x__node_violates__mutmut_50 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_51'] = x__node_violates__mutmut_51 # type: ignore # mutmut generated
mutants_x__node_violates__mutmut['x__node_violates__mutmut_52'] = x__node_violates__mutmut_52 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_patches_internal__mutmut)
def file_patches_internal(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_orig(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_1(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_2(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_3(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_4(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_5(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_6(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_7(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_8(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_9(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_10(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_11(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = None
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_12(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(None, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_13(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, None)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_14(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_15(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, )
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_16(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = None
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_17(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(None)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_18(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = None
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_19(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(None):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_20(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(None):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_21(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = None
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_22(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(None)


def x_file_patches_internal__mutmut_23(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(None, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_24(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, None, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_25(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, None, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_26(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, None, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_27(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, None) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_28(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_29(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, dyn_vars, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_30(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, parent_map, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_31(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, internal_roots) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_32(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, ) for node in ast.walk(tree))


def x_file_patches_internal__mutmut_33(
    path: Path,
    *,
    internal_roots: frozenset[str],
) -> bool:
    """Pure detection helper: True iff ``path`` exhibits any internal-patch shape.

    A syntax / read error is treated as "no violation" (another check owns
    unparseable files).
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    aliases = _resolve_internal_aliases(tree, internal_roots)
    dyn_vars = _resolve_dynamic_module_vars(tree)
    parent_map: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parent_map[child] = parent
    return any(_node_violates(node, aliases, dyn_vars, parent_map, internal_roots) for node in ast.walk(None))

mutants_x_file_patches_internal__mutmut['_mutmut_orig'] = x_file_patches_internal__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_1'] = x_file_patches_internal__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_2'] = x_file_patches_internal__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_3'] = x_file_patches_internal__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_4'] = x_file_patches_internal__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_5'] = x_file_patches_internal__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_6'] = x_file_patches_internal__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_7'] = x_file_patches_internal__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_8'] = x_file_patches_internal__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_9'] = x_file_patches_internal__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_10'] = x_file_patches_internal__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_11'] = x_file_patches_internal__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_12'] = x_file_patches_internal__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_13'] = x_file_patches_internal__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_14'] = x_file_patches_internal__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_15'] = x_file_patches_internal__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_16'] = x_file_patches_internal__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_17'] = x_file_patches_internal__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_18'] = x_file_patches_internal__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_19'] = x_file_patches_internal__mutmut_19 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_20'] = x_file_patches_internal__mutmut_20 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_21'] = x_file_patches_internal__mutmut_21 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_22'] = x_file_patches_internal__mutmut_22 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_23'] = x_file_patches_internal__mutmut_23 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_24'] = x_file_patches_internal__mutmut_24 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_25'] = x_file_patches_internal__mutmut_25 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_26'] = x_file_patches_internal__mutmut_26 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_27'] = x_file_patches_internal__mutmut_27 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_28'] = x_file_patches_internal__mutmut_28 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_29'] = x_file_patches_internal__mutmut_29 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_30'] = x_file_patches_internal__mutmut_30 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_31'] = x_file_patches_internal__mutmut_31 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_32'] = x_file_patches_internal__mutmut_32 # type: ignore # mutmut generated
mutants_x_file_patches_internal__mutmut['x_file_patches_internal__mutmut_33'] = x_file_patches_internal__mutmut_33 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoInternalPatchesǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoInternalPatches(FitnessRule):
    """Flags Python test files that substitute INTERNAL modules (F1)."""

    name = "no-internal-patches"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific config (instance attrs; from_config overrides per consumer).
    #: ``internal_roots`` — package roots whose patching is the smell.
    internal_roots: frozenset[str] = frozenset()

    @classmethod
    @_mutmut_mutated(mutants_xǁNoInternalPatchesǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("internal_roots", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("internal_roots", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = None
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("internal_roots", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("internal_roots", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("internal_roots", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("internal_roots", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, )
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("internal_roots", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = None
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(None)
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get(None, ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("internal_roots", None))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get(()))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("internal_roots", ))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("XXinternal_rootsXX", ()))
        return rule

    @classmethod
    def xǁNoInternalPatchesǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoInternalPatches:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoInternalPatches)  # noqa: S101  # narrowing for mypy
        rule.internal_roots = frozenset(config.get("INTERNAL_ROOTS", ()))
        return rule

    @_mutmut_mutated(mutants_xǁNoInternalPatchesǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        if not self.internal_roots:
            return False
        return file_patches_internal(
            path,
            internal_roots=self.internal_roots,
        )

    def xǁNoInternalPatchesǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        if not self.internal_roots:
            return False
        return file_patches_internal(
            path,
            internal_roots=self.internal_roots,
        )

    def xǁNoInternalPatchesǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        if self.internal_roots:
            return False
        return file_patches_internal(
            path,
            internal_roots=self.internal_roots,
        )

    def xǁNoInternalPatchesǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        if not self.internal_roots:
            return True
        return file_patches_internal(
            path,
            internal_roots=self.internal_roots,
        )

    def xǁNoInternalPatchesǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        if not self.internal_roots:
            return False
        return file_patches_internal(
            None,
            internal_roots=self.internal_roots,
        )

    def xǁNoInternalPatchesǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        if not self.internal_roots:
            return False
        return file_patches_internal(
            path,
            internal_roots=None,
        )

    def xǁNoInternalPatchesǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        if not self.internal_roots:
            return False
        return file_patches_internal(
            internal_roots=self.internal_roots,
        )

    def xǁNoInternalPatchesǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        if not self.internal_roots:
            return False
        return file_patches_internal(
            path,
            )

mutants_xǁNoInternalPatchesǁfrom_config__mutmut['_mutmut_orig'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_1'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_2'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_3'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_4'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_5'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_6'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_7'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_8'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_9'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_10'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_11'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_12'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfrom_config__mutmut['xǁNoInternalPatchesǁfrom_config__mutmut_13'] = NoInternalPatches.xǁNoInternalPatchesǁfrom_config__mutmut_13 # type: ignore # mutmut generated

mutants_xǁNoInternalPatchesǁfile_has_violation__mutmut['_mutmut_orig'] = NoInternalPatches.xǁNoInternalPatchesǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfile_has_violation__mutmut['xǁNoInternalPatchesǁfile_has_violation__mutmut_1'] = NoInternalPatches.xǁNoInternalPatchesǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfile_has_violation__mutmut['xǁNoInternalPatchesǁfile_has_violation__mutmut_2'] = NoInternalPatches.xǁNoInternalPatchesǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfile_has_violation__mutmut['xǁNoInternalPatchesǁfile_has_violation__mutmut_3'] = NoInternalPatches.xǁNoInternalPatchesǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfile_has_violation__mutmut['xǁNoInternalPatchesǁfile_has_violation__mutmut_4'] = NoInternalPatches.xǁNoInternalPatchesǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfile_has_violation__mutmut['xǁNoInternalPatchesǁfile_has_violation__mutmut_5'] = NoInternalPatches.xǁNoInternalPatchesǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoInternalPatchesǁfile_has_violation__mutmut['xǁNoInternalPatchesǁfile_has_violation__mutmut_6'] = NoInternalPatches.xǁNoInternalPatchesǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatches.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatches.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatches.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatches.from_config(config, repo_root=None)


def x_build__mutmut_3(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatches.from_config(repo_root=repo_root)


def x_build__mutmut_4(
    config: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
) -> NoInternalPatches:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return NoInternalPatches.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalPatches, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalPatches, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalPatches, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(NoInternalPatches, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
