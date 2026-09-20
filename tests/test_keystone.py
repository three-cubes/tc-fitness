"""Tests for the keystone drift-enders (v0.6.0)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tc_fitness.baseline import establish_baseline
from tc_fitness.keystone import (
    added_since_tag,
    baseline_shrink_only,
    load_all_baselines,
    net_new_violations_forbidden,
    resolve_previous_tag,
    staged_added_files,
)

pytestmark = pytest.mark.integration


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _init_repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "Test")
    return tmp_path


# ── net_new_violations_forbidden ──────────────────────────────────────────


def test_load_all_baselines(tmp_path: Path) -> None:
    establish_baseline("rule-a", ["src/x.py"], tmp_path)
    establish_baseline("rule-b", ["src/y.py"], tmp_path)
    loaded = load_all_baselines(tmp_path)
    assert loaded["rule-a-files.txt"] == {"src/x.py"}
    assert loaded["rule-b-files.txt"] == {"src/y.py"}


def test_load_all_baselines_is_empty_before_the_directory_exists(tmp_path: Path) -> None:
    assert load_all_baselines(tmp_path) == {}


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

    outside_repo = tmp_path.parent / f"{tmp_path.name}-not-a-repo"
    outside_repo.mkdir()
    assert staged_added_files(outside_repo) == []


def test_net_new_violations_forbidden_clean(tmp_path: Path) -> None:
    establish_baseline("r", ["src/old.py"], tmp_path)
    assert net_new_violations_forbidden(["src/brand-new.py"], tmp_path, print_fn=lambda _m: None) == 0


def test_net_new_violations_forbidden_blocks_grandfathered_add(tmp_path: Path) -> None:
    establish_baseline("r", ["src/old.py"], tmp_path)
    # An ADDED file that is already in the baseline → fail.
    assert net_new_violations_forbidden(["src/old.py"], tmp_path, print_fn=lambda _m: None) == 1


def test_net_new_violation_prints_the_supplied_remediation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    establish_baseline("r", ["src/old.py"], tmp_path)

    result = net_new_violations_forbidden(["src/old.py"], tmp_path, remediation="remove the entry")

    assert result == 1
    output = capsys.readouterr().out
    assert "src/old.py" in output
    assert "remove the entry" in output


# ── baseline_shrink_only ──────────────────────────────────────────────────


def test_shrink_only_first_release_skips(tmp_path: Path) -> None:
    _init_repo(tmp_path)
    rc = baseline_shrink_only(["a-files.txt"], tmp_path, print_fn=lambda _m: None)
    assert rc == 0  # no prior tag → clean skip


def test_shrink_only_passes_when_baseline_shrinks(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    rel = ".architecture/baseline/r-files.txt"
    establish_baseline("r", ["a", "b", "c"], repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    _git(repo, "tag", "v0.1.0")
    # Pay one entry down.
    establish_baseline("r", ["a", "b"], repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "shrink")
    assert baseline_shrink_only([rel], repo, print_fn=lambda _m: None) == 0


def test_shrink_only_fails_when_baseline_grows(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    rel = ".architecture/baseline/r-files.txt"
    establish_baseline("r", ["a"], repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    _git(repo, "tag", "v0.1.0")
    establish_baseline("r", ["a", "b"], repo)  # grew
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "grow")
    assert baseline_shrink_only([rel], repo, print_fn=lambda _m: None) == 1


def test_shrink_only_fails_when_baseline_stalls_above_zero(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    rel = ".architecture/baseline/r-files.txt"
    establish_baseline("r", ["a", "b"], repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    _git(repo, "tag", "v0.1.0")
    _seed = repo / "x.txt"
    _seed.write_text("x")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "no baseline change")
    assert baseline_shrink_only([rel], repo, print_fn=lambda _m: None) == 1


def test_shrink_only_accepts_a_baseline_reduced_to_zero(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    rel = ".architecture/baseline/r-files.txt"
    establish_baseline("r", ["a"], repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    _git(repo, "tag", "v0.1.0")

    (repo / rel).unlink()
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "pay down all debt")

    assert baseline_shrink_only([rel], repo, prev_tag="v0.1.0") == 0


def test_shrink_only_reports_missing_previous_baseline_with_remediation(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _init_repo(tmp_path)
    rel = ".architecture/baseline/r-files.txt"
    (repo / "seed.txt").write_text("seed\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    _git(repo, "tag", "v0.1.0")
    establish_baseline("r", ["new-debt"], repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "introduce baseline")

    result = baseline_shrink_only([rel], repo, prev_tag="v0.1.0", remediation="reduce the baseline")

    output = capsys.readouterr().out
    assert result == 1
    assert "prev=0 head=1" in output
    assert "reduce the baseline" in output


def test_shrink_only_accepts_an_empty_governed_set(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    result = baseline_shrink_only([], tmp_path, prev_tag="v0.1.0")

    assert result == 0
    assert "all 0 governed baseline(s)" in capsys.readouterr().out


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


def test_resolve_previous_tag_returns_none_before_a_second_commit(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    (repo / "a.txt").write_text("a")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "first")

    assert resolve_previous_tag(repo) is None


# ── catalogue_check_consistency ───────────────────────────────────────────
