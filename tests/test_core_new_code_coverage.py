"""Tests for the CORE check new_code_coverage.

Mirrors SonarCloud's "Coverage on New Code >= floor" merge condition locally:
for each changed file, the ADDED lines (right side of the diff vs the merge-base)
must clear a coverage floor. The git invocation is a DI seam, so these tests feed
canned ``merge-base`` / ``diff`` output — no real repository, no monkeypatching.
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest
from _core_check_assertions import assert_no_repo_identity

import tc_fitness.core_checks.new_code_coverage as new_code_coverage
from tc_fitness.core_checks.new_code_coverage import (
    build,
    main,
    parse_line_coverage,
)

pytestmark = pytest.mark.integration

# --------------------------------------------------------------------------- #
# Fixtures: a Cobertura report with per-line hits + a canned git runner.
# --------------------------------------------------------------------------- #


def _report(files: dict[str, dict[int, int]], *, source: str = "src") -> str:
    """Render a Cobertura report: ``{filename: {line_no: hits}}``."""
    blocks = []
    for name, lines in files.items():
        line_els = "".join(f'<line number="{n}" hits="{h}"/>' for n, h in lines.items())
        blocks.append(f'<class filename="{name}" line-rate="0.5"><lines>{line_els}</lines></class>')
    classes = "\n".join(blocks)
    return (
        '<?xml version="1.0" ?>\n'
        '<coverage line-rate="0.5" branch-rate="0.5">\n'
        f"  <sources><source>{source}</source></sources>\n"
        f"  <packages><package><classes>\n{classes}\n"
        "  </classes></package></packages>\n"
        "</coverage>\n"
    )


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _completed(args: list[str], rc: int, out: str, err: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=["git", *args], returncode=rc, stdout=out, stderr=err)


def _fake_git(
    *,
    merge_base: str = "0123abc",
    diff: str = "",
    mb_rc: int = 0,
    diff_rc: int = 0,
):
    """A canned git runner returning fixed ``merge-base`` / ``diff`` output."""

    def runner(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        if args and args[0] == "merge-base":
            return _completed(args, mb_rc, merge_base + "\n")
        if args and args[0] == "diff":
            return _completed(args, diff_rc, diff)
        return _completed(args, 0, "")

    return runner


def _diff(path: str, new_start: int, added: list[str], *, new_file: bool = False) -> str:
    """A minimal ``git diff -U0`` for one file adding ``added`` lines at ``new_start``."""
    old = "--- /dev/null" if new_file else f"--- a/{path}"
    header = (
        f"@@ -0,0 +{new_start},{len(added)} @@"
        if new_file
        else f"@@ -{new_start - 1},0 +{new_start},{len(added)} @@"
    )
    body = "".join(f"+{line}\n" for line in added)
    mode = "new file mode 100644\n" if new_file else ""
    return (
        f"diff --git a/{path} b/{path}\n"
        f"{mode}index 1111111..2222222 100644\n"
        f"{old}\n"
        f"+++ b/{path}\n"
        f"{header}\n"
        f"{body}"
    )


def _cfg(**extra: Any) -> Mapping[str, Any]:
    base: dict[str, Any] = {"roots": ["src"], "floor_pct": 80.0, "base_ref": "origin/main"}
    base.update(extra)
    return base


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run real git against a disposable repository."""
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


def _git_repo(tmp_path: Path) -> Path:
    """Create a repository whose current commit is also ``origin/main``."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.name", "Coverage Test")
    _git(repo, "config", "user.email", "coverage-test@example.invalid")
    _seed(repo, "src/a.py", "existing = 1\n")
    _git(repo, "add", "src/a.py")
    _git(repo, "commit", "--quiet", "-m", "base")
    _git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    return repo


def test_default_git_runner_disables_interactive_credentials(tmp_path: Path) -> None:
    """A stale-base refresh must warn/fall back, never block for credentials."""
    repo = _git_repo(tmp_path)
    _git(
        repo,
        "config",
        "alias.print-interactive-env",
        '!printf "%s|%s" "$GIT_TERMINAL_PROMPT" "$GCM_INTERACTIVE"',
    )

    result = new_code_coverage._default_git_runner(["print-interactive-env"], repo)

    assert result.returncode == 0
    assert result.stdout == b"0|Never"


# --------------------------------------------------------------------------- #
# Pure parser: per-line Cobertura coverage.
# --------------------------------------------------------------------------- #


def test_parse_line_coverage_joins_source_and_reads_hits(tmp_path: Path) -> None:
    p = _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 1, 11: 0}, "b.py": {1: 3}}))
    assert parse_line_coverage(p) == {"src/a.py": {10: 1, 11: 0}, "src/b.py": {1: 3}}


def test_parse_line_coverage_dot_source_stays_repo_relative(tmp_path: Path) -> None:
    """A ``<source>.</source>`` root (normalised repo-root coverage — the shape a
    multi-``--cov``-root report is collapsed to for Sonar) keeps the class
    filenames repo-relative. Prepending ``.`` would yield ``./scripts/x.py`` keys
    that never match the repo-relative changed-line paths, so the hard floor would
    silently soft-PASS on every changed file — the exact regression this guards.
    """
    report = _report({"scripts/lib/x.py": {10: 1, 11: 0}}, source=".")
    p = _seed(tmp_path, "coverage.xml", report)
    assert parse_line_coverage(p) == {"scripts/lib/x.py": {10: 1, 11: 0}}


def test_parse_line_coverage_missing_report_empty(tmp_path: Path) -> None:
    assert parse_line_coverage(tmp_path / "nope.xml") == {}


def test_parse_line_coverage_merges_duplicate_class_with_max_hits(tmp_path: Path) -> None:
    xml = (
        "<coverage><sources><source>src</source></sources><packages><package><classes>"
        '<class filename="a.py"><lines><line number="5" hits="0"/></lines></class>'
        '<class filename="a.py"><lines><line number="5" hits="4"/></lines></class>'
        "</classes></package></packages></coverage>"
    )
    p = _seed(tmp_path, "coverage.xml", xml)
    assert parse_line_coverage(p) == {"src/a.py": {5: 4}}  # covered anywhere ⇒ covered


def test_parse_line_coverage_rejects_unsafe_xml(tmp_path: Path) -> None:
    p = _seed(tmp_path, "coverage.xml", "<!DOCTYPE x>\n<coverage/>")
    try:
        parse_line_coverage(p)
    except ValueError as exc:
        assert "DTD/entity" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError for DTD declaration")


# --------------------------------------------------------------------------- #
# Pure parser: added lines from a unified diff.
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# Rule end-to-end via the injected git seam.
# --------------------------------------------------------------------------- #


def test_working_tree_added_lines_match_post_commit_measurement(tmp_path: Path) -> None:
    """Unstaged, staged, and committed forms of one source tree agree."""
    repo = _git_repo(tmp_path)
    _seed(repo, "src/a.py", "existing = 1\nuncovered = 2\n")
    _seed(repo, "coverage.xml", _report({"a.py": {1: 1, 2: 0}}))

    unstaged = build(_cfg(), repo_root=repo)
    unstaged_measurement = unstaged._measured
    unstaged_verdict = unstaged.run()
    _git(repo, "add", "src/a.py")
    staged = build(_cfg(), repo_root=repo)
    staged_measurement = staged._measured
    staged_verdict = staged.run()
    _git(repo, "commit", "--quiet", "-m", "change")
    committed = build(_cfg(), repo_root=repo)
    committed_measurement = committed._measured
    committed_verdict = committed.run()

    assert unstaged_measurement == staged_measurement == committed_measurement == {"src/a.py": (0, 1)}
    assert (unstaged_verdict, staged_verdict, committed_verdict) == (1, 1, 1)


def test_untracked_source_is_measured_before_first_commit(tmp_path: Path) -> None:
    """A new source file cannot disappear from the local changed-line floor."""
    repo = _git_repo(tmp_path)
    _seed(repo, "src/new.py", "uncovered = 1\n")
    _seed(repo, "coverage.xml", _report({"new.py": {1: 0}}))

    rule = build(_cfg(), repo_root=repo)

    assert rule.run() == 1


@pytest.mark.skipif(sys.platform == "darwin", reason="macOS rejects invalid UTF-8 filenames")
def test_untracked_source_with_non_utf8_filename_is_enumerated_losslessly(tmp_path: Path) -> None:
    """Git's byte-preserving path output must not abort the local gate."""
    repo = _git_repo(tmp_path)
    raw_name = b"bad_\xff.py"
    raw_path = os.path.join(os.fsencode(repo), b"src", raw_name)
    descriptor = os.open(raw_path, os.O_WRONLY | os.O_CREAT, 0o600)
    try:
        os.write(descriptor, b"uncovered = 1\n")
    finally:
        os.close(descriptor)

    rule = build(_cfg(), repo_root=repo)

    decoded_name = raw_name.decode("utf-8", "surrogateescape")
    assert rule._changed_lines()[f"src/{decoded_name}"] == {1}


def test_ignored_untracked_source_does_not_change_the_ci_equivalent_tree(tmp_path: Path) -> None:
    """Build residue excluded by Git remains outside local measurement."""
    repo = _git_repo(tmp_path)
    _seed(repo, ".gitignore", "src/generated.py\n")
    _seed(repo, "src/generated.py", "uncovered = 1\n")
    _seed(repo, "coverage.xml", _report({"generated.py": {1: 0}}))

    rule = build(_cfg(), repo_root=repo)

    assert rule.run() == 0


def test_stale_remote_base_is_refreshed_before_exact_merge_base(tmp_path: Path) -> None:
    """A stale remote-tracking ref is refreshed before it defines new code."""
    calls: list[list[str]] = []
    refreshed = False

    def runner(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        nonlocal refreshed
        calls.append(args)
        if args == ["remote"]:
            return _completed(args, 0, "origin\nupstream\n")
        if args[0] == "fetch":
            assert args == [
                "fetch",
                "--quiet",
                "--no-tags",
                "--",
                "upstream",
                "+refs/heads/release/next:refs/remotes/upstream/release/next",
            ]
            refreshed = True
            return _completed(args, 0, "")
        if args[0] == "merge-base":
            assert refreshed
            assert args == ["merge-base", "upstream/release/next", "HEAD"]
            return _completed(args, 0, "fresh-base\n")
        if args[0] == "diff":
            assert args == ["diff", "-U0", "fresh-base", "--"]
            return _completed(args, 0, _diff("src/a.py", 2, ["new = 1"]))
        if args[0] == "ls-files":
            return _completed(args, 0, "")
        raise AssertionError(f"unexpected git argv: {args}")

    rule = build(_cfg(base_ref="upstream/release/next"), repo_root=tmp_path, git_runner=runner)

    assert rule._changed_lines() == {"src/a.py": {2}}
    assert calls[:3] == [
        ["remote"],
        [
            "fetch",
            "--quiet",
            "--no-tags",
            "--",
            "upstream",
            "+refs/heads/release/next:refs/remotes/upstream/release/next",
        ],
        ["merge-base", "upstream/release/next", "HEAD"],
    ]


def test_real_stale_remote_tracking_ref_is_advanced(tmp_path: Path) -> None:
    """The production runner repairs an actually stale remote-tracking ref."""
    repo = _git_repo(tmp_path)
    remote = tmp_path / "origin.git"
    _git(tmp_path, "init", "--bare", "--quiet", str(remote))
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    stale = _git(repo, "rev-parse", "HEAD").stdout.strip()

    _seed(repo, "src/trunk.py", "trunk = 1\n")
    _git(repo, "add", "src/trunk.py")
    _git(repo, "commit", "--quiet", "-m", "advance trunk")
    fresh = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "push", "--quiet", "origin", "HEAD:refs/heads/main")
    _git(repo, "reset", "--hard", "--quiet", stale)
    _git(repo, "update-ref", "refs/remotes/origin/main", stale)

    build(_cfg(), repo_root=repo)._changed_lines()

    assert _git(repo, "rev-parse", "origin/main").stdout.strip() == fresh


def test_remote_refresh_failure_uses_cached_base_with_visible_diagnostic(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Offline runs keep measuring against the cached ref and say so."""

    def runner(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        if args == ["remote"]:
            return _completed(args, 0, "origin\n")
        if args[0] == "fetch":
            return _completed(args, 128, "", "network unavailable\n")
        if args[0] == "merge-base":
            return _completed(args, 0, "cached-base\n")
        if args[0] == "diff":
            return _completed(args, 0, _diff("src/a.py", 2, ["new = 1"]))
        if args[0] == "ls-files":
            return _completed(args, 0, "")
        raise AssertionError(f"unexpected git argv: {args}")

    rule = build(_cfg(), repo_root=tmp_path, git_runner=runner)

    assert rule._changed_lines() == {"src/a.py": {2}}
    diagnostic = capsys.readouterr().err
    assert "could not refresh origin/main" in diagnostic
    assert "using cached ref" in diagnostic
    assert "network unavailable" in diagnostic


def test_below_floor_changed_lines_are_a_violation(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 1, 11: 0, 12: 0}}))
    diff = _diff("src/a.py", 10, ["x = 1", "y = 2", "z = 3"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(diff=diff))
    # 1 of 3 added coverable lines covered = 33% < 80 → violation.
    assert {str(p) for p in rule.collect_violations()} == {"src/a.py"}


def test_fully_covered_changed_lines_pass(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 1, 11: 1, 12: 1}}))
    diff = _diff("src/a.py", 10, ["x = 1", "y = 2", "z = 3"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(diff=diff))
    assert rule.collect_violations() == set()


def test_floor_is_config_driven(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 1, 11: 1, 12: 0, 13: 0}}))  # 50% covered
    diff = _diff("src/a.py", 10, ["a", "b", "c", "d"])
    # floor 80 → violation; floor 50 → clean (50% is not below 50).
    assert {
        str(p)
        for p in build(
            _cfg(floor_pct=80.0), repo_root=tmp_path, git_runner=_fake_git(diff=diff)
        ).collect_violations()
    } == {"src/a.py"}
    assert (
        build(_cfg(floor_pct=50.0), repo_root=tmp_path, git_runner=_fake_git(diff=diff)).collect_violations()
        == set()
    )


def test_roots_scope_the_violation_set(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 0, 11: 0}}, source="vendor"))
    diff = _diff("vendor/a.py", 10, ["x = 1", "y = 2"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(diff=diff))
    assert rule.collect_violations() == set()  # vendor/a.py is out of the src root


def test_changed_lines_with_no_report_entry_are_not_measurable(tmp_path: Path) -> None:
    # The report records lines 1-2 for src/a.py, but the change added lines
    # 10-12 (blank lines / comments the report never recorded) → no coverable
    # new code → not a violation.
    _seed(tmp_path, "coverage.xml", _report({"a.py": {1: 1, 2: 1}}))
    diff = _diff("src/a.py", 10, ["# a", "# b", "# c"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(diff=diff))
    assert rule.collect_violations() == set()


def test_file_absent_from_report_is_skipped(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"other.py": {1: 1}}))
    diff = _diff("src/a.py", 10, ["x = 1"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(diff=diff))
    assert rule.collect_violations() == set()


# --------------------------------------------------------------------------- #
# Soft-skip paths: no report / no changes / git unavailable / unsafe ref.
# --------------------------------------------------------------------------- #


def test_no_coverage_report_is_a_soft_pass(tmp_path: Path) -> None:
    diff = _diff("src/a.py", 10, ["x = 1"])  # changes exist, but no report to score
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(diff=diff))
    assert rule.run() == 0


def test_no_changed_files_passes(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 0}}))
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(diff=""))
    assert rule.run() == 0


def test_merge_base_unavailable_is_a_soft_pass(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 0}}))
    diff = _diff("src/a.py", 10, ["x = 1"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(diff=diff, mb_rc=1))
    assert rule.run() == 0


def test_unsafe_base_ref_skips_without_touching_git(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 0}}))

    def exploding_runner(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        raise AssertionError("git must not run for an unsafe base ref")

    rule = build(_cfg(base_ref="main; rm -rf /"), repo_root=tmp_path, git_runner=exploding_runner)
    assert rule.run() == 0
    assert rule.collect_violations() == set()


# --------------------------------------------------------------------------- #
# Hard floor: new code is non-grandfatherable.
# --------------------------------------------------------------------------- #


def test_run_fails_hard_and_baseline_grandfathers_nothing(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 0}}))
    diff = _diff("src/a.py", 10, ["x = 1"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(diff=diff))
    assert rule.run() == 1
    rule.establish_baseline()
    # Unlike coverage_floor, establishing does NOT grandfather the offender: the
    # baseline is frozen EMPTY, so the floor stays hard and the run still FAILs.
    assert rule.run() == 1
    baseline = tmp_path / ".architecture" / "baseline" / "new-code-coverage-files.txt"
    entries = [
        ln
        for ln in baseline.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]
    assert entries == []


def test_hand_crafted_baseline_cannot_soften_the_floor(tmp_path: Path) -> None:
    # Even a MANUALLY written baseline naming the offender is ignored: run()
    # consults no baseline at all, so the hard floor holds.
    _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 0}}))
    baseline = tmp_path / ".architecture" / "baseline" / "new-code-coverage-files.txt"
    baseline.parent.mkdir(parents=True, exist_ok=True)
    baseline.write_text("# hand-crafted grandfather attempt\nsrc/a.py\n", encoding="utf-8")
    diff = _diff("src/a.py", 10, ["x = 1"])
    rule = build(_cfg(), repo_root=tmp_path, git_runner=_fake_git(diff=diff))
    assert rule.run() == 1


def test_main_establish_baseline_writes_empty_baseline(tmp_path: Path) -> None:
    _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 0}}))
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    baseline = tmp_path / ".architecture" / "baseline" / "new-code-coverage-files.txt"
    assert baseline.exists()
    entries = [
        ln
        for ln in baseline.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]
    assert entries == []  # new code is non-grandfatherable


# --------------------------------------------------------------------------- #
# Design law: the CORE module carries zero repo identity in executable code.
# --------------------------------------------------------------------------- #


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.new_code_coverage as mod

    assert_no_repo_identity(mod.__file__)
