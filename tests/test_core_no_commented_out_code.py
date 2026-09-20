"""Tests for the CORE check no_commented_out_code (v0.6.0)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tc_fitness.core_checks.no_commented_out_code import (
    NoCommentedOutCode,
    build,
    main,
    module_has_commented_code,
)

pytestmark = pytest.mark.integration

_DEAD = """
x = 1
# old_value = compute(x)
# if old_value > 0:
#     old_value = old_value - 1
# result = store(old_value)
y = 2
"""

_PROSE = """
x = 1
# This function strips the leading slash so paths join cleanly.
# It is a documentation comment, not disabled code.
# Three lines of plain English prose, no statements.
y = 2
"""

_SHORT = """
x = 1
# result = store(x)
y = 2
"""


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_core_flags_dead_code(tmp_path: Path) -> None:
    p = _seed(tmp_path, "d.py", _DEAD)
    assert module_has_commented_code(p, min_run=3) is True


def test_prose_is_not_flagged(tmp_path: Path) -> None:
    p = _seed(tmp_path, "p.py", _PROSE)
    assert module_has_commented_code(p, min_run=3) is False


def test_short_run_below_min_is_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "s.py", _SHORT)
    assert module_has_commented_code(p, min_run=3) is False


def test_unreadable_or_unparseable_python_is_ignored(tmp_path: Path) -> None:
    syntax = _seed(tmp_path, "syntax.py", "value = (\n")
    binary = tmp_path / "binary.py"
    binary.write_bytes(b"# result = 1\n\xff")

    assert module_has_commented_code(tmp_path / "missing.py", min_run=3) is False
    assert module_has_commented_code(syntax, min_run=3) is False
    assert module_has_commented_code(binary, min_run=3) is False


def test_directives_dividers_and_docstrings_are_not_dead_code(tmp_path: Path) -> None:
    body = '''#!/usr/bin/env python3
# coding: utf-8
# noqa: E501
# --------------------------
"""These are documented examples:
# old_value = compute(x)
# if old_value:
#     store(old_value)
"""
# This paragraph explains a path.
# Its meaning is prose for maintainers.
# It remains in the source as documentation.
value = 1
'''
    path = _seed(tmp_path, "documented.py", body)

    assert module_has_commented_code(path, min_run=3) is False


def test_code_comments_without_a_space_after_hash_are_detected(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "no_space.py",
        "#value = 1\n#if value:\n#    value = 2\n",
    )

    assert module_has_commented_code(path, min_run=3) is True


def test_blank_comment_runs_and_comments_before_docstrings_are_ignored(tmp_path: Path) -> None:
    blank = _seed(tmp_path, "blank.py", "# \n# \n# \nvalue = 1\n")
    before_docstring = _seed(
        tmp_path,
        "before_docstring.py",
        "def documented():\n"
        "    # value = 1\n"
        "    # if value:\n"
        "    #     return value\n"
        '    """Describe the function, not disabled code."""\n',
    )

    assert module_has_commented_code(blank, min_run=3) is False
    assert module_has_commented_code(before_docstring, min_run=3) is False


def test_min_run_is_config_driven(tmp_path: Path) -> None:
    p = _seed(tmp_path, "s.py", _SHORT)
    # default 3 → clean; lower min_run to 1 → the single dead line is flagged.
    rule = build({"roots": ["."], "min_run": 1}, repo_root=tmp_path)
    assert rule.file_has_violation(p) is True


def test_rule_from_config_scopes_roots(tmp_path: Path) -> None:
    _seed(tmp_path, "src/d.py", _DEAD)
    _seed(tmp_path, "vendor/d.py", _DEAD)
    rule = NoCommentedOutCode.from_config({"roots": ["src"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"src/d.py"}


def test_run_then_establish_grandfathers(tmp_path: Path) -> None:
    _seed(tmp_path, "src/d.py", _DEAD)
    rule = NoCommentedOutCode.from_config({"roots": ["src"]}, repo_root=tmp_path)
    assert rule.run() == 1
    rule.establish_baseline()
    assert rule.run() == 0


def test_main_establish_baseline_mode(tmp_path: Path) -> None:
    _seed(tmp_path, "d.py", _DEAD)
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / ".architecture" / "baseline" / "no-commented-out-code-files.txt").exists()


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.no_commented_out_code as mod

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
