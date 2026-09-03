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


def _is_double_name(name: str) -> bool:
    """Return true when a private or public name identifies a test double."""
    return name.lstrip("_").startswith(_DOUBLE_CLASS_PREFIXES)


def _dotted_name(value: ast.expr) -> str | None:
    """Return a dotted syntax name without resolving import aliases."""
    if isinstance(value, ast.Name):
        return value.id
    if isinstance(value, ast.Attribute):
        parent = _dotted_name(value.value)
        return f"{parent}.{value.attr}" if parent else None
    return None


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


def _resolved_name(value: ast.expr, aliases: Mapping[str, str]) -> str | None:
    """Return a dotted name with an imported root binding resolved."""
    dotted = _dotted_name(value)
    if dotted is None:
        return None
    root, *suffix = dotted.split(".")
    resolved_root = aliases.get(root, root)
    return ".".join((resolved_root, *suffix))


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


def _module_markers(tree: ast.Module, aliases: Mapping[str, str]) -> set[str]:
    """Return module-level pytest marker names."""
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets):
            return _marker_names(node.value, aliases)
    return set()


def _function_markers(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    aliases: Mapping[str, str],
) -> set[str]:
    """Return direct pytest marker names on one test function."""
    return set().union(*(_marker_names(decorator, aliases) for decorator in node.decorator_list))


def _is_fixture(node: ast.FunctionDef | ast.AsyncFunctionDef, aliases: Mapping[str, str]) -> bool:
    """Return true when a function is registered as a pytest fixture."""
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if _resolved_name(target, aliases) == "pytest.fixture":
            return True
    return False


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


def _function_argument_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    """Return positional and keyword-only argument names in declaration order."""
    return tuple(
        argument.arg for argument in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)
    )


def _initial_monkeypatch_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> frozenset[str]:
    """Return fixture parameters that hold pytest's monkeypatch object directly."""
    return frozenset(name for name in _function_argument_names(node) if name == "monkeypatch")


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


def _is_synthetic_module_injection(node: ast.Assign | ast.AnnAssign, aliases: Mapping[str, str]) -> bool:
    """Return true when a test assigns a synthetic module into ``sys.modules``."""
    targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
    return _is_synthetic_module_value(node.value, aliases) and any(
        isinstance(target, ast.Subscript) and _resolved_name(target.value, aliases) == "sys.modules"
        for target in targets
    )


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
