"""CORE check: declared runtime tests execute without test doubles.

Unit and contract tests may use explicit fakes to isolate a boundary. A test
declared as an end-to-end, journey, PVT, or other runtime tier instead proves
the deployed composition. Test doubles in that tier replace the system being
claimed as evidence and make a passing result non-probative.

The consumer supplies its runtime marker vocabulary. This check rejects the
common Python double forms only inside a test carrying one of those markers:
``monkeypatch`` mutation, ``unittest.mock`` construction or patching, and
classes or constructors named ``Fake*``, ``Stub*``, or ``Mock*`` (including a
leading private underscore). It also rejects synthetic ``sys.modules`` injection.
"""

from __future__ import annotations

import ast
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from tc_fitness.core_checks import run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

REMEDIATION = _remediation(
    fix=(
        "move the test to the unit or contract tier when it deliberately uses an explicit fake; "
        "otherwise replace the double with the live deployed boundary and retain its read-back evidence."
    ),
    nxt="re-run this check to confirm the declared runtime journey is real.",
    run="python -m tc_fitness.core_checks.no_test_doubles_in_runtime_tiers",
    passing="@pytest.mark.e2e\ndef test_live():\n    assert live_client.health() == 'ready'",
    forbidden="@pytest.mark.e2e\ndef test_live(monkeypatch):\n    monkeypatch.setattr(client, 'send', fake)",
)

_MONKEYPATCH_MUTATORS = frozenset({"setattr", "setenv", "delenv", "setitem", "delitem", "delattr"})
_DOUBLE_CLASS_PREFIXES = ("Fake", "Stub", "Mock")


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__is_double_name__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_double_name__mutmut)
def _is_double_name(name: str) -> bool:
    """Return true when a private or public name identifies a test double."""
    return name.lstrip("_").startswith(_DOUBLE_CLASS_PREFIXES)


def x__is_double_name__mutmut_orig(name: str) -> bool:
    """Return true when a private or public name identifies a test double."""
    return name.lstrip("_").startswith(_DOUBLE_CLASS_PREFIXES)


def x__is_double_name__mutmut_1(name: str) -> bool:
    """Return true when a private or public name identifies a test double."""
    return name.lstrip("_").startswith(None)


def x__is_double_name__mutmut_2(name: str) -> bool:
    """Return true when a private or public name identifies a test double."""
    return name.lstrip(None).startswith(_DOUBLE_CLASS_PREFIXES)


def x__is_double_name__mutmut_3(name: str) -> bool:
    """Return true when a private or public name identifies a test double."""
    return name.rstrip("_").startswith(_DOUBLE_CLASS_PREFIXES)


def x__is_double_name__mutmut_4(name: str) -> bool:
    """Return true when a private or public name identifies a test double."""
    return name.lstrip("XX_XX").startswith(_DOUBLE_CLASS_PREFIXES)

mutants_x__is_double_name__mutmut['_mutmut_orig'] = x__is_double_name__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_double_name__mutmut['x__is_double_name__mutmut_1'] = x__is_double_name__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_double_name__mutmut['x__is_double_name__mutmut_2'] = x__is_double_name__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_double_name__mutmut['x__is_double_name__mutmut_3'] = x__is_double_name__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_double_name__mutmut['x__is_double_name__mutmut_4'] = x__is_double_name__mutmut_4 # type: ignore # mutmut generated
mutants_x__dotted_name__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__dotted_name__mutmut)
def _dotted_name(value: ast.expr) -> str | None:
    """Return a dotted syntax name without resolving import aliases."""
    if isinstance(value, ast.Name):
        return value.id
    if isinstance(value, ast.Attribute):
        parent = _dotted_name(value.value)
        return f"{parent}.{value.attr}" if parent else None
    return None


def x__dotted_name__mutmut_orig(value: ast.expr) -> str | None:
    """Return a dotted syntax name without resolving import aliases."""
    if isinstance(value, ast.Name):
        return value.id
    if isinstance(value, ast.Attribute):
        parent = _dotted_name(value.value)
        return f"{parent}.{value.attr}" if parent else None
    return None


def x__dotted_name__mutmut_1(value: ast.expr) -> str | None:
    """Return a dotted syntax name without resolving import aliases."""
    if isinstance(value, ast.Name):
        return value.id
    if isinstance(value, ast.Attribute):
        parent = None
        return f"{parent}.{value.attr}" if parent else None
    return None


def x__dotted_name__mutmut_2(value: ast.expr) -> str | None:
    """Return a dotted syntax name without resolving import aliases."""
    if isinstance(value, ast.Name):
        return value.id
    if isinstance(value, ast.Attribute):
        parent = _dotted_name(None)
        return f"{parent}.{value.attr}" if parent else None
    return None

mutants_x__dotted_name__mutmut['_mutmut_orig'] = x__dotted_name__mutmut_orig # type: ignore # mutmut generated
mutants_x__dotted_name__mutmut['x__dotted_name__mutmut_1'] = x__dotted_name__mutmut_1 # type: ignore # mutmut generated
mutants_x__dotted_name__mutmut['x__dotted_name__mutmut_2'] = x__dotted_name__mutmut_2 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__import_aliases__mutmut)
def _import_aliases(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_orig(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_1(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = None
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_2(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = None
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_3(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname and imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_4(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(None, maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_5(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=None)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_6(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_7(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", )[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_8(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.rsplit(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_9(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split("XX.XX", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_10(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=2)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_11(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[1]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_12(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = None
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_13(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) or node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_14(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name != "*":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_15(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "XX*XX":
                    continue
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_16(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    break
                aliases[imported.asname or imported.name] = f"{node.module}.{imported.name}"
    return aliases


def x__import_aliases__mutmut_17(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname or imported.name] = None
    return aliases


def x__import_aliases__mutmut_18(tree: ast.Module) -> dict[str, str]:
    """Map local import bindings to their fully-qualified package names."""
    aliases: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for imported in node.names:
                binding = imported.asname or imported.name.split(".", maxsplit=1)[0]
                aliases[binding] = imported.name if imported.asname else binding
        elif isinstance(node, ast.ImportFrom) and node.module:
            for imported in node.names:
                if imported.name == "*":
                    continue
                aliases[imported.asname and imported.name] = f"{node.module}.{imported.name}"
    return aliases

mutants_x__import_aliases__mutmut['_mutmut_orig'] = x__import_aliases__mutmut_orig # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_1'] = x__import_aliases__mutmut_1 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_2'] = x__import_aliases__mutmut_2 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_3'] = x__import_aliases__mutmut_3 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_4'] = x__import_aliases__mutmut_4 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_5'] = x__import_aliases__mutmut_5 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_6'] = x__import_aliases__mutmut_6 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_7'] = x__import_aliases__mutmut_7 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_8'] = x__import_aliases__mutmut_8 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_9'] = x__import_aliases__mutmut_9 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_10'] = x__import_aliases__mutmut_10 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_11'] = x__import_aliases__mutmut_11 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_12'] = x__import_aliases__mutmut_12 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_13'] = x__import_aliases__mutmut_13 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_14'] = x__import_aliases__mutmut_14 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_15'] = x__import_aliases__mutmut_15 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_16'] = x__import_aliases__mutmut_16 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_17'] = x__import_aliases__mutmut_17 # type: ignore # mutmut generated
mutants_x__import_aliases__mutmut['x__import_aliases__mutmut_18'] = x__import_aliases__mutmut_18 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__resolved_name__mutmut)
def _resolved_name(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root, root)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_orig(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root, root)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_1(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = None
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root, root)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_2(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(None)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root, root)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_3(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is not None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root, root)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_4(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = None
    resolved_root = aliases.get(root, root)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_5(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(None)
    resolved_root = aliases.get(root, root)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_6(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split("XX.XX")
    resolved_root = aliases.get(root, root)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_7(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = None
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_8(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(None, root)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_9(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root, None)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_10(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root)
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_11(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root, )
    return ".".join((resolved_root, *suffix))


def x__resolved_name__mutmut_12(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root, root)
    return ".".join(None)


def x__resolved_name__mutmut_13(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root, root)
    return "XX.XX".join((resolved_root, *suffix))

mutants_x__resolved_name__mutmut['_mutmut_orig'] = x__resolved_name__mutmut_orig # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_1'] = x__resolved_name__mutmut_1 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_2'] = x__resolved_name__mutmut_2 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_3'] = x__resolved_name__mutmut_3 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_4'] = x__resolved_name__mutmut_4 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_5'] = x__resolved_name__mutmut_5 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_6'] = x__resolved_name__mutmut_6 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_7'] = x__resolved_name__mutmut_7 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_8'] = x__resolved_name__mutmut_8 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_9'] = x__resolved_name__mutmut_9 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_10'] = x__resolved_name__mutmut_10 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_11'] = x__resolved_name__mutmut_11 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_12'] = x__resolved_name__mutmut_12 # type: ignore # mutmut generated
mutants_x__resolved_name__mutmut['x__resolved_name__mutmut_13'] = x__resolved_name__mutmut_13 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__marker_names__mutmut)
def _marker_names(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_orig(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_1(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(None, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_2(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, None) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_3(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_4(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, ) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_5(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(None, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_6(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, None)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_7(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_8(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, )
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_9(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = None
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_10(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(None, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_11(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, None)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_12(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_13(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, )
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_14(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved or resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_15(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith(None):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_16(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("XXpytest.mark.XX"):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_17(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("PYTEST.MARK."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_18(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(None, maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_19(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=None)[0]}
    return set()


def x__marker_names__mutmut_20(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_21(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", )[0]}
    return set()


def x__marker_names__mutmut_22(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").rsplit(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_23(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix(None).split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_24(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removesuffix("pytest.mark.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_25(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("XXpytest.mark.XX").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_26(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("PYTEST.MARK.").split(".", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_27(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split("XX.XX", maxsplit=1)[0]}
    return set()


def x__marker_names__mutmut_28(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=2)[0]}
    return set()


def x__marker_names__mutmut_29(value: ast.expr, aliases: Mapping[str, str]) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element, aliases) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func, aliases)
    resolved = _resolved_name(value, aliases)
    if resolved and resolved.startswith("pytest.mark."):
        return {resolved.removeprefix("pytest.mark.").split(".", maxsplit=1)[1]}
    return set()

mutants_x__marker_names__mutmut['_mutmut_orig'] = x__marker_names__mutmut_orig # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_1'] = x__marker_names__mutmut_1 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_2'] = x__marker_names__mutmut_2 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_3'] = x__marker_names__mutmut_3 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_4'] = x__marker_names__mutmut_4 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_5'] = x__marker_names__mutmut_5 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_6'] = x__marker_names__mutmut_6 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_7'] = x__marker_names__mutmut_7 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_8'] = x__marker_names__mutmut_8 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_9'] = x__marker_names__mutmut_9 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_10'] = x__marker_names__mutmut_10 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_11'] = x__marker_names__mutmut_11 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_12'] = x__marker_names__mutmut_12 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_13'] = x__marker_names__mutmut_13 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_14'] = x__marker_names__mutmut_14 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_15'] = x__marker_names__mutmut_15 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_16'] = x__marker_names__mutmut_16 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_17'] = x__marker_names__mutmut_17 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_18'] = x__marker_names__mutmut_18 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_19'] = x__marker_names__mutmut_19 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_20'] = x__marker_names__mutmut_20 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_21'] = x__marker_names__mutmut_21 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_22'] = x__marker_names__mutmut_22 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_23'] = x__marker_names__mutmut_23 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_24'] = x__marker_names__mutmut_24 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_25'] = x__marker_names__mutmut_25 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_26'] = x__marker_names__mutmut_26 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_27'] = x__marker_names__mutmut_27 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_28'] = x__marker_names__mutmut_28 # type: ignore # mutmut generated
mutants_x__marker_names__mutmut['x__marker_names__mutmut_29'] = x__marker_names__mutmut_29 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__module_markers__mutmut)
def _module_markers(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets):
            return _marker_names(node.value, aliases)
    return set()


def x__module_markers__mutmut_orig(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets):
            return _marker_names(node.value, aliases)
    return set()


def x__module_markers__mutmut_1(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets):
            return _marker_names(node.value, aliases)
    return set()


def x__module_markers__mutmut_2(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            break
        if any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets):
            return _marker_names(node.value, aliases)
    return set()


def x__module_markers__mutmut_3(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(None):
            return _marker_names(node.value, aliases)
    return set()


def x__module_markers__mutmut_4(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) or target.id == "pytestmark" for target in node.targets):
            return _marker_names(node.value, aliases)
    return set()


def x__module_markers__mutmut_5(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id != "pytestmark" for target in node.targets):
            return _marker_names(node.value, aliases)
    return set()


def x__module_markers__mutmut_6(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "XXpytestmarkXX" for target in node.targets):
            return _marker_names(node.value, aliases)
    return set()


def x__module_markers__mutmut_7(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "PYTESTMARK" for target in node.targets):
            return _marker_names(node.value, aliases)
    return set()


def x__module_markers__mutmut_8(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets):
            return _marker_names(None, aliases)
    return set()


def x__module_markers__mutmut_9(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets):
            return _marker_names(node.value, None)
    return set()


def x__module_markers__mutmut_10(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets):
            return _marker_names(aliases)
    return set()


def x__module_markers__mutmut_11(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets):
            return _marker_names(node.value, )
    return set()

mutants_x__module_markers__mutmut['_mutmut_orig'] = x__module_markers__mutmut_orig # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_1'] = x__module_markers__mutmut_1 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_2'] = x__module_markers__mutmut_2 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_3'] = x__module_markers__mutmut_3 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_4'] = x__module_markers__mutmut_4 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_5'] = x__module_markers__mutmut_5 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_6'] = x__module_markers__mutmut_6 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_7'] = x__module_markers__mutmut_7 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_8'] = x__module_markers__mutmut_8 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_9'] = x__module_markers__mutmut_9 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_10'] = x__module_markers__mutmut_10 # type: ignore # mutmut generated
mutants_x__module_markers__mutmut['x__module_markers__mutmut_11'] = x__module_markers__mutmut_11 # type: ignore # mutmut generated
mutants_x__function_markers__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__function_markers__mutmut)
def _function_markers(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    aliases: Mapping[str, str],
) -> set[str]:
    """Return direct pytest marker names on one test function."""
    return set().union(*(_marker_names(decorator, aliases) for decorator in node.decorator_list))


def x__function_markers__mutmut_orig(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    aliases: Mapping[str, str],
) -> set[str]:
    """Return direct pytest marker names on one test function."""
    return set().union(*(_marker_names(decorator, aliases) for decorator in node.decorator_list))


def x__function_markers__mutmut_1(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    aliases: Mapping[str, str],
) -> set[str]:
    """Return direct pytest marker names on one test function."""
    return set().union(*(_marker_names(None, aliases) for decorator in node.decorator_list))


def x__function_markers__mutmut_2(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    aliases: Mapping[str, str],
) -> set[str]:
    """Return direct pytest marker names on one test function."""
    return set().union(*(_marker_names(decorator, None) for decorator in node.decorator_list))


def x__function_markers__mutmut_3(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    aliases: Mapping[str, str],
) -> set[str]:
    """Return direct pytest marker names on one test function."""
    return set().union(*(_marker_names(aliases) for decorator in node.decorator_list))


def x__function_markers__mutmut_4(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    aliases: Mapping[str, str],
) -> set[str]:
    """Return direct pytest marker names on one test function."""
    return set().union(*(_marker_names(decorator, ) for decorator in node.decorator_list))

mutants_x__function_markers__mutmut['_mutmut_orig'] = x__function_markers__mutmut_orig # type: ignore # mutmut generated
mutants_x__function_markers__mutmut['x__function_markers__mutmut_1'] = x__function_markers__mutmut_1 # type: ignore # mutmut generated
mutants_x__function_markers__mutmut['x__function_markers__mutmut_2'] = x__function_markers__mutmut_2 # type: ignore # mutmut generated
mutants_x__function_markers__mutmut['x__function_markers__mutmut_3'] = x__function_markers__mutmut_3 # type: ignore # mutmut generated
mutants_x__function_markers__mutmut['x__function_markers__mutmut_4'] = x__function_markers__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_fixture__mutmut)
def _is_fixture(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(target, aliases) == "pytest.fixture":
            return True
    return False


def x__is_fixture__mutmut_orig(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(target, aliases) == "pytest.fixture":
            return True
    return False


def x__is_fixture__mutmut_1(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = None
        if _resolved_name(target, aliases) == "pytest.fixture":
            return True
    return False


def x__is_fixture__mutmut_2(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(None, aliases) == "pytest.fixture":
            return True
    return False


def x__is_fixture__mutmut_3(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(target, None) == "pytest.fixture":
            return True
    return False


def x__is_fixture__mutmut_4(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(aliases) == "pytest.fixture":
            return True
    return False


def x__is_fixture__mutmut_5(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(target, ) == "pytest.fixture":
            return True
    return False


def x__is_fixture__mutmut_6(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(target, aliases) != "pytest.fixture":
            return True
    return False


def x__is_fixture__mutmut_7(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(target, aliases) == "XXpytest.fixtureXX":
            return True
    return False


def x__is_fixture__mutmut_8(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(target, aliases) == "PYTEST.FIXTURE":
            return True
    return False


def x__is_fixture__mutmut_9(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(target, aliases) == "pytest.fixture":
            return False
    return False


def x__is_fixture__mutmut_10(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(target, aliases) == "pytest.fixture":
            return True
    return True

mutants_x__is_fixture__mutmut['_mutmut_orig'] = x__is_fixture__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut['x__is_fixture__mutmut_1'] = x__is_fixture__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut['x__is_fixture__mutmut_2'] = x__is_fixture__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut['x__is_fixture__mutmut_3'] = x__is_fixture__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut['x__is_fixture__mutmut_4'] = x__is_fixture__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut['x__is_fixture__mutmut_5'] = x__is_fixture__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut['x__is_fixture__mutmut_6'] = x__is_fixture__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut['x__is_fixture__mutmut_7'] = x__is_fixture__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut['x__is_fixture__mutmut_8'] = x__is_fixture__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut['x__is_fixture__mutmut_9'] = x__is_fixture__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_fixture__mutmut['x__is_fixture__mutmut_10'] = x__is_fixture__mutmut_10 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__fixture_name__mutmut)
def _fixture_name(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_orig(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_1(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) and _resolved_name(decorator.func, aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_2(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_3(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(None, aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_4(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, None) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_5(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_6(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, ) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_7(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) == "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_8(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "XXpytest.fixtureXX":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_9(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "PYTEST.FIXTURE":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_10(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "pytest.fixture":
            break
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_11(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name"
                and isinstance(keyword.value, ast.Constant) or isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_12(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "name" or isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_13(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg != "name"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_14(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "XXnameXX"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name


def x__fixture_name__mutmut_15(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> str:
    """Return the public fixture name, including an explicit pytest alias."""
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call) or _resolved_name(decorator.func, aliases) != "pytest.fixture":
            continue
        for keyword in decorator.keywords:
            if (
                keyword.arg == "NAME"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                return keyword.value.value
    return node.name

mutants_x__fixture_name__mutmut['_mutmut_orig'] = x__fixture_name__mutmut_orig # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_1'] = x__fixture_name__mutmut_1 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_2'] = x__fixture_name__mutmut_2 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_3'] = x__fixture_name__mutmut_3 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_4'] = x__fixture_name__mutmut_4 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_5'] = x__fixture_name__mutmut_5 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_6'] = x__fixture_name__mutmut_6 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_7'] = x__fixture_name__mutmut_7 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_8'] = x__fixture_name__mutmut_8 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_9'] = x__fixture_name__mutmut_9 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_10'] = x__fixture_name__mutmut_10 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_11'] = x__fixture_name__mutmut_11 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_12'] = x__fixture_name__mutmut_12 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_13'] = x__fixture_name__mutmut_13 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_14'] = x__fixture_name__mutmut_14 # type: ignore # mutmut generated
mutants_x__fixture_name__mutmut['x__fixture_name__mutmut_15'] = x__fixture_name__mutmut_15 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__autouse_fixture_names__mutmut)
def _autouse_fixture_names(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_orig(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_1(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = None
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_2(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(None):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_3(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_4(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_5(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_6(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(None, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_7(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, None):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_8(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_9(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, ):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_10(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            break
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_11(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call) and _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_12(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_13(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(None, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_14(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, None) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_15(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_16(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, ) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_17(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) == "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_18(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "XXpytest.fixtureXX"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_19(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "PYTEST.FIXTURE"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_20(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                break
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_21(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                None
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_22(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant) or keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_23(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse" or isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_24(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg != "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_25(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "XXautouseXX"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_26(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "AUTOUSE"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_27(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is not True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_28(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is False
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, aliases))
    return names


def x__autouse_fixture_names__mutmut_29(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(None)
    return names


def x__autouse_fixture_names__mutmut_30(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(None, aliases))
    return names


def x__autouse_fixture_names__mutmut_31(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, None))
    return names


def x__autouse_fixture_names__mutmut_32(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(aliases))
    return names


def x__autouse_fixture_names__mutmut_33(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return names of module fixtures that pytest supplies without an argument."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not _is_fixture(node, aliases):
            continue
        for decorator in node.decorator_list:
            if (
                not isinstance(decorator, ast.Call)
                or _resolved_name(decorator.func, aliases) != "pytest.fixture"
            ):
                continue
            if any(
                keyword.arg == "autouse"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
                for keyword in decorator.keywords
            ):
                names.add(_fixture_name(node, ))
    return names

mutants_x__autouse_fixture_names__mutmut['_mutmut_orig'] = x__autouse_fixture_names__mutmut_orig # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_1'] = x__autouse_fixture_names__mutmut_1 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_2'] = x__autouse_fixture_names__mutmut_2 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_3'] = x__autouse_fixture_names__mutmut_3 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_4'] = x__autouse_fixture_names__mutmut_4 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_5'] = x__autouse_fixture_names__mutmut_5 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_6'] = x__autouse_fixture_names__mutmut_6 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_7'] = x__autouse_fixture_names__mutmut_7 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_8'] = x__autouse_fixture_names__mutmut_8 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_9'] = x__autouse_fixture_names__mutmut_9 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_10'] = x__autouse_fixture_names__mutmut_10 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_11'] = x__autouse_fixture_names__mutmut_11 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_12'] = x__autouse_fixture_names__mutmut_12 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_13'] = x__autouse_fixture_names__mutmut_13 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_14'] = x__autouse_fixture_names__mutmut_14 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_15'] = x__autouse_fixture_names__mutmut_15 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_16'] = x__autouse_fixture_names__mutmut_16 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_17'] = x__autouse_fixture_names__mutmut_17 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_18'] = x__autouse_fixture_names__mutmut_18 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_19'] = x__autouse_fixture_names__mutmut_19 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_20'] = x__autouse_fixture_names__mutmut_20 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_21'] = x__autouse_fixture_names__mutmut_21 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_22'] = x__autouse_fixture_names__mutmut_22 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_23'] = x__autouse_fixture_names__mutmut_23 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_24'] = x__autouse_fixture_names__mutmut_24 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_25'] = x__autouse_fixture_names__mutmut_25 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_26'] = x__autouse_fixture_names__mutmut_26 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_27'] = x__autouse_fixture_names__mutmut_27 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_28'] = x__autouse_fixture_names__mutmut_28 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_29'] = x__autouse_fixture_names__mutmut_29 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_30'] = x__autouse_fixture_names__mutmut_30 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_31'] = x__autouse_fixture_names__mutmut_31 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_32'] = x__autouse_fixture_names__mutmut_32 # type: ignore # mutmut generated
mutants_x__autouse_fixture_names__mutmut['x__autouse_fixture_names__mutmut_33'] = x__autouse_fixture_names__mutmut_33 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__fixture_closure__mutmut)
def _fixture_closure(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_orig(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_1(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = None
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_2(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(None, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_3(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, None): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_4(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_5(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, ): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_6(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(None)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_7(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_8(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(None, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_9(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, None)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_10(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_11(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, )
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_12(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = None
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_13(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } & _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_14(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(None, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_15(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, None)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_16(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_17(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, )
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_18(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = None
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_19(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = None
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_20(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = None
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_21(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(None, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_22(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_23(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, )
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_24(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is not None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_25(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            break
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_26(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(None)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_27(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            None
        )
    return tuple(resolved)


def x__fixture_closure__mutmut_28(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return fixtures used directly or transitively by one runtime test."""
    fixtures = {
        _fixture_name(node, aliases): node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_fixture(node, aliases)
    }
    requested = {
        argument.arg for argument in (*test.args.posonlyargs, *test.args.args, *test.args.kwonlyargs)
    } | _autouse_fixture_names(tree, aliases)
    resolved: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    while requested:
        name = requested.pop()
        fixture = fixtures.pop(name, None)
        if fixture is None:
            continue
        resolved.append(fixture)
        requested.update(
            argument.arg
            for argument in (*fixture.args.posonlyargs, *fixture.args.args, *fixture.args.kwonlyargs)
        )
    return tuple(None)

mutants_x__fixture_closure__mutmut['_mutmut_orig'] = x__fixture_closure__mutmut_orig # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_1'] = x__fixture_closure__mutmut_1 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_2'] = x__fixture_closure__mutmut_2 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_3'] = x__fixture_closure__mutmut_3 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_4'] = x__fixture_closure__mutmut_4 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_5'] = x__fixture_closure__mutmut_5 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_6'] = x__fixture_closure__mutmut_6 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_7'] = x__fixture_closure__mutmut_7 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_8'] = x__fixture_closure__mutmut_8 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_9'] = x__fixture_closure__mutmut_9 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_10'] = x__fixture_closure__mutmut_10 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_11'] = x__fixture_closure__mutmut_11 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_12'] = x__fixture_closure__mutmut_12 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_13'] = x__fixture_closure__mutmut_13 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_14'] = x__fixture_closure__mutmut_14 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_15'] = x__fixture_closure__mutmut_15 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_16'] = x__fixture_closure__mutmut_16 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_17'] = x__fixture_closure__mutmut_17 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_18'] = x__fixture_closure__mutmut_18 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_19'] = x__fixture_closure__mutmut_19 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_20'] = x__fixture_closure__mutmut_20 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_21'] = x__fixture_closure__mutmut_21 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_22'] = x__fixture_closure__mutmut_22 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_23'] = x__fixture_closure__mutmut_23 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_24'] = x__fixture_closure__mutmut_24 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_25'] = x__fixture_closure__mutmut_25 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_26'] = x__fixture_closure__mutmut_26 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_27'] = x__fixture_closure__mutmut_27 # type: ignore # mutmut generated
mutants_x__fixture_closure__mutmut['x__fixture_closure__mutmut_28'] = x__fixture_closure__mutmut_28 # type: ignore # mutmut generated
mutants_x__function_argument_names__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__function_argument_names__mutmut)
def _function_argument_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    """Return positional and keyword-only argument names in declaration order."""
    return tuple(
        argument.arg for argument in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)
    )


def x__function_argument_names__mutmut_orig(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    """Return positional and keyword-only argument names in declaration order."""
    return tuple(
        argument.arg for argument in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)
    )


def x__function_argument_names__mutmut_1(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    """Return positional and keyword-only argument names in declaration order."""
    return tuple(
        None
    )

mutants_x__function_argument_names__mutmut['_mutmut_orig'] = x__function_argument_names__mutmut_orig # type: ignore # mutmut generated
mutants_x__function_argument_names__mutmut['x__function_argument_names__mutmut_1'] = x__function_argument_names__mutmut_1 # type: ignore # mutmut generated
mutants_x__initial_monkeypatch_names__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__initial_monkeypatch_names__mutmut)
def _initial_monkeypatch_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    """Return fixture parameters that hold pytest's monkeypatch object directly."""
    return frozenset(name for name in _function_argument_names(node) if name == "monkeypatch")


def x__initial_monkeypatch_names__mutmut_orig(node: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    """Return fixture parameters that hold pytest's monkeypatch object directly."""
    return frozenset(name for name in _function_argument_names(node) if name == "monkeypatch")


def x__initial_monkeypatch_names__mutmut_1(node: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    """Return fixture parameters that hold pytest's monkeypatch object directly."""
    return frozenset(None)


def x__initial_monkeypatch_names__mutmut_2(node: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    """Return fixture parameters that hold pytest's monkeypatch object directly."""
    return frozenset(name for name in _function_argument_names(None) if name == "monkeypatch")


def x__initial_monkeypatch_names__mutmut_3(node: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    """Return fixture parameters that hold pytest's monkeypatch object directly."""
    return frozenset(name for name in _function_argument_names(node) if name != "monkeypatch")


def x__initial_monkeypatch_names__mutmut_4(node: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    """Return fixture parameters that hold pytest's monkeypatch object directly."""
    return frozenset(name for name in _function_argument_names(node) if name == "XXmonkeypatchXX")


def x__initial_monkeypatch_names__mutmut_5(node: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    """Return fixture parameters that hold pytest's monkeypatch object directly."""
    return frozenset(name for name in _function_argument_names(node) if name == "MONKEYPATCH")

mutants_x__initial_monkeypatch_names__mutmut['_mutmut_orig'] = x__initial_monkeypatch_names__mutmut_orig # type: ignore # mutmut generated
mutants_x__initial_monkeypatch_names__mutmut['x__initial_monkeypatch_names__mutmut_1'] = x__initial_monkeypatch_names__mutmut_1 # type: ignore # mutmut generated
mutants_x__initial_monkeypatch_names__mutmut['x__initial_monkeypatch_names__mutmut_2'] = x__initial_monkeypatch_names__mutmut_2 # type: ignore # mutmut generated
mutants_x__initial_monkeypatch_names__mutmut['x__initial_monkeypatch_names__mutmut_3'] = x__initial_monkeypatch_names__mutmut_3 # type: ignore # mutmut generated
mutants_x__initial_monkeypatch_names__mutmut['x__initial_monkeypatch_names__mutmut_4'] = x__initial_monkeypatch_names__mutmut_4 # type: ignore # mutmut generated
mutants_x__initial_monkeypatch_names__mutmut['x__initial_monkeypatch_names__mutmut_5'] = x__initial_monkeypatch_names__mutmut_5 # type: ignore # mutmut generated
mutants_x__scope_bindings__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__scope_bindings__mutmut)
def _scope_bindings(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return names local to a function without descending into nested scopes."""
    bindings = set(_function_argument_names(node))

    class ScopeBindingVisitor(ast.NodeVisitor):
        def visit_Name(self, child: ast.Name) -> None:
            if isinstance(child.ctx, ast.Store):
                bindings.add(child.id)

        def visit_FunctionDef(self, child: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, child: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, child: ast.ClassDef) -> None:
            return

    visitor = ScopeBindingVisitor()
    for statement in node.body:
        visitor.visit(statement)
    return bindings


def x__scope_bindings__mutmut_orig(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return names local to a function without descending into nested scopes."""
    bindings = set(_function_argument_names(node))

    class ScopeBindingVisitor(ast.NodeVisitor):
        def visit_Name(self, child: ast.Name) -> None:
            if isinstance(child.ctx, ast.Store):
                bindings.add(child.id)

        def visit_FunctionDef(self, child: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, child: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, child: ast.ClassDef) -> None:
            return

    visitor = ScopeBindingVisitor()
    for statement in node.body:
        visitor.visit(statement)
    return bindings


def x__scope_bindings__mutmut_1(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return names local to a function without descending into nested scopes."""
    bindings = None

    class ScopeBindingVisitor(ast.NodeVisitor):
        def visit_Name(self, child: ast.Name) -> None:
            if isinstance(child.ctx, ast.Store):
                bindings.add(child.id)

        def visit_FunctionDef(self, child: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, child: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, child: ast.ClassDef) -> None:
            return

    visitor = ScopeBindingVisitor()
    for statement in node.body:
        visitor.visit(statement)
    return bindings


def x__scope_bindings__mutmut_2(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return names local to a function without descending into nested scopes."""
    bindings = set(None)

    class ScopeBindingVisitor(ast.NodeVisitor):
        def visit_Name(self, child: ast.Name) -> None:
            if isinstance(child.ctx, ast.Store):
                bindings.add(child.id)

        def visit_FunctionDef(self, child: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, child: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, child: ast.ClassDef) -> None:
            return

    visitor = ScopeBindingVisitor()
    for statement in node.body:
        visitor.visit(statement)
    return bindings


def x__scope_bindings__mutmut_3(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return names local to a function without descending into nested scopes."""
    bindings = set(_function_argument_names(None))

    class ScopeBindingVisitor(ast.NodeVisitor):
        def visit_Name(self, child: ast.Name) -> None:
            if isinstance(child.ctx, ast.Store):
                bindings.add(child.id)

        def visit_FunctionDef(self, child: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, child: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, child: ast.ClassDef) -> None:
            return

    visitor = ScopeBindingVisitor()
    for statement in node.body:
        visitor.visit(statement)
    return bindings


def x__scope_bindings__mutmut_4(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return names local to a function without descending into nested scopes."""
    bindings = set(_function_argument_names(node))

    class ScopeBindingVisitor(ast.NodeVisitor):
        def visit_Name(self, child: ast.Name) -> None:
            if isinstance(child.ctx, ast.Store):
                bindings.add(None)

        def visit_FunctionDef(self, child: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, child: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, child: ast.ClassDef) -> None:
            return

    visitor = ScopeBindingVisitor()
    for statement in node.body:
        visitor.visit(statement)
    return bindings


def x__scope_bindings__mutmut_5(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return names local to a function without descending into nested scopes."""
    bindings = set(_function_argument_names(node))

    class ScopeBindingVisitor(ast.NodeVisitor):
        def visit_Name(self, child: ast.Name) -> None:
            if isinstance(child.ctx, ast.Store):
                bindings.add(child.id)

        def visit_FunctionDef(self, child: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, child: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, child: ast.ClassDef) -> None:
            return

    visitor = None
    for statement in node.body:
        visitor.visit(statement)
    return bindings


def x__scope_bindings__mutmut_6(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return names local to a function without descending into nested scopes."""
    bindings = set(_function_argument_names(node))

    class ScopeBindingVisitor(ast.NodeVisitor):
        def visit_Name(self, child: ast.Name) -> None:
            if isinstance(child.ctx, ast.Store):
                bindings.add(child.id)

        def visit_FunctionDef(self, child: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, child: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, child: ast.ClassDef) -> None:
            return

    visitor = ScopeBindingVisitor()
    for statement in node.body:
        visitor.visit(None)
    return bindings

mutants_x__scope_bindings__mutmut['_mutmut_orig'] = x__scope_bindings__mutmut_orig # type: ignore # mutmut generated
mutants_x__scope_bindings__mutmut['x__scope_bindings__mutmut_1'] = x__scope_bindings__mutmut_1 # type: ignore # mutmut generated
mutants_x__scope_bindings__mutmut['x__scope_bindings__mutmut_2'] = x__scope_bindings__mutmut_2 # type: ignore # mutmut generated
mutants_x__scope_bindings__mutmut['x__scope_bindings__mutmut_3'] = x__scope_bindings__mutmut_3 # type: ignore # mutmut generated
mutants_x__scope_bindings__mutmut['x__scope_bindings__mutmut_4'] = x__scope_bindings__mutmut_4 # type: ignore # mutmut generated
mutants_x__scope_bindings__mutmut['x__scope_bindings__mutmut_5'] = x__scope_bindings__mutmut_5 # type: ignore # mutmut generated
mutants_x__scope_bindings__mutmut['x__scope_bindings__mutmut_6'] = x__scope_bindings__mutmut_6 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__helpers_for_runtime_test__mutmut)
def _helpers_for_runtime_test(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_orig(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_1(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = None
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_2(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_") or not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_3(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_4(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_5(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith(None)
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_6(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("XXtest_XX")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_7(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("TEST_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_8(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_9(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(None, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_10(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, None)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_11(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_12(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, )
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_13(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) and test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_14(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_15(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_16(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            break
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_17(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            None
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_18(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_") or not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_19(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_20(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_21(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith(None)
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_22(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("XXtest_XX")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_23(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("TEST_")
                and not _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_24(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and _is_fixture(node, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_25(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(None, aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_26(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, None)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_27(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(aliases)
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_28(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, )
            }
        )
        break
    return helpers


def x__helpers_for_runtime_test__mutmut_29(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    aliases: Mapping[str, str],
) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Return module helpers plus non-test methods on the test's enclosing class."""
    helpers = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("test_")
        and not _is_fixture(node, aliases)
    }
    for candidate in tree.body:
        if not isinstance(candidate, ast.ClassDef) or test not in candidate.body:
            continue
        helpers.update(
            {
                node.name: node
                for node in candidate.body
                if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
                and not node.name.startswith("test_")
                and not _is_fixture(node, aliases)
            }
        )
        return
    return helpers

mutants_x__helpers_for_runtime_test__mutmut['_mutmut_orig'] = x__helpers_for_runtime_test__mutmut_orig # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_1'] = x__helpers_for_runtime_test__mutmut_1 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_2'] = x__helpers_for_runtime_test__mutmut_2 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_3'] = x__helpers_for_runtime_test__mutmut_3 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_4'] = x__helpers_for_runtime_test__mutmut_4 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_5'] = x__helpers_for_runtime_test__mutmut_5 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_6'] = x__helpers_for_runtime_test__mutmut_6 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_7'] = x__helpers_for_runtime_test__mutmut_7 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_8'] = x__helpers_for_runtime_test__mutmut_8 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_9'] = x__helpers_for_runtime_test__mutmut_9 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_10'] = x__helpers_for_runtime_test__mutmut_10 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_11'] = x__helpers_for_runtime_test__mutmut_11 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_12'] = x__helpers_for_runtime_test__mutmut_12 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_13'] = x__helpers_for_runtime_test__mutmut_13 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_14'] = x__helpers_for_runtime_test__mutmut_14 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_15'] = x__helpers_for_runtime_test__mutmut_15 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_16'] = x__helpers_for_runtime_test__mutmut_16 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_17'] = x__helpers_for_runtime_test__mutmut_17 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_18'] = x__helpers_for_runtime_test__mutmut_18 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_19'] = x__helpers_for_runtime_test__mutmut_19 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_20'] = x__helpers_for_runtime_test__mutmut_20 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_21'] = x__helpers_for_runtime_test__mutmut_21 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_22'] = x__helpers_for_runtime_test__mutmut_22 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_23'] = x__helpers_for_runtime_test__mutmut_23 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_24'] = x__helpers_for_runtime_test__mutmut_24 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_25'] = x__helpers_for_runtime_test__mutmut_25 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_26'] = x__helpers_for_runtime_test__mutmut_26 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_27'] = x__helpers_for_runtime_test__mutmut_27 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_28'] = x__helpers_for_runtime_test__mutmut_28 # type: ignore # mutmut generated
mutants_x__helpers_for_runtime_test__mutmut['x__helpers_for_runtime_test__mutmut_29'] = x__helpers_for_runtime_test__mutmut_29 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__bound_monkeypatch_names__mutmut)
def _bound_monkeypatch_names(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_orig(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_1(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = None
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_2(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(None)
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_3(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(None))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_4(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters or parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_5(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) or parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_6(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[1] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_7(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] not in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_8(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"XXselfXX", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_9(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"SELF", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_10(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "XXclsXX"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_11(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "CLS"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_12(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = None
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_13(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[2:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_14(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = None
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_15(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(None, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_16(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, None, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_17(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=None):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_18(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_19(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_20(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, ):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_21(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=True):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_22(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) or argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_23(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id not in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_24(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(None)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_25(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name) or keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_26(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters or isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_27(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg not in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_28(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id not in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_29(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(None)
    return frozenset(bound)


def x__bound_monkeypatch_names__mutmut_30(
    call: ast.Call,
    helper: ast.FunctionDef | ast.AsyncFunctionDef,
    monkeypatch_names: frozenset[str],
) -> frozenset[str]:
    """Propagate monkeypatch identity from a helper call into its parameters."""
    parameters = list(_function_argument_names(helper))
    if isinstance(call.func, ast.Attribute) and parameters and parameters[0] in {"self", "cls"}:
        parameters = parameters[1:]
    bound: set[str] = set()
    for argument, parameter in zip(call.args, parameters, strict=False):
        if isinstance(argument, ast.Name) and argument.id in monkeypatch_names:
            bound.add(parameter)
    for keyword in call.keywords:
        if (
            keyword.arg in parameters
            and isinstance(keyword.value, ast.Name)
            and keyword.value.id in monkeypatch_names
        ):
            bound.add(keyword.arg)
    return frozenset(None)

mutants_x__bound_monkeypatch_names__mutmut['_mutmut_orig'] = x__bound_monkeypatch_names__mutmut_orig # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_1'] = x__bound_monkeypatch_names__mutmut_1 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_2'] = x__bound_monkeypatch_names__mutmut_2 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_3'] = x__bound_monkeypatch_names__mutmut_3 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_4'] = x__bound_monkeypatch_names__mutmut_4 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_5'] = x__bound_monkeypatch_names__mutmut_5 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_6'] = x__bound_monkeypatch_names__mutmut_6 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_7'] = x__bound_monkeypatch_names__mutmut_7 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_8'] = x__bound_monkeypatch_names__mutmut_8 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_9'] = x__bound_monkeypatch_names__mutmut_9 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_10'] = x__bound_monkeypatch_names__mutmut_10 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_11'] = x__bound_monkeypatch_names__mutmut_11 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_12'] = x__bound_monkeypatch_names__mutmut_12 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_13'] = x__bound_monkeypatch_names__mutmut_13 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_14'] = x__bound_monkeypatch_names__mutmut_14 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_15'] = x__bound_monkeypatch_names__mutmut_15 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_16'] = x__bound_monkeypatch_names__mutmut_16 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_17'] = x__bound_monkeypatch_names__mutmut_17 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_18'] = x__bound_monkeypatch_names__mutmut_18 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_19'] = x__bound_monkeypatch_names__mutmut_19 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_20'] = x__bound_monkeypatch_names__mutmut_20 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_21'] = x__bound_monkeypatch_names__mutmut_21 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_22'] = x__bound_monkeypatch_names__mutmut_22 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_23'] = x__bound_monkeypatch_names__mutmut_23 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_24'] = x__bound_monkeypatch_names__mutmut_24 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_25'] = x__bound_monkeypatch_names__mutmut_25 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_26'] = x__bound_monkeypatch_names__mutmut_26 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_27'] = x__bound_monkeypatch_names__mutmut_27 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_28'] = x__bound_monkeypatch_names__mutmut_28 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_29'] = x__bound_monkeypatch_names__mutmut_29 # type: ignore # mutmut generated
mutants_x__bound_monkeypatch_names__mutmut['x__bound_monkeypatch_names__mutmut_30'] = x__bound_monkeypatch_names__mutmut_30 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__in_file_helper_closure__mutmut)
def _in_file_helper_closure(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_orig(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_1(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = None

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_2(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(None, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_3(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, None, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_4(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, None)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_5(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_6(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_7(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, )

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_8(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = None
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_9(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = None
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_10(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(None)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_11(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(None):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_12(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_13(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    break
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_14(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = ""
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_15(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) or call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_16(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_17(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = None
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_18(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name) or call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_19(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute) or isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_20(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id not in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_21(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"XXselfXX", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_22(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"SELF", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_23(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "XXclsXX"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_24(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "CLS"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_25(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = None
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_26(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_27(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(None) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_28(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_29(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add(None)
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_30(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(None, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_31(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, None, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_32(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, None)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_33(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_34(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_35(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, )))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_36(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = None
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_37(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers(None)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_38(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(None)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_39(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = None
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_40(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = None
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_41(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = None
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_42(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = None
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_43(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(None), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_44(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key not in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_45(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            break
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_46(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(None)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_47(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append(None)
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_48(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(None)
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_49(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(None))
    return tuple(resolved)


def x__in_file_helper_closure__mutmut_50(
    tree: ast.Module,
    test: ast.FunctionDef | ast.AsyncFunctionDef,
    nodes: Iterable[ast.FunctionDef | ast.AsyncFunctionDef],
    aliases: Mapping[str, str],
) -> tuple[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]], ...]:
    """Return helpers called from runtime nodes with bound monkeypatch parameter names."""
    helpers = _helpers_for_runtime_test(tree, test, aliases)

    def called_helpers(
        items: Iterable[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]],
    ) -> set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]]:
        requested: set[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = set()
        for item, monkeypatch_names in items:
            local_bindings = _scope_bindings(item)
            for call in ast.walk(item):
                if not isinstance(call, ast.Call):
                    continue
                helper_name: str | None = None
                if isinstance(call.func, ast.Name) and call.func.id not in local_bindings:
                    helper_name = call.func.id
                elif (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in {"self", "cls"}
                ):
                    helper_name = call.func.attr
                helper = helpers.get(helper_name) if helper_name else None
                if helper is not None:
                    requested.add((helper, _bound_monkeypatch_names(call, helper, monkeypatch_names)))
        return requested

    requested = called_helpers((node, _initial_monkeypatch_names(node)) for node in nodes)
    resolved: list[tuple[ast.FunctionDef | ast.AsyncFunctionDef, frozenset[str]]] = []
    seen: set[tuple[int, frozenset[str]]] = set()
    while requested:
        helper, monkeypatch_names = requested.pop()
        key = (id(helper), monkeypatch_names)
        if key in seen:
            continue
        seen.add(key)
        resolved.append((helper, monkeypatch_names))
        requested.update(called_helpers(((helper, monkeypatch_names),)))
    return tuple(None)

mutants_x__in_file_helper_closure__mutmut['_mutmut_orig'] = x__in_file_helper_closure__mutmut_orig # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_1'] = x__in_file_helper_closure__mutmut_1 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_2'] = x__in_file_helper_closure__mutmut_2 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_3'] = x__in_file_helper_closure__mutmut_3 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_4'] = x__in_file_helper_closure__mutmut_4 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_5'] = x__in_file_helper_closure__mutmut_5 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_6'] = x__in_file_helper_closure__mutmut_6 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_7'] = x__in_file_helper_closure__mutmut_7 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_8'] = x__in_file_helper_closure__mutmut_8 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_9'] = x__in_file_helper_closure__mutmut_9 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_10'] = x__in_file_helper_closure__mutmut_10 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_11'] = x__in_file_helper_closure__mutmut_11 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_12'] = x__in_file_helper_closure__mutmut_12 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_13'] = x__in_file_helper_closure__mutmut_13 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_14'] = x__in_file_helper_closure__mutmut_14 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_15'] = x__in_file_helper_closure__mutmut_15 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_16'] = x__in_file_helper_closure__mutmut_16 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_17'] = x__in_file_helper_closure__mutmut_17 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_18'] = x__in_file_helper_closure__mutmut_18 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_19'] = x__in_file_helper_closure__mutmut_19 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_20'] = x__in_file_helper_closure__mutmut_20 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_21'] = x__in_file_helper_closure__mutmut_21 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_22'] = x__in_file_helper_closure__mutmut_22 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_23'] = x__in_file_helper_closure__mutmut_23 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_24'] = x__in_file_helper_closure__mutmut_24 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_25'] = x__in_file_helper_closure__mutmut_25 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_26'] = x__in_file_helper_closure__mutmut_26 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_27'] = x__in_file_helper_closure__mutmut_27 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_28'] = x__in_file_helper_closure__mutmut_28 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_29'] = x__in_file_helper_closure__mutmut_29 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_30'] = x__in_file_helper_closure__mutmut_30 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_31'] = x__in_file_helper_closure__mutmut_31 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_32'] = x__in_file_helper_closure__mutmut_32 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_33'] = x__in_file_helper_closure__mutmut_33 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_34'] = x__in_file_helper_closure__mutmut_34 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_35'] = x__in_file_helper_closure__mutmut_35 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_36'] = x__in_file_helper_closure__mutmut_36 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_37'] = x__in_file_helper_closure__mutmut_37 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_38'] = x__in_file_helper_closure__mutmut_38 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_39'] = x__in_file_helper_closure__mutmut_39 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_40'] = x__in_file_helper_closure__mutmut_40 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_41'] = x__in_file_helper_closure__mutmut_41 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_42'] = x__in_file_helper_closure__mutmut_42 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_43'] = x__in_file_helper_closure__mutmut_43 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_44'] = x__in_file_helper_closure__mutmut_44 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_45'] = x__in_file_helper_closure__mutmut_45 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_46'] = x__in_file_helper_closure__mutmut_46 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_47'] = x__in_file_helper_closure__mutmut_47 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_48'] = x__in_file_helper_closure__mutmut_48 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_49'] = x__in_file_helper_closure__mutmut_49 # type: ignore # mutmut generated
mutants_x__in_file_helper_closure__mutmut['x__in_file_helper_closure__mutmut_50'] = x__in_file_helper_closure__mutmut_50 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__call_is_test_double__mutmut)
def _call_is_test_double(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_orig(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_1(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_2(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg not in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_3(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_4(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return False
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_5(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name) or node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_6(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute) or isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_7(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id not in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_8(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr not in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_9(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = None
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_10(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(None, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_11(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, None)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_12(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_13(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, )
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_14(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved or resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_15(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith(None):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_16(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("XXunittest.mock.XX"):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_17(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("UNITTEST.MOCK."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_18(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return False
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_19(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(None)


def x__call_is_test_double__mutmut_20(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved or _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_21(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(None))


def x__call_is_test_double__mutmut_22(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(None, maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_23(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=None)[-1]))


def x__call_is_test_double__mutmut_24(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_25(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", )[-1]))


def x__call_is_test_double__mutmut_26(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.split(".", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_27(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit("XX.XX", maxsplit=1)[-1]))


def x__call_is_test_double__mutmut_28(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=2)[-1]))


def x__call_is_test_double__mutmut_29(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[+1]))


def x__call_is_test_double__mutmut_30(
    node: ast.Call,
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
    monkeypatch_names: frozenset[str],
) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if (
        isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in monkeypatch_names
    ):
        return node.func.attr in _MONKEYPATCH_MUTATORS
    resolved = _resolved_name(node.func, aliases)
    if resolved and resolved.startswith("unittest.mock."):
        return True
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-2]))

mutants_x__call_is_test_double__mutmut['_mutmut_orig'] = x__call_is_test_double__mutmut_orig # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_1'] = x__call_is_test_double__mutmut_1 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_2'] = x__call_is_test_double__mutmut_2 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_3'] = x__call_is_test_double__mutmut_3 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_4'] = x__call_is_test_double__mutmut_4 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_5'] = x__call_is_test_double__mutmut_5 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_6'] = x__call_is_test_double__mutmut_6 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_7'] = x__call_is_test_double__mutmut_7 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_8'] = x__call_is_test_double__mutmut_8 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_9'] = x__call_is_test_double__mutmut_9 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_10'] = x__call_is_test_double__mutmut_10 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_11'] = x__call_is_test_double__mutmut_11 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_12'] = x__call_is_test_double__mutmut_12 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_13'] = x__call_is_test_double__mutmut_13 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_14'] = x__call_is_test_double__mutmut_14 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_15'] = x__call_is_test_double__mutmut_15 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_16'] = x__call_is_test_double__mutmut_16 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_17'] = x__call_is_test_double__mutmut_17 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_18'] = x__call_is_test_double__mutmut_18 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_19'] = x__call_is_test_double__mutmut_19 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_20'] = x__call_is_test_double__mutmut_20 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_21'] = x__call_is_test_double__mutmut_21 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_22'] = x__call_is_test_double__mutmut_22 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_23'] = x__call_is_test_double__mutmut_23 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_24'] = x__call_is_test_double__mutmut_24 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_25'] = x__call_is_test_double__mutmut_25 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_26'] = x__call_is_test_double__mutmut_26 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_27'] = x__call_is_test_double__mutmut_27 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_28'] = x__call_is_test_double__mutmut_28 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_29'] = x__call_is_test_double__mutmut_29 # type: ignore # mutmut generated
mutants_x__call_is_test_double__mutmut['x__call_is_test_double__mutmut_30'] = x__call_is_test_double__mutmut_30 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_synthetic_module_value__mutmut)
def _is_synthetic_module_value(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_orig(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_1(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is not None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_2(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return True
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_3(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = None
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_4(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(None, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_5(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, None)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_6(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_7(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, )
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_8(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved != "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_9(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "XXtypes.ModuleTypeXX":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_10(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.moduletype":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_11(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "TYPES.MODULETYPE":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_12(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return False
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_13(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(None)
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_14(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved or _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_15(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(None))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_16(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(None, maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_17(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=None)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_18(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_19(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", )[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_20(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.split(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_21(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit("XX.XX", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_22(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=2)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_23(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[+1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_24(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-2]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_25(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(None)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_26(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = None
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_27(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(None, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_28(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, None)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_29(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_30(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, )
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_31(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(None)


def x__is_synthetic_module_value__mutmut_32(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved or _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_33(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(None))


def x__is_synthetic_module_value__mutmut_34(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(None, maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_35(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=None)[-1]))


def x__is_synthetic_module_value__mutmut_36(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_37(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", )[-1]))


def x__is_synthetic_module_value__mutmut_38(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.split(".", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_39(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit("XX.XX", maxsplit=1)[-1]))


def x__is_synthetic_module_value__mutmut_40(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=2)[-1]))


def x__is_synthetic_module_value__mutmut_41(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[+1]))


def x__is_synthetic_module_value__mutmut_42(value: ast.expr | None, aliases: Mapping[str, str]) -> bool:
    """Return true when an assigned value constructs or names a synthetic module."""
    if value is None:
        return False
    if isinstance(value, ast.Call):
        resolved = _resolved_name(value.func, aliases)
        if resolved == "types.ModuleType":
            return True
        return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-1]))
    if isinstance(value, ast.Name):
        return _is_double_name(value.id)
    resolved = _resolved_name(value, aliases)
    return bool(resolved and _is_double_name(resolved.rsplit(".", maxsplit=1)[-2]))

mutants_x__is_synthetic_module_value__mutmut['_mutmut_orig'] = x__is_synthetic_module_value__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_1'] = x__is_synthetic_module_value__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_2'] = x__is_synthetic_module_value__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_3'] = x__is_synthetic_module_value__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_4'] = x__is_synthetic_module_value__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_5'] = x__is_synthetic_module_value__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_6'] = x__is_synthetic_module_value__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_7'] = x__is_synthetic_module_value__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_8'] = x__is_synthetic_module_value__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_9'] = x__is_synthetic_module_value__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_10'] = x__is_synthetic_module_value__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_11'] = x__is_synthetic_module_value__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_12'] = x__is_synthetic_module_value__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_13'] = x__is_synthetic_module_value__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_14'] = x__is_synthetic_module_value__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_15'] = x__is_synthetic_module_value__mutmut_15 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_16'] = x__is_synthetic_module_value__mutmut_16 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_17'] = x__is_synthetic_module_value__mutmut_17 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_18'] = x__is_synthetic_module_value__mutmut_18 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_19'] = x__is_synthetic_module_value__mutmut_19 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_20'] = x__is_synthetic_module_value__mutmut_20 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_21'] = x__is_synthetic_module_value__mutmut_21 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_22'] = x__is_synthetic_module_value__mutmut_22 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_23'] = x__is_synthetic_module_value__mutmut_23 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_24'] = x__is_synthetic_module_value__mutmut_24 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_25'] = x__is_synthetic_module_value__mutmut_25 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_26'] = x__is_synthetic_module_value__mutmut_26 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_27'] = x__is_synthetic_module_value__mutmut_27 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_28'] = x__is_synthetic_module_value__mutmut_28 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_29'] = x__is_synthetic_module_value__mutmut_29 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_30'] = x__is_synthetic_module_value__mutmut_30 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_31'] = x__is_synthetic_module_value__mutmut_31 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_32'] = x__is_synthetic_module_value__mutmut_32 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_33'] = x__is_synthetic_module_value__mutmut_33 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_34'] = x__is_synthetic_module_value__mutmut_34 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_35'] = x__is_synthetic_module_value__mutmut_35 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_36'] = x__is_synthetic_module_value__mutmut_36 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_37'] = x__is_synthetic_module_value__mutmut_37 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_38'] = x__is_synthetic_module_value__mutmut_38 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_39'] = x__is_synthetic_module_value__mutmut_39 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_40'] = x__is_synthetic_module_value__mutmut_40 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_41'] = x__is_synthetic_module_value__mutmut_41 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_value__mutmut['x__is_synthetic_module_value__mutmut_42'] = x__is_synthetic_module_value__mutmut_42 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_synthetic_module_injection__mutmut)
def _is_synthetic_module_injection(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_orig(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_1(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = None
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_2(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) or any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_3(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(None, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_4(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, None) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_5(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_6(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, ) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_7(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        None
    )


def x__is_synthetic_module_injection__mutmut_8(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) or _resolved_name(target.value, aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_9(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(None, aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_10(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, None) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_11(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(aliases) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_12(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, ) == "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_13(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) != "sys.modules"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_14(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "XXsys.modulesXX"
        for target in targets
    )


def x__is_synthetic_module_injection__mutmut_15(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "SYS.MODULES"
        for target in targets
    )

mutants_x__is_synthetic_module_injection__mutmut['_mutmut_orig'] = x__is_synthetic_module_injection__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_1'] = x__is_synthetic_module_injection__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_2'] = x__is_synthetic_module_injection__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_3'] = x__is_synthetic_module_injection__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_4'] = x__is_synthetic_module_injection__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_5'] = x__is_synthetic_module_injection__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_6'] = x__is_synthetic_module_injection__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_7'] = x__is_synthetic_module_injection__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_8'] = x__is_synthetic_module_injection__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_9'] = x__is_synthetic_module_injection__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_10'] = x__is_synthetic_module_injection__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_11'] = x__is_synthetic_module_injection__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_12'] = x__is_synthetic_module_injection__mutmut_12 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_13'] = x__is_synthetic_module_injection__mutmut_13 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_14'] = x__is_synthetic_module_injection__mutmut_14 # type: ignore # mutmut generated
mutants_x__is_synthetic_module_injection__mutmut['x__is_synthetic_module_injection__mutmut_15'] = x__is_synthetic_module_injection__mutmut_15 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__nodes_contain_test_double__mutmut)
def _nodes_contain_test_double(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_orig(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_1(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(None):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_2(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) or _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_3(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(None):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_4(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return False
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_5(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) or _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_6(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(None, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_7(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, None):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_8(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_9(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, ):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_10(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return False
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_11(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) or _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_12(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                None,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_13(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=None,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_14(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=None,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_15(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=None,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_16(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_17(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_18(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_19(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                ):
                return True
    return False


def x__nodes_contain_test_double__mutmut_20(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return False
    return False


def x__nodes_contain_test_double__mutmut_21(
    nodes: Iterable[tuple[ast.AST, frozenset[str]]],
    *,
    aliases: Mapping[str, str],
    forbidden_keyword_arguments: frozenset[str],
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root, monkeypatch_names in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and _is_double_name(node.name):
                return True
            if isinstance(node, ast.Assign | ast.AnnAssign) and _is_synthetic_module_injection(node, aliases):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                aliases=aliases,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
                monkeypatch_names=monkeypatch_names,
            ):
                return True
    return True

mutants_x__nodes_contain_test_double__mutmut['_mutmut_orig'] = x__nodes_contain_test_double__mutmut_orig # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_1'] = x__nodes_contain_test_double__mutmut_1 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_2'] = x__nodes_contain_test_double__mutmut_2 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_3'] = x__nodes_contain_test_double__mutmut_3 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_4'] = x__nodes_contain_test_double__mutmut_4 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_5'] = x__nodes_contain_test_double__mutmut_5 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_6'] = x__nodes_contain_test_double__mutmut_6 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_7'] = x__nodes_contain_test_double__mutmut_7 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_8'] = x__nodes_contain_test_double__mutmut_8 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_9'] = x__nodes_contain_test_double__mutmut_9 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_10'] = x__nodes_contain_test_double__mutmut_10 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_11'] = x__nodes_contain_test_double__mutmut_11 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_12'] = x__nodes_contain_test_double__mutmut_12 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_13'] = x__nodes_contain_test_double__mutmut_13 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_14'] = x__nodes_contain_test_double__mutmut_14 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_15'] = x__nodes_contain_test_double__mutmut_15 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_16'] = x__nodes_contain_test_double__mutmut_16 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_17'] = x__nodes_contain_test_double__mutmut_17 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_18'] = x__nodes_contain_test_double__mutmut_18 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_19'] = x__nodes_contain_test_double__mutmut_19 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_20'] = x__nodes_contain_test_double__mutmut_20 # type: ignore # mutmut generated
mutants_x__nodes_contain_test_double__mutmut['x__nodes_contain_test_double__mutmut_21'] = x__nodes_contain_test_double__mutmut_21 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__runtime_tests__mutmut)
def _runtime_tests(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_orig(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_1(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = None
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_2(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(None, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_3(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, None)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_4(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_5(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, )
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_6(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = None

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_7(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(None, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_8(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, None)
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_9(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_10(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, )
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_11(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers & _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_12(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(None, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_13(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, None))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_14(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_15(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, ))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_16(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = None
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_17(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers & _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_18(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(None, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_19(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, None)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_20(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_21(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, )
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_22(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") or markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_23(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith(None) and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_24(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("XXtest_XX") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_25(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("TEST_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_26(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers | runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_27(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(None)

    visit(tree.body, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_28(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(None, module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_29(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, None)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_30(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(module_markers)
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_31(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, )
    return tuple(runtime_tests)


def x__runtime_tests__mutmut_32(
    tree: ast.Module,
    *,
    aliases: Mapping[str, str],
    runtime_markers: frozenset[str],
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ...]:
    """Return test functions carrying direct, module, or enclosing-class runtime marks."""
    module_markers = _module_markers(tree, aliases)
    runtime_tests: list[ast.FunctionDef | ast.AsyncFunctionDef] = []

    def visit(nodes: Iterable[ast.stmt], inherited_markers: set[str]) -> None:
        for node in nodes:
            if isinstance(node, ast.ClassDef):
                visit(node.body, inherited_markers | _function_markers(node, aliases))
            elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                markers = inherited_markers | _function_markers(node, aliases)
                if node.name.startswith("test_") and markers & runtime_markers:
                    runtime_tests.append(node)

    visit(tree.body, module_markers)
    return tuple(None)

mutants_x__runtime_tests__mutmut['_mutmut_orig'] = x__runtime_tests__mutmut_orig # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_1'] = x__runtime_tests__mutmut_1 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_2'] = x__runtime_tests__mutmut_2 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_3'] = x__runtime_tests__mutmut_3 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_4'] = x__runtime_tests__mutmut_4 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_5'] = x__runtime_tests__mutmut_5 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_6'] = x__runtime_tests__mutmut_6 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_7'] = x__runtime_tests__mutmut_7 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_8'] = x__runtime_tests__mutmut_8 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_9'] = x__runtime_tests__mutmut_9 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_10'] = x__runtime_tests__mutmut_10 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_11'] = x__runtime_tests__mutmut_11 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_12'] = x__runtime_tests__mutmut_12 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_13'] = x__runtime_tests__mutmut_13 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_14'] = x__runtime_tests__mutmut_14 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_15'] = x__runtime_tests__mutmut_15 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_16'] = x__runtime_tests__mutmut_16 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_17'] = x__runtime_tests__mutmut_17 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_18'] = x__runtime_tests__mutmut_18 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_19'] = x__runtime_tests__mutmut_19 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_20'] = x__runtime_tests__mutmut_20 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_21'] = x__runtime_tests__mutmut_21 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_22'] = x__runtime_tests__mutmut_22 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_23'] = x__runtime_tests__mutmut_23 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_24'] = x__runtime_tests__mutmut_24 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_25'] = x__runtime_tests__mutmut_25 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_26'] = x__runtime_tests__mutmut_26 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_27'] = x__runtime_tests__mutmut_27 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_28'] = x__runtime_tests__mutmut_28 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_29'] = x__runtime_tests__mutmut_29 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_30'] = x__runtime_tests__mutmut_30 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_31'] = x__runtime_tests__mutmut_31 # type: ignore # mutmut generated
mutants_x__runtime_tests__mutmut['x__runtime_tests__mutmut_32'] = x__runtime_tests__mutmut_32 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_has_runtime_tier_test_double__mutmut)
def file_has_runtime_tier_test_double(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_orig(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_1(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_2(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_3(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_4(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_5(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_6(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_7(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_8(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_9(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_10(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_11(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = None
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_12(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(None)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_13(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = None
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_14(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(None)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_15(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = None
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_16(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(None)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_17(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(None, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_18(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=None, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_19(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=None):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_20(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_21(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_22(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, ):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_23(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = None
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_24(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(None, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_25(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, None, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_26(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, None)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_27(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_28(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_29(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, )
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_30(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = None
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_31(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = None
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_32(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(None, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_33(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, None, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_34(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, None, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_35(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, None)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_36(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_37(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_38(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_39(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, )
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_40(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            None,
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_41(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=None,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_42(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=None,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_43(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_44(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_45(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_46(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(None)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return False


def x_file_has_runtime_tier_test_double__mutmut_47(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return False
    return False


def x_file_has_runtime_tier_test_double__mutmut_48(
    path: Path,
    *,
    runtime_markers: tuple[str, ...],
    forbidden_keyword_arguments: tuple[str, ...] = (),
) -> bool:
    """True iff a declared runtime-tier test uses a recognised test double."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    runtime = frozenset(runtime_markers)
    forbidden_keywords = frozenset(forbidden_keyword_arguments)
    aliases = _import_aliases(tree)
    for test in _runtime_tests(tree, aliases=aliases, runtime_markers=runtime):
        fixture_closure = _fixture_closure(tree, test, aliases)
        runtime_nodes = (test, *fixture_closure)
        helper_closure = _in_file_helper_closure(tree, test, runtime_nodes, aliases)
        if _nodes_contain_test_double(
            (
                *((node, _initial_monkeypatch_names(node)) for node in runtime_nodes),
                *helper_closure,
            ),
            aliases=aliases,
            forbidden_keyword_arguments=forbidden_keywords,
        ):
            return True
    return True

mutants_x_file_has_runtime_tier_test_double__mutmut['_mutmut_orig'] = x_file_has_runtime_tier_test_double__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_1'] = x_file_has_runtime_tier_test_double__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_2'] = x_file_has_runtime_tier_test_double__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_3'] = x_file_has_runtime_tier_test_double__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_4'] = x_file_has_runtime_tier_test_double__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_5'] = x_file_has_runtime_tier_test_double__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_6'] = x_file_has_runtime_tier_test_double__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_7'] = x_file_has_runtime_tier_test_double__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_8'] = x_file_has_runtime_tier_test_double__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_9'] = x_file_has_runtime_tier_test_double__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_10'] = x_file_has_runtime_tier_test_double__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_11'] = x_file_has_runtime_tier_test_double__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_12'] = x_file_has_runtime_tier_test_double__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_13'] = x_file_has_runtime_tier_test_double__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_14'] = x_file_has_runtime_tier_test_double__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_15'] = x_file_has_runtime_tier_test_double__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_16'] = x_file_has_runtime_tier_test_double__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_17'] = x_file_has_runtime_tier_test_double__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_18'] = x_file_has_runtime_tier_test_double__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_19'] = x_file_has_runtime_tier_test_double__mutmut_19 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_20'] = x_file_has_runtime_tier_test_double__mutmut_20 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_21'] = x_file_has_runtime_tier_test_double__mutmut_21 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_22'] = x_file_has_runtime_tier_test_double__mutmut_22 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_23'] = x_file_has_runtime_tier_test_double__mutmut_23 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_24'] = x_file_has_runtime_tier_test_double__mutmut_24 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_25'] = x_file_has_runtime_tier_test_double__mutmut_25 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_26'] = x_file_has_runtime_tier_test_double__mutmut_26 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_27'] = x_file_has_runtime_tier_test_double__mutmut_27 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_28'] = x_file_has_runtime_tier_test_double__mutmut_28 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_29'] = x_file_has_runtime_tier_test_double__mutmut_29 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_30'] = x_file_has_runtime_tier_test_double__mutmut_30 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_31'] = x_file_has_runtime_tier_test_double__mutmut_31 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_32'] = x_file_has_runtime_tier_test_double__mutmut_32 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_33'] = x_file_has_runtime_tier_test_double__mutmut_33 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_34'] = x_file_has_runtime_tier_test_double__mutmut_34 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_35'] = x_file_has_runtime_tier_test_double__mutmut_35 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_36'] = x_file_has_runtime_tier_test_double__mutmut_36 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_37'] = x_file_has_runtime_tier_test_double__mutmut_37 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_38'] = x_file_has_runtime_tier_test_double__mutmut_38 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_39'] = x_file_has_runtime_tier_test_double__mutmut_39 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_40'] = x_file_has_runtime_tier_test_double__mutmut_40 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_41'] = x_file_has_runtime_tier_test_double__mutmut_41 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_42'] = x_file_has_runtime_tier_test_double__mutmut_42 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_43'] = x_file_has_runtime_tier_test_double__mutmut_43 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_44'] = x_file_has_runtime_tier_test_double__mutmut_44 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_45'] = x_file_has_runtime_tier_test_double__mutmut_45 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_46'] = x_file_has_runtime_tier_test_double__mutmut_46 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_47'] = x_file_has_runtime_tier_test_double__mutmut_47 # type: ignore # mutmut generated
mutants_x_file_has_runtime_tier_test_double__mutmut['x_file_has_runtime_tier_test_double__mutmut_48'] = x_file_has_runtime_tier_test_double__mutmut_48 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore


class NoTestDoublesInRuntimeTiers(FitnessRule):
    """Rejects test doubles in tests that declare live runtime coverage."""

    name = "no-test-doubles-in-runtime-tiers"
    remediation = REMEDIATION
    extensions = (".py",)
    runtime_markers: tuple[str, ...] = ()
    forbidden_keyword_arguments: tuple[str, ...] = ()

    @classmethod
    @_mutmut_mutated(mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = None
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, )
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = None
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get(None)
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("XXruntime_markersXX")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("RUNTIME_MARKERS")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = None
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(None) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = None
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get(None)
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("XXforbidden_keyword_argumentsXX")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("FORBIDDEN_KEYWORD_ARGUMENTS")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = None
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(None) if keywords is not None else ()
        return rule

    @classmethod
    def xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> NoTestDoublesInRuntimeTiers:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, NoTestDoublesInRuntimeTiers)  # noqa: S101  # type narrowing
        markers = config.get("runtime_markers")
        rule.runtime_markers = tuple(markers) if markers is not None else ()
        keywords = config.get("forbidden_keyword_arguments")
        rule.forbidden_keyword_arguments = tuple(keywords) if keywords is None else ()
        return rule

    @_mutmut_mutated(mutants_xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        return file_has_runtime_tier_test_double(
            path,
            runtime_markers=self.runtime_markers,
            forbidden_keyword_arguments=self.forbidden_keyword_arguments,
        )

    def xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        return file_has_runtime_tier_test_double(
            path,
            runtime_markers=self.runtime_markers,
            forbidden_keyword_arguments=self.forbidden_keyword_arguments,
        )

    def xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        return file_has_runtime_tier_test_double(
            None,
            runtime_markers=self.runtime_markers,
            forbidden_keyword_arguments=self.forbidden_keyword_arguments,
        )

    def xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        return file_has_runtime_tier_test_double(
            path,
            runtime_markers=None,
            forbidden_keyword_arguments=self.forbidden_keyword_arguments,
        )

    def xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        return file_has_runtime_tier_test_double(
            path,
            runtime_markers=self.runtime_markers,
            forbidden_keyword_arguments=None,
        )

    def xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        return file_has_runtime_tier_test_double(
            runtime_markers=self.runtime_markers,
            forbidden_keyword_arguments=self.forbidden_keyword_arguments,
        )

    def xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        return file_has_runtime_tier_test_double(
            path,
            forbidden_keyword_arguments=self.forbidden_keyword_arguments,
        )

    def xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        return file_has_runtime_tier_test_double(
            path,
            runtime_markers=self.runtime_markers,
            )

mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['_mutmut_orig'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_1'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_2'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_3'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_4'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_5'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_6'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_7'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_8'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_9'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_10'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_11'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_12'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_13'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_14'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_15'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_16'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_17'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_18'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut['xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_19'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfrom_config__mutmut_19 # type: ignore # mutmut generated

mutants_xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut['_mutmut_orig'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut['xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_1'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut['xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_2'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut['xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_3'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut['xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_4'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut['xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_5'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut['xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_6'] = NoTestDoublesInRuntimeTiers.xǁNoTestDoublesInRuntimeTiersǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestDoublesInRuntimeTiers:
    """Build this consumer-configured CORE check."""
    return NoTestDoublesInRuntimeTiers.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestDoublesInRuntimeTiers:
    """Build this consumer-configured CORE check."""
    return NoTestDoublesInRuntimeTiers.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestDoublesInRuntimeTiers:
    """Build this consumer-configured CORE check."""
    return NoTestDoublesInRuntimeTiers.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestDoublesInRuntimeTiers:
    """Build this consumer-configured CORE check."""
    return NoTestDoublesInRuntimeTiers.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestDoublesInRuntimeTiers:
    """Build this consumer-configured CORE check."""
    return NoTestDoublesInRuntimeTiers.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestDoublesInRuntimeTiers:
    """Build this consumer-configured CORE check."""
    return NoTestDoublesInRuntimeTiers.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports the standard CORE check arguments."""
    return run_core_check(NoTestDoublesInRuntimeTiers, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry — supports the standard CORE check arguments."""
    return run_core_check(NoTestDoublesInRuntimeTiers, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry — supports the standard CORE check arguments."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry — supports the standard CORE check arguments."""
    return run_core_check(NoTestDoublesInRuntimeTiers, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry — supports the standard CORE check arguments."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry — supports the standard CORE check arguments."""
    return run_core_check(NoTestDoublesInRuntimeTiers, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
