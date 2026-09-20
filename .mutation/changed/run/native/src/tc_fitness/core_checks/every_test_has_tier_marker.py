"""CORE check: every-test-has-tier-marker — each test declares its tier.

An interface-driven test architecture needs every test to declare which lane
it belongs to (a fast lane on every commit, a slower lane in CI) so the tier
guarantees stay live. Without this gate, untagged tests drift into the slow
lane (or are never run). This rule flags any test file where a ``test_*``
function carries no tier marker and no module-level ``pytestmark`` pins one.
Consumers that require one primary tier for every test module can opt into
module-only classification.

Detection (AST walk per file):

  1. A module-level ``pytestmark = ...`` pinning one of the configured tier
     marker names covers every test in the file -- pass.
  2. Otherwise every ``test_*`` function must carry a matching
     ``@pytest.mark.<tier>`` decorator.
  3. A file with no ``test_*`` functions (a fixtures/support module) passes.
  4. Files below a directory carrying ``contract.yaml`` are public-contract
       fixture data, so are not independently classified as repository tests.
  5. With ``require_module_marker``, every test module must declare exactly one
     module-level tier; function-level markers alone do not satisfy the rule.

Canonical mode checks a deliberately small source grammar, not Python's
runtime semantics. Pair it with ``-p tc_fitness.pytest_tiers`` to prove that
each collected item actually has exactly one effective canonical tier.
Whether the chosen tier matches the test's reach remains a review concern.

Ported from tc-agent-zone ``scripts/checks/every_test_has_tier_marker.py``
and re-expressed as a configurable, repo-agnostic rule: scan roots and the
excluded path components arrive from config; the tier marker vocabulary is
the rule's own shape (``unit`` / ``contract`` / ``integration`` / ``e2e``)
and is overridable.
"""

from __future__ import annotations

import ast
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from tc_fitness.check_contracts import registered_contract_directory
from tc_fitness.core_checks import CORE_CHECKS, run_core_check
from tc_fitness.fitness_rule import FitnessRule
from tc_fitness.lib import remediation as _remediation

#: The default tier vocabulary -- the test-architecture's own shape, not repo
#: identity. A consumer with a different taxonomy overrides via config.
DEFAULT_TIER_MARKERS: tuple[str, ...] = ("unit", "contract", "integration", "e2e")

#: Path components that mark a support/fixture subtree to skip even when it
#: holds ``test_*.py`` files. Overridable via config.
DEFAULT_EXCLUDED_PARTS: tuple[str, ...] = ("node_modules", ".venv", "__pycache__", "fixtures")

REMEDIATION = _remediation(
    fix=(
        "add pytestmark = pytest.mark.<tier> at module level (when every test "
        "in the file shares one tier) OR decorate each test_* function with "
        "@pytest.mark.<tier>. Pick the tier by the test's reach: a pure "
        "single-unit test, a single-interface contract test, or a "
        "cross-boundary end-to-end test."
    ),
    nxt="re-run this check to confirm it goes green.",
    run="python -m tc_fitness.core_checks.every_test_has_tier_marker",
    passing="pytestmark = pytest.mark.unit  # at module level, covers every test",
    forbidden="def test_parser(): ...  # no tier marker anywhere -- drifts off every lane",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__extract_marker_names__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__extract_marker_names__mutmut)
def _extract_marker_names(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_orig(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_1(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = None
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_2(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out = _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_3(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out &= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_4(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(None)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_5(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name) or value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_6(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark" or isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_7(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute) or value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_8(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr != "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_9(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "XXmarkXX"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_10(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "MARK"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_11(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id != "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_12(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "XXpytestXX"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_13(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "PYTEST"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_14(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(None)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_15(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out = _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_16(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out &= _extract_marker_names(value.func)
        return out
    return out


def x__extract_marker_names__mutmut_17(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` attributes referenced under ``value``."""
    out: set[str] = set()
    if isinstance(value, ast.List | ast.Tuple):
        for elt in value.elts:
            out |= _extract_marker_names(elt)
        return out
    if isinstance(value, ast.Attribute):
        if (
            isinstance(value.value, ast.Attribute)
            and value.value.attr == "mark"
            and isinstance(value.value.value, ast.Name)
            and value.value.value.id == "pytest"
        ):
            out.add(value.attr)
        return out
    if isinstance(value, ast.Call):
        out |= _extract_marker_names(None)
        return out
    return out

mutants_x__extract_marker_names__mutmut['_mutmut_orig'] = x__extract_marker_names__mutmut_orig # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_1'] = x__extract_marker_names__mutmut_1 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_2'] = x__extract_marker_names__mutmut_2 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_3'] = x__extract_marker_names__mutmut_3 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_4'] = x__extract_marker_names__mutmut_4 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_5'] = x__extract_marker_names__mutmut_5 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_6'] = x__extract_marker_names__mutmut_6 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_7'] = x__extract_marker_names__mutmut_7 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_8'] = x__extract_marker_names__mutmut_8 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_9'] = x__extract_marker_names__mutmut_9 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_10'] = x__extract_marker_names__mutmut_10 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_11'] = x__extract_marker_names__mutmut_11 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_12'] = x__extract_marker_names__mutmut_12 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_13'] = x__extract_marker_names__mutmut_13 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_14'] = x__extract_marker_names__mutmut_14 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_15'] = x__extract_marker_names__mutmut_15 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_16'] = x__extract_marker_names__mutmut_16 # type: ignore # mutmut generated
mutants_x__extract_marker_names__mutmut['x__extract_marker_names__mutmut_17'] = x__extract_marker_names__mutmut_17 # type: ignore # mutmut generated
mutants_x__module_tier_marker__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__module_tier_marker__mutmut)
def _module_tier_marker(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "pytestmark":
                return _extract_marker_names(node.value) & tiers
    return set()


def x__module_tier_marker__mutmut_orig(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "pytestmark":
                return _extract_marker_names(node.value) & tiers
    return set()


def x__module_tier_marker__mutmut_1(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "pytestmark":
                return _extract_marker_names(node.value) & tiers
    return set()


def x__module_tier_marker__mutmut_2(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            break
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "pytestmark":
                return _extract_marker_names(node.value) & tiers
    return set()


def x__module_tier_marker__mutmut_3(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) or target.id == "pytestmark":
                return _extract_marker_names(node.value) & tiers
    return set()


def x__module_tier_marker__mutmut_4(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id != "pytestmark":
                return _extract_marker_names(node.value) & tiers
    return set()


def x__module_tier_marker__mutmut_5(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "XXpytestmarkXX":
                return _extract_marker_names(node.value) & tiers
    return set()


def x__module_tier_marker__mutmut_6(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "PYTESTMARK":
                return _extract_marker_names(node.value) & tiers
    return set()


def x__module_tier_marker__mutmut_7(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "pytestmark":
                return _extract_marker_names(node.value) | tiers
    return set()


def x__module_tier_marker__mutmut_8(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "pytestmark":
                return _extract_marker_names(None) & tiers
    return set()

mutants_x__module_tier_marker__mutmut['_mutmut_orig'] = x__module_tier_marker__mutmut_orig # type: ignore # mutmut generated
mutants_x__module_tier_marker__mutmut['x__module_tier_marker__mutmut_1'] = x__module_tier_marker__mutmut_1 # type: ignore # mutmut generated
mutants_x__module_tier_marker__mutmut['x__module_tier_marker__mutmut_2'] = x__module_tier_marker__mutmut_2 # type: ignore # mutmut generated
mutants_x__module_tier_marker__mutmut['x__module_tier_marker__mutmut_3'] = x__module_tier_marker__mutmut_3 # type: ignore # mutmut generated
mutants_x__module_tier_marker__mutmut['x__module_tier_marker__mutmut_4'] = x__module_tier_marker__mutmut_4 # type: ignore # mutmut generated
mutants_x__module_tier_marker__mutmut['x__module_tier_marker__mutmut_5'] = x__module_tier_marker__mutmut_5 # type: ignore # mutmut generated
mutants_x__module_tier_marker__mutmut['x__module_tier_marker__mutmut_6'] = x__module_tier_marker__mutmut_6 # type: ignore # mutmut generated
mutants_x__module_tier_marker__mutmut['x__module_tier_marker__mutmut_7'] = x__module_tier_marker__mutmut_7 # type: ignore # mutmut generated
mutants_x__module_tier_marker__mutmut['x__module_tier_marker__mutmut_8'] = x__module_tier_marker__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_pytestmark_target__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_pytestmark_target__mutmut)
def _is_pytestmark_target(target: ast.expr) -> bool:
    return isinstance(target, ast.Name) and target.id == "pytestmark"


def x__is_pytestmark_target__mutmut_orig(target: ast.expr) -> bool:
    return isinstance(target, ast.Name) and target.id == "pytestmark"


def x__is_pytestmark_target__mutmut_1(target: ast.expr) -> bool:
    return isinstance(target, ast.Name) or target.id == "pytestmark"


def x__is_pytestmark_target__mutmut_2(target: ast.expr) -> bool:
    return isinstance(target, ast.Name) and target.id != "pytestmark"


def x__is_pytestmark_target__mutmut_3(target: ast.expr) -> bool:
    return isinstance(target, ast.Name) and target.id == "XXpytestmarkXX"


def x__is_pytestmark_target__mutmut_4(target: ast.expr) -> bool:
    return isinstance(target, ast.Name) and target.id == "PYTESTMARK"

mutants_x__is_pytestmark_target__mutmut['_mutmut_orig'] = x__is_pytestmark_target__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_pytestmark_target__mutmut['x__is_pytestmark_target__mutmut_1'] = x__is_pytestmark_target__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_pytestmark_target__mutmut['x__is_pytestmark_target__mutmut_2'] = x__is_pytestmark_target__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_pytestmark_target__mutmut['x__is_pytestmark_target__mutmut_3'] = x__is_pytestmark_target__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_pytestmark_target__mutmut['x__is_pytestmark_target__mutmut_4'] = x__is_pytestmark_target__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__is_direct_tier_marker__mutmut)
def _is_direct_tier_marker(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_orig(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_1(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name) or value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_2(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark" or isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_3(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute) or value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_4(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers or isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_5(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute) or value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_6(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr not in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_7(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr != "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_8(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "XXmarkXX"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_9(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "MARK"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    )


def x__is_direct_tier_marker__mutmut_10(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id != "pytest"
    )


def x__is_direct_tier_marker__mutmut_11(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "XXpytestXX"
    )


def x__is_direct_tier_marker__mutmut_12(value: ast.expr, tiers: frozenset[str]) -> bool:
    """Accept only the static ``pytest.mark.<tier>`` declaration form."""
    return (
        isinstance(value, ast.Attribute)
        and value.attr in tiers
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "PYTEST"
    )

mutants_x__is_direct_tier_marker__mutmut['_mutmut_orig'] = x__is_direct_tier_marker__mutmut_orig # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_1'] = x__is_direct_tier_marker__mutmut_1 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_2'] = x__is_direct_tier_marker__mutmut_2 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_3'] = x__is_direct_tier_marker__mutmut_3 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_4'] = x__is_direct_tier_marker__mutmut_4 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_5'] = x__is_direct_tier_marker__mutmut_5 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_6'] = x__is_direct_tier_marker__mutmut_6 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_7'] = x__is_direct_tier_marker__mutmut_7 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_8'] = x__is_direct_tier_marker__mutmut_8 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_9'] = x__is_direct_tier_marker__mutmut_9 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_10'] = x__is_direct_tier_marker__mutmut_10 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_11'] = x__is_direct_tier_marker__mutmut_11 # type: ignore # mutmut generated
mutants_x__is_direct_tier_marker__mutmut['x__is_direct_tier_marker__mutmut_12'] = x__is_direct_tier_marker__mutmut_12 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__canonical_declaration__mutmut)
def _canonical_declaration(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_orig(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_1(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = None
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_2(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0]) or _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_3(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1 or _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_4(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign) or len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_5(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) != 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_6(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 2
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_7(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(None)
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_8(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[1])
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_9(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(None, tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_10(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, None)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_11(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(tiers)
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_12(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, )
    ]
    return declarations[0] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_13(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[1] if len(declarations) == 1 else None


def x__canonical_declaration__mutmut_14(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) != 1 else None


def x__canonical_declaration__mutmut_15(tree: ast.Module, tiers: frozenset[str]) -> ast.Assign | None:
    """Return the sole allowed primary-tier declaration, if present.

    Canonical mode intentionally does not interpret Python.  It permits just
    one literal, top-level ``pytestmark = pytest.mark.<tier>`` assignment;
    all other binding and marker syntax is examined separately and rejected.
    """
    declarations = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and _is_pytestmark_target(node.targets[0])
        and _is_direct_tier_marker(node.value, tiers)
    ]
    return declarations[0] if len(declarations) == 2 else None

mutants_x__canonical_declaration__mutmut['_mutmut_orig'] = x__canonical_declaration__mutmut_orig # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_1'] = x__canonical_declaration__mutmut_1 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_2'] = x__canonical_declaration__mutmut_2 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_3'] = x__canonical_declaration__mutmut_3 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_4'] = x__canonical_declaration__mutmut_4 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_5'] = x__canonical_declaration__mutmut_5 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_6'] = x__canonical_declaration__mutmut_6 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_7'] = x__canonical_declaration__mutmut_7 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_8'] = x__canonical_declaration__mutmut_8 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_9'] = x__canonical_declaration__mutmut_9 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_10'] = x__canonical_declaration__mutmut_10 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_11'] = x__canonical_declaration__mutmut_11 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_12'] = x__canonical_declaration__mutmut_12 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_13'] = x__canonical_declaration__mutmut_13 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_14'] = x__canonical_declaration__mutmut_14 # type: ignore # mutmut generated
mutants_x__canonical_declaration__mutmut['x__canonical_declaration__mutmut_15'] = x__canonical_declaration__mutmut_15 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__uses_pytestmark__mutmut)
def _uses_pytestmark(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_orig(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_1(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" or node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_2(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id != "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_3(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "XXpytestmarkXX" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_4(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "PYTESTMARK" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_5(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_6(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" and (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_7(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname != "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_8(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "XXpytestmarkXX" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_9(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "PYTESTMARK" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_10(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None or node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_11(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is not None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_12(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(None, maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_13(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=None)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_14(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_15(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", )[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_16(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.rsplit(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_17(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split("XX.XX", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_18(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=2)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_19(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[1] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_20(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] != "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_21(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "XXpytestmarkXX"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_22(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "PYTESTMARK"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_23(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg != "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_24(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "XXpytestmarkXX"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_25(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "PYTESTMARK"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_26(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name != "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_27(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "XXpytestmarkXX"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_28(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "PYTESTMARK"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_29(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name != "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_30(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "XXpytestmarkXX"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_31(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "PYTESTMARK"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_32(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest != "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_33(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "XXpytestmarkXX"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_34(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "PYTESTMARK"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_35(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name != "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_36(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "XXpytestmarkXX"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_37(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "PYTESTMARK"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_38(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"} or getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_39(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(None).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_40(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ not in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_41(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"XXTypeVarXX", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_42(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"typevar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_43(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TYPEVAR", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_44(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "XXParamSpecXX", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_45(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "paramspec", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_46(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "PARAMSPEC", "TypeVarTuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_47(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "XXTypeVarTupleXX"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_48(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "typevartuple"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_49(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TYPEVARTUPLE"}
        and getattr(node, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_50(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(None, "name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_51(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, None, None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_52(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr("name", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_53(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_54(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", ) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_55(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "XXnameXX", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_56(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "NAME", None) == "pytestmark"
    )


def x__uses_pytestmark__mutmut_57(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) != "pytestmark"
    )


def x__uses_pytestmark__mutmut_58(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "XXpytestmarkXX"
    )


def x__uses_pytestmark__mutmut_59(node: ast.AST, allowed_target: ast.expr) -> bool:
    """Reserve pytestmark for the sole declaration, including bare reads."""
    if isinstance(node, ast.Name):
        return node.id == "pytestmark" and node is not allowed_target
    if isinstance(node, ast.alias):
        return node.asname == "pytestmark" or (
            node.asname is None and node.name.split(".", maxsplit=1)[0] == "pytestmark"
        )
    if isinstance(node, ast.arg):
        return node.arg == "pytestmark"
    if isinstance(node, ast.ExceptHandler):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchAs | ast.MatchStar):
        return node.name == "pytestmark"
    if isinstance(node, ast.MatchMapping):
        return node.rest == "pytestmark"
    if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
        return node.name == "pytestmark"
    return (
        type(node).__name__ in {"TypeVar", "ParamSpec", "TypeVarTuple"}
        and getattr(node, "name", None) == "PYTESTMARK"
    )

mutants_x__uses_pytestmark__mutmut['_mutmut_orig'] = x__uses_pytestmark__mutmut_orig # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_1'] = x__uses_pytestmark__mutmut_1 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_2'] = x__uses_pytestmark__mutmut_2 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_3'] = x__uses_pytestmark__mutmut_3 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_4'] = x__uses_pytestmark__mutmut_4 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_5'] = x__uses_pytestmark__mutmut_5 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_6'] = x__uses_pytestmark__mutmut_6 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_7'] = x__uses_pytestmark__mutmut_7 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_8'] = x__uses_pytestmark__mutmut_8 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_9'] = x__uses_pytestmark__mutmut_9 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_10'] = x__uses_pytestmark__mutmut_10 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_11'] = x__uses_pytestmark__mutmut_11 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_12'] = x__uses_pytestmark__mutmut_12 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_13'] = x__uses_pytestmark__mutmut_13 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_14'] = x__uses_pytestmark__mutmut_14 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_15'] = x__uses_pytestmark__mutmut_15 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_16'] = x__uses_pytestmark__mutmut_16 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_17'] = x__uses_pytestmark__mutmut_17 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_18'] = x__uses_pytestmark__mutmut_18 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_19'] = x__uses_pytestmark__mutmut_19 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_20'] = x__uses_pytestmark__mutmut_20 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_21'] = x__uses_pytestmark__mutmut_21 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_22'] = x__uses_pytestmark__mutmut_22 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_23'] = x__uses_pytestmark__mutmut_23 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_24'] = x__uses_pytestmark__mutmut_24 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_25'] = x__uses_pytestmark__mutmut_25 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_26'] = x__uses_pytestmark__mutmut_26 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_27'] = x__uses_pytestmark__mutmut_27 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_28'] = x__uses_pytestmark__mutmut_28 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_29'] = x__uses_pytestmark__mutmut_29 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_30'] = x__uses_pytestmark__mutmut_30 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_31'] = x__uses_pytestmark__mutmut_31 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_32'] = x__uses_pytestmark__mutmut_32 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_33'] = x__uses_pytestmark__mutmut_33 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_34'] = x__uses_pytestmark__mutmut_34 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_35'] = x__uses_pytestmark__mutmut_35 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_36'] = x__uses_pytestmark__mutmut_36 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_37'] = x__uses_pytestmark__mutmut_37 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_38'] = x__uses_pytestmark__mutmut_38 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_39'] = x__uses_pytestmark__mutmut_39 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_40'] = x__uses_pytestmark__mutmut_40 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_41'] = x__uses_pytestmark__mutmut_41 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_42'] = x__uses_pytestmark__mutmut_42 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_43'] = x__uses_pytestmark__mutmut_43 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_44'] = x__uses_pytestmark__mutmut_44 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_45'] = x__uses_pytestmark__mutmut_45 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_46'] = x__uses_pytestmark__mutmut_46 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_47'] = x__uses_pytestmark__mutmut_47 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_48'] = x__uses_pytestmark__mutmut_48 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_49'] = x__uses_pytestmark__mutmut_49 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_50'] = x__uses_pytestmark__mutmut_50 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_51'] = x__uses_pytestmark__mutmut_51 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_52'] = x__uses_pytestmark__mutmut_52 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_53'] = x__uses_pytestmark__mutmut_53 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_54'] = x__uses_pytestmark__mutmut_54 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_55'] = x__uses_pytestmark__mutmut_55 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_56'] = x__uses_pytestmark__mutmut_56 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_57'] = x__uses_pytestmark__mutmut_57 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_58'] = x__uses_pytestmark__mutmut_58 # type: ignore # mutmut generated
mutants_x__uses_pytestmark__mutmut['x__uses_pytestmark__mutmut_59'] = x__uses_pytestmark__mutmut_59 # type: ignore # mutmut generated
mutants_x__has_unallowed_pytestmark_use__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_unallowed_pytestmark_use__mutmut)
def _has_unallowed_pytestmark_use(tree: ast.Module, declaration: ast.Assign) -> bool:
    return any(_uses_pytestmark(node, declaration.targets[0]) for node in ast.walk(tree))


def x__has_unallowed_pytestmark_use__mutmut_orig(tree: ast.Module, declaration: ast.Assign) -> bool:
    return any(_uses_pytestmark(node, declaration.targets[0]) for node in ast.walk(tree))


def x__has_unallowed_pytestmark_use__mutmut_1(tree: ast.Module, declaration: ast.Assign) -> bool:
    return any(None)


def x__has_unallowed_pytestmark_use__mutmut_2(tree: ast.Module, declaration: ast.Assign) -> bool:
    return any(_uses_pytestmark(None, declaration.targets[0]) for node in ast.walk(tree))


def x__has_unallowed_pytestmark_use__mutmut_3(tree: ast.Module, declaration: ast.Assign) -> bool:
    return any(_uses_pytestmark(node, None) for node in ast.walk(tree))


def x__has_unallowed_pytestmark_use__mutmut_4(tree: ast.Module, declaration: ast.Assign) -> bool:
    return any(_uses_pytestmark(declaration.targets[0]) for node in ast.walk(tree))


def x__has_unallowed_pytestmark_use__mutmut_5(tree: ast.Module, declaration: ast.Assign) -> bool:
    return any(_uses_pytestmark(node, ) for node in ast.walk(tree))


def x__has_unallowed_pytestmark_use__mutmut_6(tree: ast.Module, declaration: ast.Assign) -> bool:
    return any(_uses_pytestmark(node, declaration.targets[1]) for node in ast.walk(tree))


def x__has_unallowed_pytestmark_use__mutmut_7(tree: ast.Module, declaration: ast.Assign) -> bool:
    return any(_uses_pytestmark(node, declaration.targets[0]) for node in ast.walk(None))

mutants_x__has_unallowed_pytestmark_use__mutmut['_mutmut_orig'] = x__has_unallowed_pytestmark_use__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_unallowed_pytestmark_use__mutmut['x__has_unallowed_pytestmark_use__mutmut_1'] = x__has_unallowed_pytestmark_use__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_unallowed_pytestmark_use__mutmut['x__has_unallowed_pytestmark_use__mutmut_2'] = x__has_unallowed_pytestmark_use__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_unallowed_pytestmark_use__mutmut['x__has_unallowed_pytestmark_use__mutmut_3'] = x__has_unallowed_pytestmark_use__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_unallowed_pytestmark_use__mutmut['x__has_unallowed_pytestmark_use__mutmut_4'] = x__has_unallowed_pytestmark_use__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_unallowed_pytestmark_use__mutmut['x__has_unallowed_pytestmark_use__mutmut_5'] = x__has_unallowed_pytestmark_use__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_unallowed_pytestmark_use__mutmut['x__has_unallowed_pytestmark_use__mutmut_6'] = x__has_unallowed_pytestmark_use__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_unallowed_pytestmark_use__mutmut['x__has_unallowed_pytestmark_use__mutmut_7'] = x__has_unallowed_pytestmark_use__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_marker_namespace_alias__mutmut)
def _has_marker_namespace_alias(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_orig(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_1(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_2(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(None) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_3(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(None)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_4(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(None):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_5(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(None):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_6(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" or alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_7(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name != "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_8(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "XXpytestXX" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_9(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "PYTEST" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_10(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_11(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return False
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_12(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) or node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_13(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module != "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_14(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "XXpytestXX":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_15(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "PYTEST":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_16(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(None):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_17(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name not in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_18(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"XXmarkXX", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_19(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"MARK", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_20(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "XX*XX"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_21(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return False
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_22(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = None
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_23(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) or node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_24(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id != "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_25(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "XXpytestXX"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_26(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "PYTEST"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_27(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = None
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_28(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name) or node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_29(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark" or isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_30(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute) or node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_31(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr != "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_32(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "XXmarkXX"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_33(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "MARK"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_34(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id != "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_35(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "XXpytestXX"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_36(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "PYTEST"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_37(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest and is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_38(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = None
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_39(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(None)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_40(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) and parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_41(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_42(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is node:
                return True
    return False


def x__has_marker_namespace_alias__mutmut_43(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return False
    return False


def x__has_marker_namespace_alias__mutmut_44(tree: ast.Module) -> bool:
    """Require direct pytest namespace access; never resolve alias chains.

    ``pytest`` and ``pytest.mark`` must be the receiver of an attribute, not
    a value copied/passed elsewhere. Marker imports must use ``import pytest``.
    Unrelated attributes such as ``documents.contract`` remain ordinary code.
    Imported helper semantics and reflection belong to collection assurance.
    """
    parents = {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pytest" and alias.asname is not None for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pytest":
            if any(alias.name in {"mark", "*"} for alias in node.names):
                return True
        is_pytest = isinstance(node, ast.Name) and node.id == "pytest"
        is_mark = (
            isinstance(node, ast.Attribute)
            and node.attr == "mark"
            and isinstance(node.value, ast.Name)
            and node.value.id == "pytest"
        )
        if is_pytest or is_mark:
            parent = parents.get(node)
            if not isinstance(parent, ast.Attribute) or parent.value is not node:
                return True
    return True

mutants_x__has_marker_namespace_alias__mutmut['_mutmut_orig'] = x__has_marker_namespace_alias__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_1'] = x__has_marker_namespace_alias__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_2'] = x__has_marker_namespace_alias__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_3'] = x__has_marker_namespace_alias__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_4'] = x__has_marker_namespace_alias__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_5'] = x__has_marker_namespace_alias__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_6'] = x__has_marker_namespace_alias__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_7'] = x__has_marker_namespace_alias__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_8'] = x__has_marker_namespace_alias__mutmut_8 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_9'] = x__has_marker_namespace_alias__mutmut_9 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_10'] = x__has_marker_namespace_alias__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_11'] = x__has_marker_namespace_alias__mutmut_11 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_12'] = x__has_marker_namespace_alias__mutmut_12 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_13'] = x__has_marker_namespace_alias__mutmut_13 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_14'] = x__has_marker_namespace_alias__mutmut_14 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_15'] = x__has_marker_namespace_alias__mutmut_15 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_16'] = x__has_marker_namespace_alias__mutmut_16 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_17'] = x__has_marker_namespace_alias__mutmut_17 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_18'] = x__has_marker_namespace_alias__mutmut_18 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_19'] = x__has_marker_namespace_alias__mutmut_19 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_20'] = x__has_marker_namespace_alias__mutmut_20 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_21'] = x__has_marker_namespace_alias__mutmut_21 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_22'] = x__has_marker_namespace_alias__mutmut_22 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_23'] = x__has_marker_namespace_alias__mutmut_23 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_24'] = x__has_marker_namespace_alias__mutmut_24 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_25'] = x__has_marker_namespace_alias__mutmut_25 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_26'] = x__has_marker_namespace_alias__mutmut_26 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_27'] = x__has_marker_namespace_alias__mutmut_27 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_28'] = x__has_marker_namespace_alias__mutmut_28 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_29'] = x__has_marker_namespace_alias__mutmut_29 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_30'] = x__has_marker_namespace_alias__mutmut_30 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_31'] = x__has_marker_namespace_alias__mutmut_31 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_32'] = x__has_marker_namespace_alias__mutmut_32 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_33'] = x__has_marker_namespace_alias__mutmut_33 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_34'] = x__has_marker_namespace_alias__mutmut_34 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_35'] = x__has_marker_namespace_alias__mutmut_35 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_36'] = x__has_marker_namespace_alias__mutmut_36 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_37'] = x__has_marker_namespace_alias__mutmut_37 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_38'] = x__has_marker_namespace_alias__mutmut_38 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_39'] = x__has_marker_namespace_alias__mutmut_39 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_40'] = x__has_marker_namespace_alias__mutmut_40 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_41'] = x__has_marker_namespace_alias__mutmut_41 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_42'] = x__has_marker_namespace_alias__mutmut_42 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_43'] = x__has_marker_namespace_alias__mutmut_43 # type: ignore # mutmut generated
mutants_x__has_marker_namespace_alias__mutmut['x__has_marker_namespace_alias__mutmut_44'] = x__has_marker_namespace_alias__mutmut_44 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_pytestmark_attribute_or_mutation__mutmut)
def _has_pytestmark_attribute_or_mutation(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "pytestmark" or (isinstance(node.value, ast.Name) and node.value.id == "pytestmark")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_orig(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "pytestmark" or (isinstance(node.value, ast.Name) and node.value.id == "pytestmark")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_1(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        None
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_2(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute) or (
            node.attr == "pytestmark" or (isinstance(node.value, ast.Name) and node.value.id == "pytestmark")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_3(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "pytestmark" and (isinstance(node.value, ast.Name) and node.value.id == "pytestmark")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_4(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr != "pytestmark" or (isinstance(node.value, ast.Name) and node.value.id == "pytestmark")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_5(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "XXpytestmarkXX" or (isinstance(node.value, ast.Name) and node.value.id == "pytestmark")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_6(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "PYTESTMARK" or (isinstance(node.value, ast.Name) and node.value.id == "pytestmark")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_7(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "pytestmark" or (isinstance(node.value, ast.Name) or node.value.id == "pytestmark")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_8(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "pytestmark" or (isinstance(node.value, ast.Name) and node.value.id != "pytestmark")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_9(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "pytestmark" or (isinstance(node.value, ast.Name) and node.value.id == "XXpytestmarkXX")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_10(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "pytestmark" or (isinstance(node.value, ast.Name) and node.value.id == "PYTESTMARK")
        )
        for node in ast.walk(tree)
    )


def x__has_pytestmark_attribute_or_mutation__mutmut_11(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "pytestmark" or (isinstance(node.value, ast.Name) and node.value.id == "pytestmark")
        )
        for node in ast.walk(None)
    )

mutants_x__has_pytestmark_attribute_or_mutation__mutmut['_mutmut_orig'] = x__has_pytestmark_attribute_or_mutation__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_1'] = x__has_pytestmark_attribute_or_mutation__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_2'] = x__has_pytestmark_attribute_or_mutation__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_3'] = x__has_pytestmark_attribute_or_mutation__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_4'] = x__has_pytestmark_attribute_or_mutation__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_5'] = x__has_pytestmark_attribute_or_mutation__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_6'] = x__has_pytestmark_attribute_or_mutation__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_7'] = x__has_pytestmark_attribute_or_mutation__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_8'] = x__has_pytestmark_attribute_or_mutation__mutmut_8 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_9'] = x__has_pytestmark_attribute_or_mutation__mutmut_9 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_10'] = x__has_pytestmark_attribute_or_mutation__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_pytestmark_attribute_or_mutation__mutmut['x__has_pytestmark_attribute_or_mutation__mutmut_11'] = x__has_pytestmark_attribute_or_mutation__mutmut_11 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__has_tier_marker_outside_declaration__mutmut)
def _has_tier_marker_outside_declaration(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(node, tiers) and id(node) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_orig(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(node, tiers) and id(node) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_1(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = None
    return any(
        _is_direct_tier_marker(node, tiers) and id(node) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_2(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(None) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(node, tiers) and id(node) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_3(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(None)}
    return any(
        _is_direct_tier_marker(node, tiers) and id(node) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_4(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        None
    )


def x__has_tier_marker_outside_declaration__mutmut_5(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(node, tiers) or id(node) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_6(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(None, tiers) and id(node) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_7(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(node, None) and id(node) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_8(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(tiers) and id(node) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_9(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(node, ) and id(node) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_10(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(node, tiers) and id(None) not in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_11(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(node, tiers) and id(node) in allowed_value_nodes
        for node in ast.walk(tree)
        if isinstance(node, ast.expr)
    )


def x__has_tier_marker_outside_declaration__mutmut_12(
    tree: ast.Module,
    tiers: frozenset[str],
    declaration: ast.Assign,
) -> bool:
    """Reject every explicit tier marker except the canonical declaration value."""
    allowed_value_nodes = {id(node) for node in ast.walk(declaration.value)}
    return any(
        _is_direct_tier_marker(node, tiers) and id(node) not in allowed_value_nodes
        for node in ast.walk(None)
        if isinstance(node, ast.expr)
    )

mutants_x__has_tier_marker_outside_declaration__mutmut['_mutmut_orig'] = x__has_tier_marker_outside_declaration__mutmut_orig # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_1'] = x__has_tier_marker_outside_declaration__mutmut_1 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_2'] = x__has_tier_marker_outside_declaration__mutmut_2 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_3'] = x__has_tier_marker_outside_declaration__mutmut_3 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_4'] = x__has_tier_marker_outside_declaration__mutmut_4 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_5'] = x__has_tier_marker_outside_declaration__mutmut_5 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_6'] = x__has_tier_marker_outside_declaration__mutmut_6 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_7'] = x__has_tier_marker_outside_declaration__mutmut_7 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_8'] = x__has_tier_marker_outside_declaration__mutmut_8 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_9'] = x__has_tier_marker_outside_declaration__mutmut_9 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_10'] = x__has_tier_marker_outside_declaration__mutmut_10 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_11'] = x__has_tier_marker_outside_declaration__mutmut_11 # type: ignore # mutmut generated
mutants_x__has_tier_marker_outside_declaration__mutmut['x__has_tier_marker_outside_declaration__mutmut_12'] = x__has_tier_marker_outside_declaration__mutmut_12 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__canonical_module_tier_is_valid__mutmut)
def _canonical_module_tier_is_valid(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_orig(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_1(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = None
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_2(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(None, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_3(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, None)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_4(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_5(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, )
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_6(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is not None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_7(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return True
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_8(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_9(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree) and _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_10(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree) and _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_11(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration) and _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_12(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(None, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_13(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, None)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_14(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_15(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, )
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_16(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(None)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_17(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(None)
        or _has_tier_marker_outside_declaration(tree, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_18(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(None, tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_19(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, None, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_20(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, None)
    )


def x__canonical_module_tier_is_valid__mutmut_21(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tiers, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_22(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, declaration)
    )


def x__canonical_module_tier_is_valid__mutmut_23(tree: ast.Module, tiers: frozenset[str]) -> bool:
    """True iff a module has one static, unambiguous primary tier declaration."""
    declaration = _canonical_declaration(tree, tiers)
    if declaration is None:
        return False
    return not (
        _has_unallowed_pytestmark_use(tree, declaration)
        or _has_marker_namespace_alias(tree)
        or _has_pytestmark_attribute_or_mutation(tree)
        or _has_tier_marker_outside_declaration(tree, tiers, )
    )

mutants_x__canonical_module_tier_is_valid__mutmut['_mutmut_orig'] = x__canonical_module_tier_is_valid__mutmut_orig # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_1'] = x__canonical_module_tier_is_valid__mutmut_1 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_2'] = x__canonical_module_tier_is_valid__mutmut_2 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_3'] = x__canonical_module_tier_is_valid__mutmut_3 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_4'] = x__canonical_module_tier_is_valid__mutmut_4 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_5'] = x__canonical_module_tier_is_valid__mutmut_5 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_6'] = x__canonical_module_tier_is_valid__mutmut_6 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_7'] = x__canonical_module_tier_is_valid__mutmut_7 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_8'] = x__canonical_module_tier_is_valid__mutmut_8 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_9'] = x__canonical_module_tier_is_valid__mutmut_9 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_10'] = x__canonical_module_tier_is_valid__mutmut_10 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_11'] = x__canonical_module_tier_is_valid__mutmut_11 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_12'] = x__canonical_module_tier_is_valid__mutmut_12 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_13'] = x__canonical_module_tier_is_valid__mutmut_13 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_14'] = x__canonical_module_tier_is_valid__mutmut_14 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_15'] = x__canonical_module_tier_is_valid__mutmut_15 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_16'] = x__canonical_module_tier_is_valid__mutmut_16 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_17'] = x__canonical_module_tier_is_valid__mutmut_17 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_18'] = x__canonical_module_tier_is_valid__mutmut_18 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_19'] = x__canonical_module_tier_is_valid__mutmut_19 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_20'] = x__canonical_module_tier_is_valid__mutmut_20 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_21'] = x__canonical_module_tier_is_valid__mutmut_21 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_22'] = x__canonical_module_tier_is_valid__mutmut_22 # type: ignore # mutmut generated
mutants_x__canonical_module_tier_is_valid__mutmut['x__canonical_module_tier_is_valid__mutmut_23'] = x__canonical_module_tier_is_valid__mutmut_23 # type: ignore # mutmut generated
mutants_x__function_tier_marker__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__function_tier_marker__mutmut)
def _function_tier_marker(node: ast.FunctionDef | ast.AsyncFunctionDef, tiers: frozenset[str]) -> set[str]:
    out: set[str] = set()
    for dec in node.decorator_list:
        out |= _extract_marker_names(dec)
    return out & tiers


def x__function_tier_marker__mutmut_orig(node: ast.FunctionDef | ast.AsyncFunctionDef, tiers: frozenset[str]) -> set[str]:
    out: set[str] = set()
    for dec in node.decorator_list:
        out |= _extract_marker_names(dec)
    return out & tiers


def x__function_tier_marker__mutmut_1(node: ast.FunctionDef | ast.AsyncFunctionDef, tiers: frozenset[str]) -> set[str]:
    out: set[str] = None
    for dec in node.decorator_list:
        out |= _extract_marker_names(dec)
    return out & tiers


def x__function_tier_marker__mutmut_2(node: ast.FunctionDef | ast.AsyncFunctionDef, tiers: frozenset[str]) -> set[str]:
    out: set[str] = set()
    for dec in node.decorator_list:
        out = _extract_marker_names(dec)
    return out & tiers


def x__function_tier_marker__mutmut_3(node: ast.FunctionDef | ast.AsyncFunctionDef, tiers: frozenset[str]) -> set[str]:
    out: set[str] = set()
    for dec in node.decorator_list:
        out &= _extract_marker_names(dec)
    return out & tiers


def x__function_tier_marker__mutmut_4(node: ast.FunctionDef | ast.AsyncFunctionDef, tiers: frozenset[str]) -> set[str]:
    out: set[str] = set()
    for dec in node.decorator_list:
        out |= _extract_marker_names(None)
    return out & tiers


def x__function_tier_marker__mutmut_5(node: ast.FunctionDef | ast.AsyncFunctionDef, tiers: frozenset[str]) -> set[str]:
    out: set[str] = set()
    for dec in node.decorator_list:
        out |= _extract_marker_names(dec)
    return out | tiers

mutants_x__function_tier_marker__mutmut['_mutmut_orig'] = x__function_tier_marker__mutmut_orig # type: ignore # mutmut generated
mutants_x__function_tier_marker__mutmut['x__function_tier_marker__mutmut_1'] = x__function_tier_marker__mutmut_1 # type: ignore # mutmut generated
mutants_x__function_tier_marker__mutmut['x__function_tier_marker__mutmut_2'] = x__function_tier_marker__mutmut_2 # type: ignore # mutmut generated
mutants_x__function_tier_marker__mutmut['x__function_tier_marker__mutmut_3'] = x__function_tier_marker__mutmut_3 # type: ignore # mutmut generated
mutants_x__function_tier_marker__mutmut['x__function_tier_marker__mutmut_4'] = x__function_tier_marker__mutmut_4 # type: ignore # mutmut generated
mutants_x__function_tier_marker__mutmut['x__function_tier_marker__mutmut_5'] = x__function_tier_marker__mutmut_5 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__untagged_functions__mutmut)
def _untagged_functions(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_orig(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_1(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = None
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_2(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(None):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_3(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_4(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            break
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_5(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if node.name.startswith("test_"):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_6(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith(None):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_7(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("XXtest_XX"):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_8(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("TEST_"):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_9(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            break
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_10(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_11(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(None, tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_12(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(node, None):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_13(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(tiers):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_14(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(node, ):
            out.append(node.name)
    return out


def x__untagged_functions__mutmut_15(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not node.name.startswith("test_"):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(None)
    return out

mutants_x__untagged_functions__mutmut['_mutmut_orig'] = x__untagged_functions__mutmut_orig # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_1'] = x__untagged_functions__mutmut_1 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_2'] = x__untagged_functions__mutmut_2 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_3'] = x__untagged_functions__mutmut_3 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_4'] = x__untagged_functions__mutmut_4 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_5'] = x__untagged_functions__mutmut_5 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_6'] = x__untagged_functions__mutmut_6 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_7'] = x__untagged_functions__mutmut_7 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_8'] = x__untagged_functions__mutmut_8 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_9'] = x__untagged_functions__mutmut_9 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_10'] = x__untagged_functions__mutmut_10 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_11'] = x__untagged_functions__mutmut_11 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_12'] = x__untagged_functions__mutmut_12 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_13'] = x__untagged_functions__mutmut_13 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_14'] = x__untagged_functions__mutmut_14 # type: ignore # mutmut generated
mutants_x__untagged_functions__mutmut['x__untagged_functions__mutmut_15'] = x__untagged_functions__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_file_missing_tier_marker__mutmut)
def file_missing_tier_marker(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_orig(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_1(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = True,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_2(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = None
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_3(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(None, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_4(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=None)
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_5(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_6(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), )
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_7(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding=None), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_8(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="XXutf-8XX"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_9(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="UTF-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_10(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(None))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_11(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return True
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_12(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = None
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_13(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        None
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_14(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) or node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_15(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith(None)
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_16(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("XXtest_XX")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_17(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("TEST_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_18(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(None)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_19(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests or not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_20(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_21(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(None, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_22(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, None)
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_23(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_24(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, )
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_25(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(None))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_26(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(None, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_27(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, None):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_28(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_29(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, ):
        return False
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_30(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return True
    return bool(_untagged_functions(tree, tiers))


def x_file_missing_tier_marker__mutmut_31(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(None)


def x_file_missing_tier_marker__mutmut_32(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(None, tiers))


def x_file_missing_tier_marker__mutmut_33(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, None))


def x_file_missing_tier_marker__mutmut_34(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tiers))


def x_file_missing_tier_marker__mutmut_35(
    path: Path,
    *,
    tiers: frozenset[str],
    require_module_marker: bool = False,
) -> bool:
    """True iff ``path`` holds a ``test_*`` function with no tier marker.

    Pure helper (the detection core): a module-level ``pytestmark`` tier
    covers the whole file; otherwise every ``test_*`` function must carry one.
    When ``require_module_marker`` is true, a test module instead needs exactly
    one static module-level tier from the fixed canonical vocabulary; ``tiers``
    is a generic-mode option only. A file with no test functions (a fixtures
    module) is not a violation. A syntax / decode error is treated as "no
    violation".
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return False
    has_tests = any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_")
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, ))

mutants_x_file_missing_tier_marker__mutmut['_mutmut_orig'] = x_file_missing_tier_marker__mutmut_orig # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_1'] = x_file_missing_tier_marker__mutmut_1 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_2'] = x_file_missing_tier_marker__mutmut_2 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_3'] = x_file_missing_tier_marker__mutmut_3 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_4'] = x_file_missing_tier_marker__mutmut_4 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_5'] = x_file_missing_tier_marker__mutmut_5 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_6'] = x_file_missing_tier_marker__mutmut_6 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_7'] = x_file_missing_tier_marker__mutmut_7 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_8'] = x_file_missing_tier_marker__mutmut_8 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_9'] = x_file_missing_tier_marker__mutmut_9 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_10'] = x_file_missing_tier_marker__mutmut_10 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_11'] = x_file_missing_tier_marker__mutmut_11 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_12'] = x_file_missing_tier_marker__mutmut_12 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_13'] = x_file_missing_tier_marker__mutmut_13 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_14'] = x_file_missing_tier_marker__mutmut_14 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_15'] = x_file_missing_tier_marker__mutmut_15 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_16'] = x_file_missing_tier_marker__mutmut_16 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_17'] = x_file_missing_tier_marker__mutmut_17 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_18'] = x_file_missing_tier_marker__mutmut_18 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_19'] = x_file_missing_tier_marker__mutmut_19 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_20'] = x_file_missing_tier_marker__mutmut_20 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_21'] = x_file_missing_tier_marker__mutmut_21 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_22'] = x_file_missing_tier_marker__mutmut_22 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_23'] = x_file_missing_tier_marker__mutmut_23 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_24'] = x_file_missing_tier_marker__mutmut_24 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_25'] = x_file_missing_tier_marker__mutmut_25 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_26'] = x_file_missing_tier_marker__mutmut_26 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_27'] = x_file_missing_tier_marker__mutmut_27 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_28'] = x_file_missing_tier_marker__mutmut_28 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_29'] = x_file_missing_tier_marker__mutmut_29 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_30'] = x_file_missing_tier_marker__mutmut_30 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_31'] = x_file_missing_tier_marker__mutmut_31 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_32'] = x_file_missing_tier_marker__mutmut_32 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_33'] = x_file_missing_tier_marker__mutmut_33 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_34'] = x_file_missing_tier_marker__mutmut_34 # type: ignore # mutmut generated
mutants_x_file_missing_tier_marker__mutmut['x_file_missing_tier_marker__mutmut_35'] = x_file_missing_tier_marker__mutmut_35 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut: MutantDict = {}  # type: ignore
mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut: MutantDict = {}  # type: ignore
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut: MutantDict = {}  # type: ignore


class EveryTestHasTierMarker(FitnessRule):
    """Flags test files whose tests lack a tier marker."""

    name = "every-test-has-tier-marker"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knobs.
    tier_markers: tuple[str, ...] = DEFAULT_TIER_MARKERS
    require_module_marker: bool = False

    @classmethod
    @_mutmut_mutated(mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut, is_classmethod = True)
    def from_config(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_orig(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_1(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = None
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_2(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(None, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_3(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=None)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_4(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_5(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, )
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_6(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = None
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_7(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get(None)
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_8(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("XXtier_markersXX")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_9(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("TIER_MARKERS")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_10(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = None
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_11(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(None) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_12(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_13(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = None
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_14(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(None)
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_15(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get(None, False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_16(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", None))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_17(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get(False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_18(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", ))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_19(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("XXrequire_module_markerXX", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_20(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("REQUIRE_MODULE_MARKER", False))
        return rule

    @classmethod
    def xǁEveryTestHasTierMarkerǁfrom_config__mutmut_21(
        cls,
        config: Mapping[str, Any],
        *,
        repo_root: Path | None = None,
    ) -> EveryTestHasTierMarker:
        rule = super().from_config(config, repo_root=repo_root)
        assert isinstance(rule, EveryTestHasTierMarker)  # noqa: S101  # narrowing for mypy
        markers = config.get("tier_markers")
        rule.tier_markers = tuple(markers) if markers is not None else DEFAULT_TIER_MARKERS
        rule.require_module_marker = bool(config.get("require_module_marker", True))
        return rule

    @_mutmut_mutated(mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut)
    def is_in_scope(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_orig(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_1(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_2(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(None):
            return False
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_3(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return True
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_4(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = None
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_5(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(None).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_6(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(None):
            return False
        return Path(rel).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_7(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(part not in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_8(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return True
        return Path(rel).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_9(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith(None)

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_10(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(None).name.startswith("test_")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_11(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("XXtest_XX")

    def xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_12(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("TEST_")

    @_mutmut_mutated(mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut)
    def file_has_violation(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return False
        return file_missing_tier_marker(
            path,
            tiers=frozenset(self.tier_markers),
            require_module_marker=self.require_module_marker,
        )

    def xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_orig(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return False
        return file_missing_tier_marker(
            path,
            tiers=frozenset(self.tier_markers),
            require_module_marker=self.require_module_marker,
        )

    def xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_1(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(None):
            return False
        return file_missing_tier_marker(
            path,
            tiers=frozenset(self.tier_markers),
            require_module_marker=self.require_module_marker,
        )

    def xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_2(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return True
        return file_missing_tier_marker(
            path,
            tiers=frozenset(self.tier_markers),
            require_module_marker=self.require_module_marker,
        )

    def xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_3(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return False
        return file_missing_tier_marker(
            None,
            tiers=frozenset(self.tier_markers),
            require_module_marker=self.require_module_marker,
        )

    def xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_4(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return False
        return file_missing_tier_marker(
            path,
            tiers=None,
            require_module_marker=self.require_module_marker,
        )

    def xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_5(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return False
        return file_missing_tier_marker(
            path,
            tiers=frozenset(self.tier_markers),
            require_module_marker=None,
        )

    def xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_6(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return False
        return file_missing_tier_marker(
            tiers=frozenset(self.tier_markers),
            require_module_marker=self.require_module_marker,
        )

    def xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_7(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return False
        return file_missing_tier_marker(
            path,
            require_module_marker=self.require_module_marker,
        )

    def xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_8(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return False
        return file_missing_tier_marker(
            path,
            tiers=frozenset(self.tier_markers),
            )

    def xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_9(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return False
        return file_missing_tier_marker(
            path,
            tiers=frozenset(None),
            require_module_marker=self.require_module_marker,
        )

    @_mutmut_mutated(mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut)
    def _is_registered_contract_fixture(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_orig(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_1(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = None
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_2(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent != self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_3(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                return
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_4(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = None
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_5(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(None, CORE_CHECKS)
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_6(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, None)
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_7(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(CORE_CHECKS)
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_8(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, )
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_9(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is not None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_10(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is None:
                break
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_11(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is None:
                continue
            return any(None)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_12(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is None:
                continue
            return any(resolved.is_relative_to(None) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_13(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent * case.fixture).resolve()) for case in contract.cases)
        return False

    def xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_14(self, path: Path) -> bool:
        """Treat a manifest-bound case tree as test data, never test code.

        A directory name alone cannot hide a test. The nearest contract must
        parse under the public schema, bind its directory/check identity, and
        explicitly name the case fixture containing ``path``.
        """
        resolved = path.resolve()
        for parent in resolved.parents:
            if parent == self._repo_root.parent:
                break
            contract = registered_contract_directory(parent, CORE_CHECKS)
            if contract is None:
                continue
            return any(resolved.is_relative_to((parent / case.fixture).resolve()) for case in contract.cases)
        return True

mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['_mutmut_orig'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_1'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_2'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_3'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_4'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_5'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_6'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_7'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_8'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_9'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_10'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_11'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_12'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_13'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_14'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_15'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_16'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_17'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_18'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_19'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_20'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfrom_config__mutmut['xǁEveryTestHasTierMarkerǁfrom_config__mutmut_21'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfrom_config__mutmut_21 # type: ignore # mutmut generated

mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['_mutmut_orig'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_1'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_2'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_3'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_4'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_4 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_5'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_5 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_6'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_6 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_7'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_7 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_8'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_8 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_9'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_9 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_10'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_10 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_11'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_11 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁis_in_scope__mutmut['xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_12'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁis_in_scope__mutmut_12 # type: ignore # mutmut generated

mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut['_mutmut_orig'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut['xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_1'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut['xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_2'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut['xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_3'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut['xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_4'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_4 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut['xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_5'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_5 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut['xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_6'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_6 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut['xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_7'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_7 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut['xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_8'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_8 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut['xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_9'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁfile_has_violation__mutmut_9 # type: ignore # mutmut generated

mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['_mutmut_orig'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_1'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_2'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_3'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_4'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_4 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_5'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_5 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_6'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_6 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_7'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_7 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_8'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_8 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_9'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_9 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_10'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_10 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_11'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_11 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_12'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_12 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_13'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_13 # type: ignore # mutmut generated
mutants_xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut['xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_14'] = EveryTestHasTierMarker.xǁEveryTestHasTierMarkerǁ_is_registered_contract_fixture__mutmut_14 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EveryTestHasTierMarker:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EveryTestHasTierMarker.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EveryTestHasTierMarker:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EveryTestHasTierMarker.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EveryTestHasTierMarker:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EveryTestHasTierMarker.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EveryTestHasTierMarker:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EveryTestHasTierMarker.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EveryTestHasTierMarker:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EveryTestHasTierMarker.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EveryTestHasTierMarker:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EveryTestHasTierMarker.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EveryTestHasTierMarker, argv)


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EveryTestHasTierMarker, argv)


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(None, argv)


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EveryTestHasTierMarker, None)


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(argv)


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EveryTestHasTierMarker, )

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
