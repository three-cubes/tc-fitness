"""Source discovery and parsing edge cases for cognitive complexity."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from tc_fitness.core_checks.cognitive_complexity import _function_scores, _tree_entries, build

pytestmark = pytest.mark.integration


def _repo(tmp_path: Path, files: dict[str, bytes]) -> Path:
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp_path, check=True)
    author_env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "Test Maintainer",
        "GIT_AUTHOR_EMAIL": "maintainer@example.test",
        "GIT_COMMITTER_NAME": "Test Maintainer",
        "GIT_COMMITTER_EMAIL": "maintainer@example.test",
    }
    for relative, content in files.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "baseline"],
        cwd=tmp_path,
        env=author_env,
        check=True,
    )
    subprocess.run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], cwd=tmp_path, check=True)
    return tmp_path


def _rule(repo: Path):
    return build({"roots": ["src"], "threshold": 2, "base_ref": "origin/main"}, repo_root=repo)


def test_function_scores_returns_empty_for_invalid_syntax() -> None:
    assert _function_scores("def broken(:\n") == {}


def test_tree_entries_skip_regular_non_source_blobs() -> None:
    payload = b"100644 blob abcdef\tsrc/readme.txt\x00"

    assert _tree_entries(payload, (".py",)) == []


def test_function_scores_qualifies_duplicate_class_and_function_ordinals() -> None:
    source = """
class Service:
    def run(self):
        if True:
            pass

class Service:
    def run(self):
        if True:
            if True:
                pass
"""

    assert _function_scores(source) == {
        "Service#0.run#0": 1,
        "Service#1.run#0": 3,
    }


def test_enumeration_skips_missing_and_symlinked_tracked_sources(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {"src/keep.py": b"def keep():\n    return 1\n", "src/missing.py": b""})
    (repo / "src/missing.py").unlink()
    outside = tmp_path.parent / f"{tmp_path.name}-outside.py"
    outside.write_text("def outside():\n    return 1\n", encoding="utf-8")
    (repo / "src/escape.py").symlink_to(outside)

    assert [path.relative_to(repo).as_posix() for path in _rule(repo).enumerate_files()] == ["src/keep.py"]


def test_enumeration_skips_resolved_paths_outside_the_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = _repo(tmp_path, {"src/escape.py": b"def outside():\n    return 1\n"})
    target = repo / "src/escape.py"
    outside = repo.parent / "outside.py"
    original_resolve = Path.resolve

    def resolve(path: Path, *args, **kwargs) -> Path:
        return outside if path == target else original_resolve(path, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", resolve)

    assert _rule(repo).enumerate_files() == []


def test_collect_skips_current_source_that_is_not_valid_utf8(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {"src/invalid.py": b"def clean():\n    return 1\n"})
    (repo / "src/invalid.py").write_bytes(b"\xff")

    assert _rule(repo).collect_violations() == set()


def test_collect_skips_current_source_when_read_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = _repo(tmp_path, {"src/unreadable.py": b"def clean():\n    return 1\n"})
    target = repo / "src/unreadable.py"
    original_read_text = Path.read_text

    def read_text(path: Path, *args, **kwargs):
        if path == target:
            raise PermissionError("fixture denies source read")
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text)

    assert _rule(repo).collect_violations() == set()
