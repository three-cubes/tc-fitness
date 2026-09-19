"""Tests for the configurable branch-naming engine gate (Task 1.8).

Lifts taz's ``scripts/checks/branch_naming.py`` (Linear ``gitBranchName`` shape
``<user>/<team>-<number>-<slug>``) into the shared engine with the exempt sets
as config — taz keeps ``develop`` in its exempt branches, kairix doesn't. The
branch name is injected (no git dependency in the unit tests); the default
``DEFAULT_LINEAR_PATTERN`` is the Linear shape.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tc_fitness.checks.branch_naming import (
    GITHUB_HEAD_REF_ENV,
    check_branch,
    current_branch,
)

pytestmark = pytest.mark.integration


# ── PR-event detached-HEAD resolution (the gate must BITE on PRs) ────────────
#
# On a GitHub ``pull_request`` event the runner checks out the merge commit in
# DETACHED HEAD, so ``git rev-parse --abbrev-ref HEAD`` returns the literal
# ``"HEAD"`` (which is exempt) and the branch-naming rule would silently no-op.
# ``current_branch`` must resolve ``$GITHUB_HEAD_REF`` first so the gate checks
# the ACTUAL PR source-branch name. These tests inject ``env`` + a tmp git repo
# explicitly — no real environment mutation, no network, fully deterministic.


def _init_detached_repo(tmp_path: Path) -> Path:
    """A throwaway git repo left in DETACHED HEAD — the PR-checkout shape.

    Reproduces what a GitHub ``pull_request`` checkout looks like locally:
    ``git rev-parse --abbrev-ref HEAD`` resolves to the literal ``"HEAD"``.
    """
    run = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True)  # noqa: E731
    run("init", "-q")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "t")
    run("commit", "--allow-empty", "-q", "-m", "c0")
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    run("checkout", "-q", sha)  # detach HEAD onto the commit SHA
    abbrev = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=tmp_path, text=True
    ).strip()
    assert abbrev == "HEAD", f"expected detached HEAD, got {abbrev!r}"
    return tmp_path


def test_pr_event_resolves_head_ref_over_detached_head(tmp_path: Path) -> None:
    # On a PR event the env var wins over the detached `git` "HEAD" — the gate
    # sees the real source-branch name, not the exempt literal "HEAD".
    repo = _init_detached_repo(tmp_path)
    branch = current_branch(repo, env={GITHUB_HEAD_REF_ENV: "feature/random-thing"})
    assert branch == "feature/random-thing"


def test_detached_head_without_pr_ref_skips_clean(tmp_path: Path) -> None:
    # Detached HEAD and NO PR env var (e.g. a local detached checkout) → the
    # literal "HEAD" is mapped to None (a clean skip), never a false failure.
    repo = _init_detached_repo(tmp_path)
    assert current_branch(repo, env={}) is None
    assert check_branch(current_branch(repo, env={})) == 0


def test_empty_head_ref_falls_back_to_git(tmp_path: Path) -> None:
    # GITHUB_HEAD_REF is set but EMPTY on non-PR events (push). It must be
    # ignored so the real branch name is resolved from git.
    run = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True)  # noqa: E731
    run("init", "-q")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "t")
    run("commit", "--allow-empty", "-q", "-m", "c0")
    run("checkout", "-q", "-b", "dan/sgo-106-real-branch")
    branch = current_branch(tmp_path, env={GITHUB_HEAD_REF_ENV: ""})
    assert branch == "dan/sgo-106-real-branch"


def test_push_event_uses_git_branch(tmp_path: Path) -> None:
    # No PR env var at all → the local/push branch name comes from git.
    run = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True)  # noqa: E731
    run("init", "-q")
    run("config", "user.email", "t@example.com")
    run("config", "user.name", "t")
    run("commit", "--allow-empty", "-q", "-m", "c0")
    run("checkout", "-q", "-b", "broken-thing")
    branch = current_branch(tmp_path, env={})
    assert branch == "broken-thing"
    assert check_branch(branch) == 1  # the gate bites on push too
