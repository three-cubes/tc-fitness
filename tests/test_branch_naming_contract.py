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
    check_branch,
)

pytestmark = pytest.mark.contract


def test_fail_prints_remediation(capsys: pytest.CaptureFixture[str]) -> None:
    rc = check_branch("nope")
    err = capsys.readouterr().err
    assert rc == 1
    assert "nope" in err
    assert "fix:" in err or "rename" in err.lower()


def test_none_branch_skips_clean(capsys: pytest.CaptureFixture[str]) -> None:
    # Not in a git repo / detached → skip clean (exit 0), never a false fail.
    rc = check_branch(None)
    assert rc == 0


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
