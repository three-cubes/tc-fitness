"""Regression tests for reading cognitive-complexity baselines from Git trees."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from tc_fitness.core_checks.cognitive_complexity import build

pytestmark = pytest.mark.integration


def _repo(root: Path, files: dict[str, bytes]) -> Path:
    """Create a base commit and expose it as the configured remote-tracking ref."""
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    author_env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "Test Maintainer",
        "GIT_AUTHOR_EMAIL": "maintainer@example.test",
        "GIT_COMMITTER_NAME": "Test Maintainer",
        "GIT_COMMITTER_EMAIL": "maintainer@example.test",
    }
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(
        ["git", "-c", "commit.gpgsign=false", "commit", "-q", "-m", "baseline"],
        cwd=root,
        env=author_env,
        check=True,
    )
    subprocess.run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], cwd=root, check=True)
    return root


def _complex_source(depth: int = 3) -> bytes:
    lines = ["def handle(value):"]
    lines.extend(f"{'    ' * level}if value:" for level in range(1, depth + 1))
    lines.append(f"{'    ' * (depth + 1)}return 1")
    return ("\n".join(lines) + "\n").encode()


def _rule(root: Path):
    return build(
        {"roots": ["src"], "threshold": 2, "base_ref": "origin/main"},
        repo_root=root,
    )


def test_export_ignored_tracked_source_is_still_used_as_baseline(tmp_path: Path) -> None:
    repo = _repo(
        tmp_path,
        {
            ".gitattributes": b"src/*.py export-ignore\n",
            "src/legacy.py": _complex_source(),
        },
    )

    assert _rule(repo).collect_violations() == set()


def test_root_absent_at_merge_base_is_an_empty_baseline(tmp_path: Path) -> None:
    repo = _repo(tmp_path, {"README.md": b"base has no configured source root\n"})
    candidate = repo / "src" / "new.py"
    candidate.parent.mkdir(parents=True)
    candidate.write_bytes(_complex_source())

    rule = _rule(repo)

    assert rule._baseline_sources() == {}
    assert rule.collect_violations() == {Path("src/new.py")}


def test_invalid_baseline_file_does_not_discard_other_baseline_sources(tmp_path: Path) -> None:
    valid = _complex_source()
    repo = _repo(
        tmp_path,
        {
            "src/valid.py": valid,
            "src/invalid.py": b"def invalid():\n    return \xff\n",
        },
    )

    baseline = _rule(repo)._baseline_sources()

    assert isinstance(baseline, dict)
    assert baseline == {"src/valid.py": valid.decode("utf-8")}
