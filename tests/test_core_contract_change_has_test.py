"""Tests for the CORE check contract_change_has_test.

A change that touches a *contract-surface* file (the shared base every consumer
inherits) but touches NO *test* file is the exact class that let the v0.13.0
empty-roots regression ship: ``fitness_rule.py`` changed, no test proved the new
behaviour, and the break reached ``main``. This gate mirrors the merge condition
LOCALLY — a contract-surface change without a companion test change FAILs.

The changed-file list is sourced the same way :mod:`new_code_coverage` sources
it — a ``git merge-base`` + ``git diff`` DI seam — so these tests feed canned
``merge-base`` / ``--name-only`` output: no real repository, no monkeypatching.
"""

from __future__ import annotations

import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from _core_check_assertions import assert_no_repo_identity

from tc_fitness.core_checks.contract_change_has_test import build, main

# --------------------------------------------------------------------------- #
# Fixtures: a canned git runner returning fixed merge-base + --name-only output.
# --------------------------------------------------------------------------- #


def _completed(args: list[str], rc: int, out: str) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=["git", *args], returncode=rc, stdout=out, stderr="")


def _fake_git(
    *,
    changed: list[str] | None = None,
    merge_base: str = "0123abc",
    mb_rc: int = 0,
    diff_rc: int = 0,
):
    """A canned git runner returning fixed ``merge-base`` / ``diff --name-only`` output."""
    names = "".join(f"{p}\n" for p in (changed or []))

    def runner(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        if args and args[0] == "merge-base":
            return _completed(args, mb_rc, merge_base + "\n")
        if args and args[0] == "diff":
            return _completed(args, diff_rc, names)
        return _completed(args, 0, "")

    return runner


def _cfg(**extra: Any) -> Mapping[str, Any]:
    base: dict[str, Any] = {
        "contract_surface": ["src/tc_fitness/fitness_rule.py"],
        "test_globs": ["tests/**"],
        "base_ref": "origin/main",
    }
    base.update(extra)
    return base


# --------------------------------------------------------------------------- #
# The three canonical cases.
# --------------------------------------------------------------------------- #


def test_contract_change_without_test_is_a_violation(tmp_path: Path) -> None:
    # The v0.13.0 shape: the shared contract base changed, no test changed.
    git = _fake_git(changed=["src/tc_fitness/fitness_rule.py"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=git)
    assert {str(p) for p in rule.collect_violations()} == {"src/tc_fitness/fitness_rule.py"}
    assert rule.run() == 1


def test_contract_change_with_test_change_is_clean(tmp_path: Path) -> None:
    git = _fake_git(
        changed=["src/tc_fitness/fitness_rule.py", "tests/test_fitness_rule.py"],
    )
    rule = build(_cfg(), repo_root=tmp_path, git_runner=git)
    assert rule.collect_violations() == set()
    assert rule.run() == 0


def test_no_contract_change_is_a_noop(tmp_path: Path) -> None:
    # No contract-surface file in the change set → nothing to enforce → clean.
    git = _fake_git(changed=["README.md", "docs/notes.md", "src/tc_fitness/gate.py"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=git)
    assert rule.collect_violations() == set()
    assert rule.run() == 0


# --------------------------------------------------------------------------- #
# Config-driven surfaces + multiple contract files.
# --------------------------------------------------------------------------- #


def test_contract_surface_is_config_driven(tmp_path: Path) -> None:
    git = _fake_git(changed=["src/tc_fitness/gate.py"])
    # Default surface (fitness_rule.py) → gate.py is not a contract file → clean.
    assert build(_cfg(), repo_root=tmp_path, git_runner=git).collect_violations() == set()
    # Widen the surface to the whole package → gate.py IS a contract file, no test → violation.
    widened = build(
        _cfg(contract_surface=["src/tc_fitness/**"]),
        repo_root=tmp_path,
        git_runner=git,
    )
    assert {str(p) for p in widened.collect_violations()} == {"src/tc_fitness/gate.py"}


def test_test_globs_are_config_driven(tmp_path: Path) -> None:
    # A test change under a NON-default location only counts when test_globs says so.
    git = _fake_git(changed=["src/tc_fitness/fitness_rule.py", "spec/rule_spec.py"])
    # Default test_globs = tests/** → spec/ change does not count → violation.
    assert build(_cfg(), repo_root=tmp_path, git_runner=git).run() == 1
    # Widen test_globs to include spec/ → the change now counts → clean.
    assert build(_cfg(test_globs=["tests/**", "spec/**"]), repo_root=tmp_path, git_runner=git).run() == 0


def test_every_touched_contract_file_is_reported(tmp_path: Path) -> None:
    git = _fake_git(changed=["src/tc_fitness/a.py", "src/tc_fitness/b.py"])
    rule = build(
        _cfg(contract_surface=["src/tc_fitness/**"]),
        repo_root=tmp_path,
        git_runner=git,
    )
    assert {str(p) for p in rule.collect_violations()} == {
        "src/tc_fitness/a.py",
        "src/tc_fitness/b.py",
    }


# --------------------------------------------------------------------------- #
# Soft-skip paths: no changes / merge-base unavailable / unsafe ref.
# --------------------------------------------------------------------------- #


def test_no_changed_files_passes(tmp_path: Path) -> None:
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(changed=[]))
    assert rule.run() == 0


def test_merge_base_unavailable_is_a_soft_pass(tmp_path: Path) -> None:
    git = _fake_git(changed=["src/tc_fitness/fitness_rule.py"], mb_rc=1)
    rule = build(_cfg(), repo_root=tmp_path, git_runner=git)
    assert rule.run() == 0
    assert rule.collect_violations() == set()


def test_diff_failure_is_a_soft_pass(tmp_path: Path) -> None:
    git = _fake_git(changed=["src/tc_fitness/fitness_rule.py"], diff_rc=1)
    rule = build(_cfg(), repo_root=tmp_path, git_runner=git)
    assert rule.run() == 0


def test_unsafe_base_ref_skips_without_touching_git(tmp_path: Path) -> None:
    def exploding_runner(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        raise AssertionError("git must not run for an unsafe base ref")

    rule = build(_cfg(base_ref="main; rm -rf /"), repo_root=tmp_path, git_runner=exploding_runner)
    assert rule.run() == 0
    assert rule.collect_violations() == set()


# --------------------------------------------------------------------------- #
# Hard floor: a contract change without a test is non-grandfatherable.
# --------------------------------------------------------------------------- #


def test_run_fails_hard_and_baseline_grandfathers_nothing(tmp_path: Path) -> None:
    git = _fake_git(changed=["src/tc_fitness/fitness_rule.py"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=git)
    assert rule.run() == 1
    rule.establish_baseline()
    # Establishing does NOT grandfather the offender: the baseline is frozen
    # EMPTY, so the gate stays hard and the run still FAILs.
    assert rule.run() == 1
    baseline = tmp_path / ".architecture" / "baseline" / "contract-change-has-test-files.txt"
    entries = [
        ln
        for ln in baseline.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]
    assert entries == []


def test_main_establish_baseline_writes_empty_baseline(tmp_path: Path) -> None:
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    baseline = tmp_path / ".architecture" / "baseline" / "contract-change-has-test-files.txt"
    assert baseline.exists()
    entries = [
        ln
        for ln in baseline.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]
    assert entries == []  # a missing test for a contract change is non-grandfatherable


# --------------------------------------------------------------------------- #
# Design law: the CORE module carries zero repo identity in executable code.
# --------------------------------------------------------------------------- #


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.contract_change_has_test as mod

    assert_no_repo_identity(mod.__file__)
