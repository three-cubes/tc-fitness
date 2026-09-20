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


def _module_tier_marker(tree: ast.Module, tiers: frozenset[str]) -> set[str]:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "pytestmark":
                return _extract_marker_names(node.value) & tiers
    return set()


def _is_pytestmark_target(target: ast.expr) -> bool:
    return isinstance(target, ast.Name) and target.id == "pytestmark"


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


def _has_unallowed_pytestmark_use(tree: ast.Module, declaration: ast.Assign) -> bool:
    return any(_uses_pytestmark(node, declaration.targets[0]) for node in ast.walk(tree))


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


def _has_pytestmark_attribute_or_mutation(tree: ast.Module) -> bool:
    """Reject ``x.pytestmark`` and uses that mutate/read pytestmark itself."""
    return any(
        isinstance(node, ast.Attribute)
        and (
            node.attr == "pytestmark" or (isinstance(node.value, ast.Name) and node.value.id == "pytestmark")
        )
        for node in ast.walk(tree)
    )


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


def _function_tier_marker(node: ast.FunctionDef | ast.AsyncFunctionDef, tiers: frozenset[str]) -> set[str]:
    out: set[str] = set()
    for dec in node.decorator_list:
        out |= _extract_marker_names(dec)
    return out & tiers


def _is_collected_test_function(name: str) -> bool:
    """Match pytest's own default for collecting a test function.

    ``python_functions`` defaults to ``test``, not ``test_``. Requiring the
    underscore leaves ``def testThing()`` collected by pytest but invisible
    here, so a module holding only such tests reads as having none and escapes
    the tier requirement entirely. File names are a separate default —
    ``python_files`` is ``test_*.py`` — and keep their underscore.
    """
    return name.startswith("test")


def _untagged_functions(tree: ast.Module, tiers: frozenset[str]) -> list[str]:
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        if not _is_collected_test_function(node.name):
            continue
        if not _function_tier_marker(node, tiers):
            out.append(node.name)
    return out


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
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and _is_collected_test_function(node.name)
        for node in ast.walk(tree)
    )
    if require_module_marker:
        return has_tests and not _canonical_module_tier_is_valid(tree, frozenset(DEFAULT_TIER_MARKERS))
    if _module_tier_marker(tree, tiers):
        return False
    return bool(_untagged_functions(tree, tiers))


class EveryTestHasTierMarker(FitnessRule):
    """Flags test files whose tests lack a tier marker."""

    name = "every-test-has-tier-marker"
    remediation = REMEDIATION
    extensions = (".py",)

    #: Rule-specific knobs.
    tier_markers: tuple[str, ...] = DEFAULT_TIER_MARKERS
    require_module_marker: bool = False

    @classmethod
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

    def is_in_scope(self, rel: str) -> bool:
        """Tier markers only apply to ``test_*`` modules; skip support trees."""
        if not super().is_in_scope(rel):
            return False
        parts = Path(rel).parts
        if any(part in DEFAULT_EXCLUDED_PARTS for part in parts):
            return False
        return Path(rel).name.startswith("test_")

    def file_has_violation(self, path: Path) -> bool:
        if self._is_registered_contract_fixture(path):
            return False
        return file_missing_tier_marker(
            path,
            tiers=frozenset(self.tier_markers),
            require_module_marker=self.require_module_marker,
        )

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


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> EveryTestHasTierMarker:
    """Factory the engine calls to bind this CORE check to a consumer's config."""
    return EveryTestHasTierMarker.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry supporting ``--repo-root``."""
    return run_core_check(EveryTestHasTierMarker, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
