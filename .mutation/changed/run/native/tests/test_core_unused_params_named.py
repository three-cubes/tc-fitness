"""Tests for the CORE check unused_params_named (v0.6.0)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tc_fitness.core_checks.unused_params_named import (
    UnusedParamsNamed,
    build,
    module_has_unused_param,
)

pytestmark = pytest.mark.integration

_UNUSED = """
def handle(event, context):
    return event.id
"""

_NAMED = """
def handle(event, _context):
    return event.id
"""

_ABSTRACT = """
from abc import abstractmethod

class Base:
    @abstractmethod
    def fetch(self, query):
        ...
"""


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_core_flags_unused(tmp_path: Path) -> None:
    p = _seed(tmp_path, "u.py", _UNUSED)
    assert module_has_unused_param(p) is True


def test_underscore_named_is_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "n.py", _NAMED)
    assert module_has_unused_param(p) is False


def test_abstractmethod_is_exempt(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.py", _ABSTRACT)
    assert module_has_unused_param(p) is False


def test_self_and_args_kwargs_exempt(tmp_path: Path) -> None:
    body = "def f(self, *args, **kwargs):\n    return 1\n"
    p = _seed(tmp_path, "x.py", body)
    assert module_has_unused_param(p) is False


def test_property_setter_value_exempt(tmp_path: Path) -> None:
    body = "class C:\n    @x.setter\n    def x(self, value):\n        pass\n"
    p = _seed(tmp_path, "s.py", body)
    assert module_has_unused_param(p) is False


@pytest.mark.parametrize(
    "body",
    [
        "def f(query):\n    pass\n",
        "def f(query):\n    ...\n",
        "def f(query):\n    raise NotImplementedError\n",
        "def f(query):\n    raise NotImplementedError()\n",
        'def f(query):\n    "protocol contract"\n',
        'def f(query):\n    "protocol contract"\n    pass\n',
        'def f(query):\n    "protocol contract"\n    ...\n',
        'def f(query):\n    "protocol contract"\n    raise NotImplementedError\n',
        "from typing import overload\n@overload\ndef f(query):\n    ...\n",
        "from typing import overload\n@overload()\ndef f(query):\n    ...\n",
    ],
)
def test_contract_stub_forms_do_not_report_unused_parameters(tmp_path: Path, body: str) -> None:
    _seed(tmp_path, "src/stubs.py", body)
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_positional_only_and_keyword_only_unused_parameters_are_reported(tmp_path: Path) -> None:
    body = "def positional(event, /):\n    return 1\n"
    body += "def keyword(*, context):\n    return 1\n"
    _seed(tmp_path, "src/handlers.py", body)
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_non_name_decorator_does_not_hide_a_real_unused_parameter(tmp_path: Path) -> None:
    body = "@decorators['contract']\ndef handle(event):\n    return 1\n"
    _seed(tmp_path, "src/decorated.py", body)
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_two_statement_implementation_bodies_are_not_treated_as_stubs(tmp_path: Path) -> None:
    body = 'def uses_event(event):\n    "description"\n    return event.id\n'
    body += "def ignores_event(event):\n    pass\n    return 1\n"
    _seed(tmp_path, "src/handlers.py", body)
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_no_args_and_underscore_parameters_are_clean(tmp_path: Path) -> None:
    body = "def empty():\n    return 1\n"
    body += "def ignored(_context):\n    return 1\n"
    _seed(tmp_path, "src/handlers.py", body)
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 0


def test_rule_from_config_scopes_roots(tmp_path: Path) -> None:
    _seed(tmp_path, "src/u.py", _UNUSED)
    _seed(tmp_path, "vendor/u.py", _UNUSED)
    rule = UnusedParamsNamed.from_config({"roots": ["src"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"src/u.py"}


def test_executable_numeric_expression_is_not_mistaken_for_stub(tmp_path: Path) -> None:
    _seed(tmp_path, "src/worker.py", "def handle(event):\n    42\n")
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_unparseable_configured_source_is_reported(tmp_path: Path) -> None:
    _seed(tmp_path, "src/broken.py", "def handler(:\n")
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.unused_params_named as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(text)
    docstring_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None and node.body:
                first = node.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                    docstring_ids.add(id(first.value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstring_ids:
            lowered = node.value.lower()
            for tok in ("kairix", "tc-agent-zone", "agent-zone", "kata"):
                assert tok not in lowered, f"repo identity leaked: {tok}"
