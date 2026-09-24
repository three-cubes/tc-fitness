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
from pathlib import Path

import pytest
from _core_check_assertions import assert_no_repo_identity

import tc_fitness.core_checks.new_code_coverage as new_code_coverage
from tc_fitness.core_checks.new_code_coverage import parse_line_coverage

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
# Design law: the CORE module carries zero repo identity in executable code.
# --------------------------------------------------------------------------- #


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.new_code_coverage as mod

    assert_no_repo_identity(mod.__file__)
