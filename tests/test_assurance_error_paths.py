"""Defensive guards in coverage and contract assurance that no other test triggers.

Each of these `raise` statements exists because the surrounding function refuses to
let a downstream check consume evidence it cannot fully trust. A guard nobody ever
triggers is a guard nobody can prove still works; these tests exist to keep proving it.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness import coverage_transaction
from tc_fitness.check_contract_execution import (
    _materialize_git_fixture,
    copy_verified_fixture,
    terminal_check_result,
)
from tc_fitness.check_contracts import CheckContractError, GitCaseEnvironment, GitFixtureEnvironment
from tc_fitness.check_evidence import CheckEvidence, CheckResult
from tc_fitness.core_checks.coverage_floor import parse_coverage_details
from tc_fitness.coverage_admission import complete_line_hits, exact_checkout
from tc_fitness.coverage_measurement import cross_check_branches

pytestmark = pytest.mark.contract

REPO_ROOT = Path(__file__).resolve().parents[1]


def seed(root: Path, path: str, text: str) -> Path:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    return target


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True, timeout=20)
    return result.stdout.strip()


def init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q")
    git(root, "config", "user.name", "three-cubes-agent[bot]")
    git(root, "config", "user.email", "295831460+three-cubes-agent[bot]@users.noreply.github.com")


def test_an_annotated_tag_object_cannot_stand_in_for_the_declared_base_commit(tmp_path: Path) -> None:
    """An exact-base identity must itself be a commit, not a peelable tag pointer."""
    init_repo(tmp_path)
    seed(tmp_path, "src/subject.py", "value = 1\n")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-qm", "base")
    git(tmp_path, "tag", "-am", "annotated base", "base-tag")
    base = git(tmp_path, "rev-parse", "base-tag")
    seed(tmp_path, "src/subject.py", "value = 2\n")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-qm", "candidate")
    candidate = git(tmp_path, "rev-parse", "HEAD")
    git(tmp_path, "checkout", "-q", "--detach", candidate)

    with pytest.raises(ValueError, match="coverage exact base is not a commit"):
        exact_checkout(tmp_path, base, candidate)


def test_a_report_that_omits_a_declared_source_file_is_rejected(tmp_path: Path) -> None:
    """A report measuring a different file set than the scope cannot admit the scope."""
    seed(tmp_path, "src/subject.py", "value = 1\n")
    report = seed(
        tmp_path,
        "coverage.xml",
        '<coverage lines-valid="1" lines-covered="1" branches-valid="0" branches-covered="0" '
        'line-rate="1.0" branch-rate="1.0"><sources><source>src</source></sources>'
        '<packages><package><classes><class filename="subject.py" line-rate="1.0" branch-rate="1.0">'
        '<lines><line number="1" hits="1"/></lines></class></classes></package></packages></coverage>',
    )

    with pytest.raises(ValueError, match="coverage report does not measure the complete source set"):
        complete_line_hits(tmp_path, report, {"src/other.py": tmp_path / "src/other.py"})


def test_a_report_whose_line_detail_disagrees_with_the_sources_true_statements_is_rejected(
    tmp_path: Path,
) -> None:
    """Detail must match Coverage.py's own statement inventory, not a hand-picked subset."""
    source = seed(tmp_path, "src/subject.py", "x = 1\ny = 2\n")
    report = seed(
        tmp_path,
        "coverage.xml",
        '<coverage lines-valid="1" lines-covered="1" branches-valid="0" branches-covered="0" '
        'line-rate="1.0" branch-rate="1.0"><sources><source>src</source></sources>'
        '<packages><package><classes><class filename="subject.py" line-rate="1.0" branch-rate="1.0">'
        '<lines><line number="1" hits="1"/></lines></class></classes></package></packages></coverage>',
    )

    with pytest.raises(ValueError, match=r"omits or invents executable source lines: src/subject\.py"):
        complete_line_hits(tmp_path, report, {"src/subject.py": source})


def test_a_corrupted_branch_condition_string_fails_the_independent_xml_cross_check(tmp_path: Path) -> None:
    """A branch line's own condition-coverage text is re-validated, not trusted blind."""
    seed(tmp_path, "src/subject.py", "def choose(value):\n    if value:\n        return 1\n    return 0\n")
    seed(
        tmp_path,
        "exercise.py",
        "from src.subject import choose\nassert choose(True) == 1\nassert choose(False) == 0\n",
    )
    seed(
        tmp_path,
        ".coveragerc",
        "[run]\nbranch = true\nsource = src\n[report]\nexclude_lines =\npartial_branches =\n",
    )
    for arguments in (("run", "exercise.py"), ("xml",), ("json",)):
        subprocess.run(
            [sys.executable, "-m", "coverage", *arguments],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            timeout=15,
        )
    report = tmp_path / "coverage.xml"
    files = {"src/subject.py": tmp_path / "src/subject.py"}
    hits = complete_line_hits(tmp_path, report, files)
    counts = parse_coverage_details(report, repo_root=tmp_path)
    corrupted = re.sub(
        r'condition-coverage="[0-9.]+% \([0-9]+/[0-9]+\)"',
        'condition-coverage="bogus"',
        report.read_text(),
        count=1,
    )
    assert corrupted != report.read_text()
    report.write_text(corrupted)

    with pytest.raises(ValueError, match="coverage XML branch counts are malformed"):
        cross_check_branches(tmp_path, report, files, hits, counts)


def test_an_unresolvable_uv_identity_probe_blocks_the_fresh_measurement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A broken uv toolchain must not silently produce an untrustworthy measurement."""
    snapshot = tmp_path / "snapshot"
    snapshot.mkdir()
    scratch = tmp_path / "scratch"
    scratch.mkdir()

    class _FailedIdentity:
        returncode = 1
        stdout = b""
        stderr = b"uv: command not found\n"

    monkeypatch.setattr(coverage_transaction.shutil, "which", lambda _name: "/usr/bin/uv")
    monkeypatch.setattr(coverage_transaction, "run_bounded_process", lambda *a, **k: _FailedIdentity())

    with pytest.raises(ValueError, match="trusted uv identity is unavailable"):
        coverage_transaction._fresh_measurement(snapshot, "0" * 40, scratch, "execution-id")


def test_a_fixture_copy_whose_digest_no_longer_matches_its_source_is_rejected(tmp_path: Path) -> None:
    """A snapshot bound to the wrong digest could feed the check a different candidate unnoticed."""
    fixture = tmp_path / "fixture"
    seed(fixture, "src/example.py", "value = 1\n")
    destination = tmp_path / "copy"

    with pytest.raises(CheckContractError, match="fixture changed while copying the execution snapshot"):
        copy_verified_fixture(fixture, destination, "sha256:" + "0" * 64)


def test_terminal_check_result_rejects_evidence_that_never_ran_a_check() -> None:
    """A ledger written without a terminal result would record an outcome nobody observed."""
    with pytest.raises(CheckContractError, match="missing or multiple terminal check results"):
        terminal_check_result(CheckEvidence())


def test_terminal_check_result_rejects_evidence_from_more_than_one_dispatched_check() -> None:
    """Two terminal results mean the contract's exit code binds to an ambiguous run, not one case."""
    evidence = CheckEvidence(
        results=[
            CheckResult(check="core:license_present", status="pass", exit_code=0),
            CheckResult(check="core:license_present", status="pass", exit_code=0),
        ]
    )

    with pytest.raises(CheckContractError, match="missing or multiple terminal check results"):
        terminal_check_result(evidence)


def test_a_git_history_path_the_filesystem_refuses_to_stat_is_reported_not_crashed_on(tmp_path: Path) -> None:
    """A history path beyond the filesystem's own name limit is a real OSError, not a design gap."""
    repo = tmp_path / "repo"
    (repo / ".contract").mkdir(parents=True)
    environment = GitCaseEnvironment(
        schema="tc.fitness/check-environment/v2",
        path="inherit",
        git=GitFixtureEnvironment(
            schema="tc.fitness/git-fixture/v1",
            history=".contract/" + "x" * 300,
            checkout="refs/heads/candidate",
        ),
    )

    with pytest.raises(CheckContractError, match="cannot read Git contract history"):
        _materialize_git_fixture(repo, environment)


def test_module_entrypoint_runs_coverage_admissions_own_main() -> None:
    """`python -m tc_fitness.coverage_admission` must expose the same public CLI as import."""
    result = subprocess.run(
        [sys.executable, "-m", "tc_fitness.coverage_admission", "--help"],
        capture_output=True,
        text=True,
        check=False,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr
    assert "produce" in result.stdout
