"""Tests for the CORE check actionable_feedback (v0.6.0)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tc_fitness.core_checks.actionable_feedback import (
    ActionableFeedback,
    build,
    module_has_unactionable_error,
)

pytestmark = pytest.mark.integration

_BAD = """
def check(errors):
    errors.append("validation failed")
"""

_OK = """
def check(errors):
    errors.append("bad name; fix: rename it; next: rerun the gate")
"""

_OK_FSTRING = """
def check(errors, rel):
    errors.append(f"{rel}: bad; fix: rename; next: rerun")
"""

_NON_ERROR_VAR = """
def check(results):
    results.append("validation failed")
"""


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_flags_unactionable(tmp_path: Path) -> None:
    p = _seed(tmp_path, "bad.py", _BAD)
    assert module_has_unactionable_error(p, markers=("fix:", "next:", "run:")) is True


def test_detection_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "ok.py", _OK)
    assert module_has_unactionable_error(p, markers=("fix:", "next:", "run:")) is False


def test_detection_clean_fstring(tmp_path: Path) -> None:
    p = _seed(tmp_path, "okf.py", _OK_FSTRING)
    assert module_has_unactionable_error(p, markers=("fix:", "next:", "run:")) is False


def test_non_error_variable_ignored(tmp_path: Path) -> None:
    p = _seed(tmp_path, "ne.py", _NON_ERROR_VAR)
    assert module_has_unactionable_error(p, markers=("fix:", "next:", "run:")) is False


def test_syntax_error_is_not_a_violation(tmp_path: Path) -> None:
    p = _seed(tmp_path, "broken.py", "def (:\n")
    assert module_has_unactionable_error(p, markers=("fix:",)) is False


def test_broken_utf8_source_is_not_a_violation(tmp_path: Path) -> None:
    path = tmp_path / "broken-encoding.py"
    path.write_bytes(b"errors.append('bad')\n\xff")

    assert module_has_unactionable_error(path, markers=("fix:",)) is False


def test_extend_checks_each_literal_in_a_container(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "extended.py",
        'def check(errors, detail):\n    errors.extend(["fix: repaired", f"still broken: {detail}"])\n',
    )

    assert module_has_unactionable_error(path, markers=("fix:", "next:", "run:")) is True


def test_non_literal_arguments_and_other_receivers_are_ignored(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "dynamic.py",
        "def check(errors, error_results, render):\n"
        "    errors.append(42)\n"
        "    errors.append(render())\n"
        "    errors.extend([])\n"
        "    error_results.messages.append('validation failed')\n",
    )

    assert module_has_unactionable_error(path, markers=("fix:",)) is False


def test_markers_are_config_driven(tmp_path: Path) -> None:
    body = 'def c(errors):\n    errors.append("do: thing")\n'
    p = _seed(tmp_path, "m.py", body)
    # Default markers absent → violation; configure "do:" → clean.
    assert module_has_unactionable_error(p, markers=("fix:", "next:", "run:")) is True
    rule = build({"roots": ["."], "markers": ["do:"]}, repo_root=tmp_path)
    assert rule.file_has_violation(p) is False


def test_rule_from_config_scopes_roots(tmp_path: Path) -> None:
    _seed(tmp_path, "src/bad.py", _BAD)
    _seed(tmp_path, "vendor/bad.py", _BAD)
    rule = ActionableFeedback.from_config({"roots": ["src"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"src/bad.py"}


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.actionable_feedback as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(text)
    docstring_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None and node.body:
                first = node.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                    docstring_ids.add(id(first.value))
    repo_tokens = ("kairix", "tc-agent-zone", "agent-zone", "kata")
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if id(node) in docstring_ids:
                continue
            lowered = node.value.lower()
            for tok in repo_tokens:
                assert tok not in lowered, f"repo identity leaked in a code literal: {tok}"
