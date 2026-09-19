"""Integration tests for Git-backed keystone discovery helpers."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tc_fitness.keystone import added_since_tag, resolve_previous_tag, staged_added_files

pytestmark = pytest.mark.integration


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _init_repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "Test")
    return tmp_path


def test_added_file_queries_follow_real_staged_and_tagged_git_diffs(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    (repo / "seed.txt").write_text("seed\n")
    _git(repo, "add", "seed.txt")
    _git(repo, "commit", "-q", "-m", "seed")
    _git(repo, "tag", "v1.0.0")
    (repo / "new.txt").write_text("new\n")
    _git(repo, "add", "new.txt")
    assert staged_added_files(repo) == ["new.txt"]
    _git(repo, "commit", "-q", "-m", "add new file")
    assert added_since_tag(repo, "v1.0.0") == ["new.txt"]

    not_a_repo = tmp_path / "not-a-repo"
    not_a_repo.mkdir()
    assert staged_added_files(not_a_repo) == []
    bare_repo = tmp_path / "bare.git"
    _git(tmp_path, "init", "--bare", str(bare_repo))
    assert staged_added_files(bare_repo) == []
    assert added_since_tag(repo, "missing-tag") == []


def test_resolve_previous_tag(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    (repo / "a.txt").write_text("a")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c1")
    _git(repo, "tag", "v0.1.0")
    (repo / "b.txt").write_text("b")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c2")
    assert resolve_previous_tag(repo) == "v0.1.0"
