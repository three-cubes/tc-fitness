"""Tests for the CORE check new_code_coverage.

Mirrors SonarCloud's "Coverage on New Code >= floor" merge condition locally:
for each changed file, the ADDED lines (right side of the diff vs the merge-base)
must clear a coverage floor. The git invocation is a DI seam, so these tests feed
canned ``merge-base`` / ``diff`` output — no real repository, no monkeypatching.
"""

from __future__ import annotations

import subprocess
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from _core_check_assertions import assert_no_repo_identity

from tc_fitness.core_checks.new_code_coverage import (
    build,
    main,
    parse_added_lines,
    parse_line_coverage,
)

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


def _completed(args: list[str], rc: int, out: str) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=["git", *args], returncode=rc, stdout=out, stderr="")


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


# --------------------------------------------------------------------------- #
# Pure parser: per-line Cobertura coverage.
# --------------------------------------------------------------------------- #


def test_parse_line_coverage_joins_source_and_reads_hits(tmp_path: Path) -> None:
    p = _seed(tmp_path, "coverage.xml", _report({"a.py": {10: 1, 11: 0}, "b.py": {1: 3}}))
    assert parse_line_coverage(p) == {"src/a.py": {10: 1, 11: 0}, "src/b.py": {1: 3}}


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


def test_parse_added_lines_basic_hunk() -> None:
    diff = _diff("src/a.py", 10, ["x = 1", "y = 2", "z = 3"])
    assert parse_added_lines(diff) == {"src/a.py": {10, 11, 12}}


def test_parse_added_lines_new_file_whole_body_is_added() -> None:
    diff = _diff("src/new.py", 1, ["a = 1", "b = 2"], new_file=True)
    assert parse_added_lines(diff) == {"src/new.py": {1, 2}}


def test_parse_added_lines_deleted_file_contributes_nothing() -> None:
    diff = (
        "diff --git a/src/gone.py b/src/gone.py\n"
        "deleted file mode 100644\n"
        "index 1111111..0000000 100644\n"
        "--- a/src/gone.py\n"
        "+++ /dev/null\n"
        "@@ -1,2 +0,0 @@\n"
        "-was = 1\n"
        "-here = 2\n"
    )
    assert parse_added_lines(diff) == {}


def test_parse_added_lines_context_lines_advance_counter() -> None:
    # A -U1 hunk: context lines advance the new-side counter so the added line
    # lands on its true number (11), not the hunk start (10).
    diff = (
        "diff --git a/src/c.py b/src/c.py\n"
        "index aaa..bbb 100644\n"
        "--- a/src/c.py\n"
        "+++ b/src/c.py\n"
        "@@ -10,2 +10,3 @@ def f():\n"
        " keep = 0\n"
        "+added = 1\n"
        " tail = 2\n"
    )
    assert parse_added_lines(diff) == {"src/c.py": {11}}


def test_parse_added_lines_multiple_hunks_one_file() -> None:
    diff = (
        "diff --git a/src/m.py b/src/m.py\n"
        "index aaa..bbb 100644\n"
        "--- a/src/m.py\n"
        "+++ b/src/m.py\n"
        "@@ -0,0 +1,1 @@\n"
        "+first\n"
        "@@ -10,0 +12,2 @@\n"
        "+twelfth\n"
        "+thirteenth\n"
    )
    assert parse_added_lines(diff) == {"src/m.py": {1, 12, 13}}


# --------------------------------------------------------------------------- #
# Rule end-to-end via the injected git seam.
# --------------------------------------------------------------------------- #


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
