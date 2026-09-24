"""Regression coverage for cognitive complexity path moves and empty roots."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from tc_fitness.core_checks.cognitive_complexity import build

pytestmark = pytest.mark.integration


def _nested(depth: int) -> str:
    lines = ["def f(value):"]
    lines.extend(f"{'    ' * level}if value:" for level in range(1, depth + 1))
    lines.append(f"{'    ' * (depth + 1)}return 1")
    return "\n".join(lines) + "\n"


def _commit(repo: Path, message: str) -> None:
    author_env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "Test Maintainer",
        "GIT_AUTHOR_EMAIL": "maintainer@example.test",
        "GIT_COMMITTER_NAME": "Test Maintainer",
        "GIT_COMMITTER_EMAIL": "maintainer@example.test",
    }
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(
        ["git", "-c", "commit.gpgsign=false", "commit", "-q", "-m", message],
        cwd=repo,
        env=author_env,
        check=True,
    )


def _repo(tmp_path: Path, files: dict[str, str]) -> Path:
    repo = tmp_path.resolve()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    for relative, content in files.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    _commit(repo, "baseline")
    subprocess.run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], cwd=repo, check=True)
    return repo


def _rename_and_commit(repo: Path, old_relative: str, new_relative: str, content: str) -> None:
    old_path = repo / old_relative
    new_path = repo / new_relative
    new_path.parent.mkdir(parents=True, exist_ok=True)
    old_path.rename(new_path)
    new_path.write_text(content, encoding="utf-8")
    _commit(repo, "move source")


def test_unchanged_over_threshold_file_renamed_to_new_path_passes(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {"src/old.py": _nested(3)})
    _rename_and_commit(repo, "src/old.py", "src/new.py", _nested(3))

    rule = build({"roots": ["src"], "threshold": 1}, repo_root=repo)

    assert rule.collect_violations() == set()


def test_renamed_file_with_worsened_complexity_fails(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {"src/old.py": _nested(2)})
    _rename_and_commit(repo, "src/old.py", "src/new.py", _nested(3))

    rule = build({"roots": ["src"], "threshold": 1}, repo_root=repo)

    assert rule.collect_violations() == {Path("src/new.py")}


def test_unstaged_filesystem_move_preserves_legacy_function_baseline(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {"src/old.py": _nested(3)})
    (repo / "src/old.py").rename(repo / "src/new.py")

    rule = build({"roots": ["src"], "threshold": 1}, repo_root=repo)

    assert rule.collect_violations() == set()


def test_empty_roots_are_noop_and_explicit_repository_root_scans(tmp_path: Path) -> None:
    repo = _repo(
        tmp_path,
        {
            "src/changed.py": "def f(value):\n    return value\n",
            "other/unchanged.py": "def g(value):\n    return value\n",
        },
    )
    changed = repo / "src/changed.py"
    changed.write_text(_nested(3), encoding="utf-8")
    _commit(repo, "introduce complex function")

    no_roots = build({"threshold": 1}, repo_root=repo)
    all_roots = build({"roots": ["."], "threshold": 1}, repo_root=repo)
    no_root_files = no_roots.enumerate_files()
    no_root_violations = no_roots.collect_violations()
    all_root_violations = all_roots.collect_violations()

    assert no_root_files == []
    assert no_root_violations == set()
    assert {path.as_posix() for path in all_root_violations} == {"src/changed.py"}
