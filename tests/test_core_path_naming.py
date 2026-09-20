"""Tests for the CORE check path_naming (v0.6.0)."""

from __future__ import annotations

import ast
import runpy
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks.path_naming import (
    build,
    main,
    name_violates_convention,
)

pytestmark = pytest.mark.integration


def _seed(tmp_path: Path, rel: str, body: str = "x\n") -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_rule_from_config_scopes_roots(tmp_path: Path) -> None:
    _seed(tmp_path, "docs/BadNote.md")
    _seed(tmp_path, "docs/good-note.md")
    _seed(tmp_path, "vendor/BadNote.md")
    rule = build({"kebab_roots": ["docs/"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"docs/BadNote.md"}


def test_no_roots_flags_nothing(tmp_path: Path) -> None:
    _seed(tmp_path, "docs/BadNote.md")
    rule = build({}, repo_root=tmp_path)
    assert rule.collect_violations() == set()


def test_snake_root_init_allowed(tmp_path: Path) -> None:
    _seed(tmp_path, "scripts/__init__.py")
    _seed(tmp_path, "scripts/_private_helper.py")
    rule = build({"snake_roots": ["scripts/"]}, repo_root=tmp_path)
    assert rule.collect_violations() == set()


def test_fixed_generated_segments_are_outside_authored_path_scope(tmp_path: Path) -> None:
    rule = build({"kebab_roots": ["docs/"]}, repo_root=tmp_path)
    assert not rule.is_in_scope("docs/node_modules/BadName.md")
    assert rule.is_in_scope("docs/BadName.md")


def test_enumeration_handles_missing_nonfile_cache_and_wrong_extension(tmp_path: Path) -> None:
    _seed(tmp_path, "docs/good-name.md")
    _seed(tmp_path, "docs/readme.txt")
    _seed(tmp_path, "docs/__pycache__/BadName.md")
    (tmp_path / "docs" / "directory.md").mkdir()
    rule = build({"kebab_roots": ["missing/", "docs/"]}, repo_root=tmp_path)

    assert {path.relative_to(tmp_path).as_posix() for path in rule.enumerate_files()} == {"docs/good-name.md"}


def test_cli_executes_with_repo_root(tmp_path: Path) -> None:
    assert main(["--repo-root", str(tmp_path)]) == 0


def test_allowed_name_under_a_kebab_root_is_never_flagged_even_if_not_kebab_case() -> None:
    """A README is exempt by the rule itself now, not by a configurable allow-list."""
    assert not name_violates_convention(
        "docs/README.md",
        kebab_roots=("docs/",),
        snake_roots=(),
    )


def test_extension_with_no_matching_root_convention_is_clean() -> None:
    """A .py under a kebab-only root, or a .md under a snake-only root, is outside either rule."""
    assert not name_violates_convention(
        "docs/Weird.py",
        kebab_roots=("docs/",),
        snake_roots=(),
    )
    assert not name_violates_convention(
        "scripts/Weird.md",
        kebab_roots=(),
        snake_roots=("scripts/",),
    )


def test_python_module_entrypoint_runs_the_real_check(tmp_path: Path) -> None:
    previous_argv = sys.argv
    sys.argv = ["path_naming", "--repo-root", str(tmp_path)]
    try:
        with pytest.raises(SystemExit) as exc:
            runpy.run_path(
                str(Path(__file__).parents[1] / "src/tc_fitness/core_checks/path_naming.py"),
                run_name="__main__",
            )
    finally:
        sys.argv = previous_argv

    assert exc.value.code == 0


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.path_naming as mod

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
