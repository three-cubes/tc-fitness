"""CORE check: declared runtime tests execute without test doubles.

Unit and contract tests may use explicit fakes to isolate a boundary. A test
declared as an end-to-end, journey, PVT, or other runtime tier instead proves
the deployed composition. Test doubles in that tier replace the system being
claimed as evidence and make a passing result non-probative.

The consumer supplies its runtime marker vocabulary. This check rejects the
common Python double forms only inside a test carrying one of those markers:
``monkeypatch`` mutation, ``unittest.mock`` construction or patching, and
classes or constructors named ``Fake*``, ``Stub*``, or ``Mock*``.
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

_DOUBLE_CONSTRUCTORS = frozenset({"Mock", "MagicMock", "AsyncMock", "patch"})
_MONKEYPATCH_MUTATORS = frozenset({"setattr", "setenv", "delenv"})
_DOUBLE_CLASS_PREFIXES = ("Fake", "Stub", "Mock")


def _marker_names(value: ast.expr) -> set[str]:
    """Return ``pytest.mark.<name>`` references held by an expression."""
    if isinstance(value, ast.List | ast.Tuple):
        return set().union(*(_marker_names(element) for element in value.elts))
    if isinstance(value, ast.Call):
        return _marker_names(value.func)
    if (
        isinstance(value, ast.Attribute)
        and isinstance(value.value, ast.Attribute)
        and value.value.attr == "mark"
        and isinstance(value.value.value, ast.Name)
        and value.value.value.id == "pytest"
    ):
        return {value.attr}
    return set()


def _module_markers(tree: ast.Module) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets):
            return _marker_names(node.value)
    return set()


def _function_markers(node: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    """Return direct pytest marker names on one test function."""
    return set().union(*(_marker_names(decorator) for decorator in node.decorator_list))


def _call_is_test_double(node: ast.Call, *, forbidden_keyword_arguments: frozenset[str]) -> bool:
    """Recognise common test-double construction and monkeypatch mutation."""
    if any(
        keyword.arg in forbidden_keyword_arguments for keyword in node.keywords if keyword.arg is not None
    ):
        return True
    if isinstance(node.func, ast.Name):
        return node.func.id in _DOUBLE_CONSTRUCTORS or node.func.id.startswith(_DOUBLE_CLASS_PREFIXES)
    if not isinstance(node.func, ast.Attribute):
        return False
    if isinstance(node.func.value, ast.Name) and node.func.value.id == "monkeypatch":
        return node.func.attr in _MONKEYPATCH_MUTATORS
    return node.func.attr in _DOUBLE_CONSTRUCTORS or (
        node.func.attr == "object"
        and isinstance(node.func.value, ast.Attribute)
        and node.func.value.attr == "patch"
    )


def _nodes_contain_test_double(
    nodes: Iterable[ast.AST], *, forbidden_keyword_arguments: frozenset[str]
) -> bool:
    """True when any supplied syntax subtree declares or invokes a test double."""
    for root in nodes:
        for node in ast.walk(root):
            if isinstance(node, ast.ClassDef) and node.name.startswith(_DOUBLE_CLASS_PREFIXES):
                return True
            if isinstance(node, ast.Call) and _call_is_test_double(
                node,
                forbidden_keyword_arguments=forbidden_keyword_arguments,
            ):
                return True
    return False


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
    if _module_markers(tree) & runtime:
        return _nodes_contain_test_double(tree.body, forbidden_keyword_arguments=forbidden_keywords)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
            and node.name.startswith("test_")
            and _function_markers(node) & runtime
            and _nodes_contain_test_double((node,), forbidden_keyword_arguments=forbidden_keywords)
        ):
            return True
    return False


class NoTestDoublesInRuntimeTiers(FitnessRule):
    """Rejects test doubles in tests that declare live runtime coverage."""

    name = "no-test-doubles-in-runtime-tiers"
    remediation = REMEDIATION
    extensions = (".py",)
    runtime_markers: tuple[str, ...] = ()
    forbidden_keyword_arguments: tuple[str, ...] = ()

    @classmethod
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

    def file_has_violation(self, path: Path) -> bool:
        return file_has_runtime_tier_test_double(
            path,
            runtime_markers=self.runtime_markers,
            forbidden_keyword_arguments=self.forbidden_keyword_arguments,
        )


def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> NoTestDoublesInRuntimeTiers:
    """Build this consumer-configured CORE check."""
    return NoTestDoublesInRuntimeTiers.from_config(config, repo_root=repo_root)


def main(argv: list[str] | None = None) -> int:
    """CLI entry — supports the standard CORE check arguments."""
    return run_core_check(NoTestDoublesInRuntimeTiers, argv)


if __name__ == "__main__":
    import sys

    sys.exit(main())
