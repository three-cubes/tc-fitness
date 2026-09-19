"""Tests for the CORE check cognitive_complexity (v0.6.0)."""

from __future__ import annotations

import ast
import runpy
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks.cognitive_complexity import (
    CognitiveComplexity,
    build,
    main,
    module_over_threshold,
)

pytestmark = pytest.mark.integration

# A deeply nested function: nested ifs inside a loop push the score well past 15.
_COMPLEX = """
def f(items):
    total = 0
    for a in items:
        if a > 0:
            if a > 1:
                if a > 2:
                    if a > 3:
                        if a > 4:
                            if a > 5:
                                if a > 6:
                                    total += a
    return total
"""

_SIMPLE = """
def f(items):
    return sum(a for a in items if a > 0)
"""


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_core_flags_complex(tmp_path: Path) -> None:
    p = _seed(tmp_path, "c.py", _COMPLEX)
    assert module_over_threshold(p, threshold=15) is True


def test_detection_core_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "s.py", _SIMPLE)
    assert module_over_threshold(p, threshold=15) is False


def test_threshold_is_config_driven(tmp_path: Path) -> None:
    # A moderately-branchy function: clean at 15, flagged when the ceiling is 1.
    body = "def f(x):\n    if x:\n        return 1\n    return 0\n"
    p = _seed(tmp_path, "m.py", body)
    assert module_over_threshold(p, threshold=15) is False
    rule = build({"roots": ["."], "threshold": 0}, repo_root=tmp_path)
    assert rule.file_has_violation(p) is True


def test_syntax_error_is_not_a_violation(tmp_path: Path) -> None:
    p = _seed(tmp_path, "bad.py", "def f(:\n")
    assert module_over_threshold(p, threshold=15) is False


def test_scorer_counts_each_python_branch_form_in_a_real_module(tmp_path: Path) -> None:
    p = _seed(
        tmp_path,
        "branches.py",
        """
async def f(items, manager):
    if items and manager and True:
        pass
    else:
        pass
    for item in items:
        pass
    else:
        pass
    async for item in items:
        pass
    else:
        pass
    while False:
        pass
    else:
        pass
    try:
        with manager:
            value = 1 if items else 0
        async with manager:
            pass
    except ValueError:
        pass
    else:
        pass
    finally:
        pass
    return value
""",
    )
    assert module_over_threshold(p, threshold=0) is True
    assert module_over_threshold(p, threshold=100) is False


def test_decode_error_is_not_a_violation(tmp_path: Path) -> None:
    p = tmp_path / "invalid.py"
    p.write_bytes(b"\xff")
    assert module_over_threshold(p, threshold=0) is False


def test_boolean_operators_in_conditions_contribute_to_complexity(tmp_path: Path) -> None:
    path = _seed(
        tmp_path, "conditions.py", "def f(a, b, c):\n    if a and b and c:\n        return 1\n    return 0\n"
    )
    assert module_over_threshold(path, threshold=2) is True
    assert module_over_threshold(path, threshold=3) is False


def test_elif_chain_counts_each_decision_once(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "elif.py",
        "def f(a, b, c):\n    if a:\n        return 1\n    elif b:\n        return 2\n    elif c:\n        return 3\n    return 0\n",
    )
    assert module_over_threshold(path, threshold=3) is False
    assert module_over_threshold(path, threshold=2) is True


def test_empty_else_paths_and_nested_function_definitions_are_scored(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "all_paths.py",
        "def f(items):\n"
        "    for item in items:\n        pass\n"
        "    async def nested():\n        if items:\n            return 1\n"
        "    def sync_nested():\n        while items:\n            break\n"
        "    async def iterate(values):\n        async for value in values:\n            pass\n        else:\n            pass\n"
        "    async def iterate_without_else(values):\n        async for value in values:\n            pass\n"
        "    try:\n        pass\n    except ValueError:\n        pass\n",
    )
    assert module_over_threshold(path, threshold=0) is True
    assert module_over_threshold(path, threshold=100) is False


def test_rule_from_config_scopes_roots(tmp_path: Path) -> None:
    _seed(tmp_path, "src/c.py", _COMPLEX)
    _seed(tmp_path, "vendor/c.py", _COMPLEX)
    rule = CognitiveComplexity.from_config({"roots": ["src"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"src/c.py"}


def test_run_then_establish_grandfathers(tmp_path: Path) -> None:
    _seed(tmp_path, "src/c.py", _COMPLEX)
    rule = CognitiveComplexity.from_config({"roots": ["src"]}, repo_root=tmp_path)
    assert rule.run() == 1
    rule.establish_baseline()
    assert rule.run() == 0


def test_main_establish_baseline_mode(tmp_path: Path) -> None:
    _seed(tmp_path, "c.py", _COMPLEX)
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / ".architecture" / "baseline" / "cognitive-complexity-files.txt").exists()


def test_main_accepts_repo_root_and_scans_it(tmp_path: Path) -> None:
    _seed(tmp_path, "src/complex.py", _COMPLEX)
    assert main(["--repo-root", str(tmp_path)]) == 0


def test_module_entrypoint_uses_repo_root_argument(tmp_path: Path) -> None:
    import tc_fitness.core_checks.cognitive_complexity as module

    original_argv = sys.argv
    sys.argv = ["cognitive_complexity", "--repo-root", str(tmp_path)]
    try:
        with pytest.raises(SystemExit) as result:
            runpy.run_path(str(Path(module.__file__)), run_name="__main__")
    finally:
        sys.argv = original_argv
    assert result.value.code == 0


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.cognitive_complexity as mod

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
