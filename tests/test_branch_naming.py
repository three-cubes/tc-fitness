"""Tests for the configurable branch-naming engine gate (Task 1.8).

Lifts taz's ``scripts/checks/branch_naming.py`` (Linear ``gitBranchName`` shape
``<user>/<team>-<number>-<slug>``) into the shared engine with the exempt sets
as config — taz keeps ``develop`` in its exempt branches, kairix doesn't. The
branch name is injected (no git dependency in the unit tests); the default
``DEFAULT_LINEAR_PATTERN`` is the Linear shape.
"""

from __future__ import annotations

import re

import pytest

from tc_fitness.checks.branch_naming import (
    DEFAULT_EXEMPT_PATTERNS,
    DEFAULT_LINEAR_PATTERN,
    check_branch,
)


def test_linear_shape_passes() -> None:
    rc = check_branch("dan/kno-45-pr-a-sync-compose")
    assert rc == 0


def test_non_linear_shape_fails() -> None:
    rc = check_branch("feature/random-thing")  # no team-number segment
    assert rc == 1


def test_default_exempt_branches_main() -> None:
    assert check_branch("main") == 0
    assert check_branch("HEAD") == 0


def test_develop_not_exempt_by_default_but_configurable() -> None:
    # kairix: develop is NOT exempt → fails as a non-conforming name.
    assert check_branch("develop") == 1
    # taz: develop added to the exempt set → passes.
    assert check_branch("develop", exempt_branches={"main", "develop", "HEAD"}) == 0


def test_exempt_patterns_default_cover_automation() -> None:
    assert check_branch("worktree-agent-abc123") == 0
    assert check_branch("renovate/some-dep") == 0
    assert check_branch("dependabot/pip/foo") == 0
    assert check_branch("gh-pages") == 0


def test_custom_exempt_patterns_extend() -> None:
    extra = (*DEFAULT_EXEMPT_PATTERNS, re.compile(r"^release/"))
    assert check_branch("release/2026.6", exempt_patterns=extra) == 0
    # Without the extra pattern it fails.
    assert check_branch("release/2026.6") == 1


def test_custom_pattern_overrides_shape() -> None:
    # A repo with a different convention passes its own compiled pattern.
    custom = re.compile(r"^wip-\d+$")
    assert check_branch("wip-7", pattern=custom) == 0
    assert check_branch("dan/kno-45-slug", pattern=custom) == 1


def test_fail_prints_remediation(capsys: pytest.CaptureFixture[str]) -> None:
    rc = check_branch("nope")
    err = capsys.readouterr().err
    assert rc == 1
    assert "nope" in err
    assert "fix:" in err or "rename" in err.lower()


def test_default_pattern_is_the_linear_shape() -> None:
    assert DEFAULT_LINEAR_PATTERN.match("dan/kno-45-slug")
    assert not DEFAULT_LINEAR_PATTERN.match("main")


def test_none_branch_skips_clean(capsys: pytest.CaptureFixture[str]) -> None:
    # Not in a git repo / detached → skip clean (exit 0), never a false fail.
    rc = check_branch(None)
    assert rc == 0
