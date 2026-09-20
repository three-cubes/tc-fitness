"""Tests for the keystone drift-enders (v0.6.0)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from tc_fitness.keystone import (
    catalogue_check_consistency,
    find_net_new_violations,
    reconcile_catalogue,
)

pytestmark = pytest.mark.unit


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _init_repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "Test")
    return tmp_path


# ── net_new_violations_forbidden ──────────────────────────────────────────


def test_find_net_new_hits() -> None:
    baselines = {"r-files.txt": {"src/old.py"}}
    assert find_net_new_violations(["src/old.py"], baselines) == {"r-files.txt": ["src/old.py"]}
    assert find_net_new_violations(["src/new.py"], baselines) == {}


# ── baseline_shrink_only ──────────────────────────────────────────────────


# ── catalogue_check_consistency ───────────────────────────────────────────


def test_reconcile_clean() -> None:
    report = reconcile_catalogue(
        cataloged_check_ids=["core:a", "core:b"],
        available_check_ids=["core:a", "core:b"],
    )
    assert report.ok


def test_reconcile_orphan_check() -> None:
    report = reconcile_catalogue(
        cataloged_check_ids=["core:a"],
        available_check_ids=["core:a", "core:b"],
    )
    assert report.orphan_checks == ["core:b"]
    assert not report.ok


def test_reconcile_dangling_entry() -> None:
    report = reconcile_catalogue(
        cataloged_check_ids=["core:a", "core:missing"],
        available_check_ids=["core:a"],
    )
    assert report.dangling_entries == [("core:missing", "core:missing")]
    assert not report.ok


def test_catalogue_check_consistency_exit_codes() -> None:
    ok = catalogue_check_consistency(
        cataloged_check_ids=["x"],
        available_check_ids=["x"],
        print_fn=lambda _m: None,
    )
    assert ok == 0
    bad = catalogue_check_consistency(
        cataloged_check_ids=["x", "y"],
        available_check_ids=["x"],
        print_fn=lambda _m: None,
    )
    assert bad == 1
