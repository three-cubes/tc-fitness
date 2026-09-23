"""Tests for the CORE check new_code_coverage.

Mirrors SonarCloud's "Coverage on New Code >= floor" merge condition locally:
for each changed file, the ADDED lines (right side of the diff vs the merge-base)
must clear a coverage floor. The git invocation is a DI seam, so these tests feed
canned ``merge-base`` / ``diff`` output — no real repository, no monkeypatching.
"""

from __future__ import annotations

import json
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


def test_xml_parser_falls_back_to_stdlib_without_site_packages(tmp_path: Path) -> None:
    report = _seed(tmp_path, "coverage.xml", _report({"fallback.py": {1: 1}}))
    source_root = Path(__file__).parents[1] / "src"
    script = (
        "import json, sys; from pathlib import Path; "
        "from tc_fitness.core_checks.new_code_coverage import parse_line_coverage; "
        "print(json.dumps(parse_line_coverage(Path(sys.argv[1]))))"
    )

    result = subprocess.run(
        [sys.executable, "-S", "-c", script, str(report)],
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": str(source_root)},
        capture_output=True,
        check=True,
        text=True,
    )

    assert json.loads(result.stdout) == {"src/fallback.py": {"1": 1}}


def test_parse_line_coverage_merges_duplicate_class_with_max_hits(tmp_path: Path) -> None:
    xml = (
        "<coverage><sources><source>src</source></sources><packages><package><classes>"
        '<class filename="a.py"><lines><line number="5" hits="0"/></lines></class>'
        '<class filename="a.py"><lines><line number="5" hits="4"/></lines></class>'
        "</classes></package></packages></coverage>"
    )
    p = _seed(tmp_path, "coverage.xml", xml)
    assert parse_line_coverage(p) == {"src/a.py": {5: 4}}  # covered anywhere ⇒ covered


def test_parse_line_coverage_handles_prefixed_and_malformed_class_records(tmp_path: Path) -> None:
    xml = (
        "<coverage><sources><source>src</source></sources><packages><package><classes>"
        '<class filename="src/already.py"><lines><line number="1" hits="2"/></lines></class>'
        '<class filename=""><lines><line number="2" hits="1"/></lines></class>'
        '<class filename="bad.py"><lines><line number="3"/><line hits="1"/>'
        '<line number="bad" hits="1"/><line number="4" hits="bad"/></lines></class>'
        "</classes></package></packages></coverage>"
    )
    report = _seed(tmp_path, "coverage.xml", xml)

    assert parse_line_coverage(report) == {"src/already.py": {1: 2}, "src/bad.py": {}}


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


def test_ignored_untracked_source_does_not_change_the_ci_equivalent_tree(tmp_path: Path) -> None:
    """Build residue excluded by Git remains outside local measurement."""
    repo = _git_repo(tmp_path)
    _seed(repo, ".gitignore", "src/generated.py\n")
    _seed(repo, "src/generated.py", "uncovered = 1\n")
    _seed(repo, "coverage.xml", _report({"generated.py": {1: 0}}))

    rule = build(_cfg(), repo_root=repo)

    assert rule.run() == 0


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


# --------------------------------------------------------------------------- #
# Hard floor: new code is non-grandfatherable.
# --------------------------------------------------------------------------- #


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


# --------------------------------------------------------------------------- #
# Design law: the CORE module carries zero repo identity in executable code.
# --------------------------------------------------------------------------- #


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.new_code_coverage as mod

    assert_no_repo_identity(mod.__file__)
