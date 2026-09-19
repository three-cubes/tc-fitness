"""Real Git, Coverage.py and public dispatch prove exact coverage admission."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness.catalogue import RuleEntry
from tc_fitness.check_evidence import CheckEvidence, capture_check_evidence
from tc_fitness.runner import run

pytestmark = pytest.mark.integration


def write(root: Path, name: str, text: str) -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def command(root: Path, *args: str) -> str:
    result = subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stderr + result.stdout
    return result.stdout.strip()


def commit(root: Path) -> str:
    command(root, "git", "add", ".")
    command(
        root,
        "git",
        "-c",
        "user.name=Contract",
        "-c",
        "user.email=contract@example.invalid",
        "commit",
        "-qm",
        "fixture",
    )
    return command(root, "git", "rev-parse", "HEAD")


def repository(root: Path, *, covered: bool = True, name: str = "subject.py") -> dict[str, object]:
    command(root, "git", "init", "-q")
    write(root, ".gitignore", ".coverage*\ncoverage.xml\nreceipt*\n__pycache__/\n")
    write(root, "src/" + name, "def choose(flag):\n    return 1\n")
    test = (
        "import runpy\nsubject = runpy.run_path("
        + repr("src/" + name)
        + ")\nassert subject['choose'](False) == 1\n"
    )
    write(root, "test_subject.py", test)
    write(root, "coverage-policy.toml", "line_floor = 95\nbranch_floor = 95\n")
    base = commit(root)
    write(root, "src/" + name, "def choose(flag):\n    if flag:\n        return 2\n    return 1\n")
    write(root, "test_subject.py", test + ("assert subject['choose'](True) == 2\n" if covered else ""))
    head = commit(root)
    write(
        root,
        ".coveragerc",
        "[run]\nbranch = true\nsource = src\n[report]\nexclude_lines =\npartial_branches =\n",
    )
    command(root, sys.executable, "-m", "coverage", "run", "test_subject.py")
    command(root, sys.executable, "-m", "coverage", "xml")
    return {"roots": ["src"], "floor_pct": 100, "exact_base_commit": base, "candidate_commit": head}


def dispatch(root: Path, config: dict[str, object], check: str = "new_code_coverage") -> CheckEvidence:
    with capture_check_evidence() as evidence:
        run(
            (RuleEntry(id=check, gate=check, check="core:" + check),),
            repo_root=root,
            core_check_configs={check: config},
        )
    assert len(evidence.results) == 1
    return evidence


def test_exact_base_scores_added_executable_lines_from_real_absolute_report(tmp_path: Path) -> None:
    config = repository(tmp_path, covered=False)
    evidence = dispatch(tmp_path, config)
    assert evidence.results[0].status == "fail"
    assert [(finding.rule, finding.path) for finding in evidence.findings] == [
        ("new-code-coverage", "src/subject.py")
    ]
    assert "3" in evidence.findings[0].message


@pytest.mark.parametrize("name", ["subject.py", "space name.py", "ümlaut.py"])
def test_exact_base_accepts_real_fully_covered_changes(tmp_path: Path, name: str) -> None:
    config = repository(tmp_path, name=name)
    assert dispatch(tmp_path, config).results[0].status == "pass"


@pytest.mark.parametrize(
    "change",
    [
        "wrong-base",
        "symbolic-base",
        "wrong-head",
        "dirty",
        "untracked",
        "missing-report",
        "missing-detail",
        "exemption",
        "low-floor",
        "empty-roots",
    ],
)
def test_exact_base_fails_closed_instead_of_soft_passing(tmp_path: Path, change: str) -> None:
    config = repository(tmp_path)
    if change == "wrong-base":
        config["exact_base_commit"] = "a" * 40
    elif change == "symbolic-base":
        config["exact_base_commit"] = "HEAD~1"
    elif change == "wrong-head":
        config["candidate_commit"] = config["exact_base_commit"]
    elif change == "dirty":
        write(tmp_path, "src/subject.py", "raise RuntimeError('unmeasured')\n")
    elif change == "untracked":
        write(tmp_path, "src/new.py", "raise RuntimeError('unmeasured')\n")
    elif change == "missing-report":
        (tmp_path / "coverage.xml").unlink()
    elif change == "missing-detail":
        report = tmp_path / "coverage.xml"
        report.write_text(report.read_text().replace('<line number="3" hits="1"/>', ""))
    elif change == "exemption":
        config["exempt_files"] = ["src/subject.py"]
    elif change == "low-floor":
        config["floor_pct"] = 99
    else:
        config["roots"] = []
    evidence = dispatch(tmp_path, config)
    assert evidence.results[0].status == "error"
    assert evidence.findings[0].rule == "check-execution-error"


def test_exact_base_missing_git_is_error(tmp_path: Path) -> None:
    config = repository(tmp_path)
    write(
        tmp_path,
        "invoke.py",
        "import json\nfrom tc_fitness.core_checks.new_code_coverage import build\nfrom pathlib import Path\nconfig=json.loads("
        + repr(json.dumps(config))
        + ")\nraise SystemExit(build(config, repo_root=Path.cwd()).run())\n",
    )
    result = subprocess.run(
        [sys.executable, "invoke.py"],
        cwd=tmp_path,
        env={**os.environ, "PATH": ""},
        capture_output=True,
        check=False,
        timeout=10,
    )
    assert result.returncode != 0


def produce(
    root: Path, base: str, candidate: str, output: Path, *, attempt: str = "attempt-1"
) -> dict[str, object]:
    command(
        root,
        sys.executable,
        "-m",
        "tc_fitness.coverage_admission",
        "produce",
        "--base-commit",
        base,
        "--candidate-commit",
        candidate,
        "--config",
        "coverage-policy.toml",
        "--source",
        "src",
        "--run-id",
        "run-1",
        "--attempt-id",
        attempt,
        "--output",
        str(output),
        "--",
        "test_subject.py",
    )
    receipt = output / "receipt.json"
    assert receipt.is_file(), "the public producer must retain a fresh, bound receipt"
    return json.loads(receipt.read_text())


def receipt_pair(root: Path, output: Path) -> tuple[dict[str, object], Path, Path]:
    config = repository(root)
    base, candidate = str(config["exact_base_commit"]), str(config["candidate_commit"])
    command(root, "git", "checkout", "-q", base)
    accepted_dir = output / "accepted"
    accepted = produce(root, base, base, accepted_dir)
    command(root, "git", "checkout", "-q", candidate)
    current_dir = output / "candidate"
    current = produce(root, base, candidate, current_dir)
    config.update(
        {
            "floor_pct": 95,
            "branch_floor_pct": 95,
            "critical_branch_files": ["src/subject.py"],
            "coverage_report": str(current_dir / "coverage.xml"),
            "coverage_receipt": str(current_dir / "receipt.json"),
            "coverage_receipt_digest": current["digest"],
            "accepted_coverage_receipt": str(accepted_dir / "receipt.json"),
            "accepted_coverage_digest": accepted["digest"],
            "coverage_config": "coverage-policy.toml",
            "run_id": "run-1",
            "attempt_id": "attempt-1",
            "max_age_seconds": 3600,
        }
    )
    return config, accepted_dir / "receipt.json", current_dir / "receipt.json"


def test_public_producer_and_admission_accept_current_exact_source(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    config, _, receipt = receipt_pair(root, tmp_path)
    evidence = dispatch(root, config, "coverage_floor")
    assert evidence.results[0].status == "pass"
    payload = json.loads(receipt.read_text())
    assert payload["counts"] == {"lines": 4, "covered_lines": 4, "branches": 2, "covered_branches": 2}
    assert payload["execution"]["attempt_id"] == "attempt-1"


def test_public_producer_measures_python_started_by_the_test_process(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    command(root, "git", "init", "-q")
    write(root, ".gitignore", "__pycache__/\n")
    write(root, "coverage-policy.toml", "line_floor = 95\nbranch_floor = 95\n")
    write(
        root,
        "src/subject.py",
        "def choose(flag):\n    if flag:\n        return 1\n    return 0\n",
    )
    write(
        root,
        "child.py",
        "import runpy\n"
        "subject = runpy.run_path('src/subject.py')\n"
        "assert subject['choose'](True) == 1\n"
        "assert subject['choose'](False) == 0\n",
    )
    write(
        root,
        "test_subject.py",
        "import subprocess, sys\nsubprocess.run([sys.executable, 'child.py'], check=True)\n",
    )
    candidate = commit(root)

    payload = produce(root, candidate, candidate, tmp_path / "subprocess-measurement")

    assert payload["counts"] == {
        "lines": 4,
        "covered_lines": 4,
        "branches": 2,
        "covered_branches": 2,
    }


def test_public_producer_aggregates_concurrent_python_process_measurements(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    command(root, "git", "init", "-q")
    write(root, ".gitignore", "__pycache__/\n")
    write(root, "coverage-policy.toml", "line_floor = 95\nbranch_floor = 95\n")
    write(
        root,
        "src/subject.py",
        "def choose(flag):\n    if flag:\n        return 1\n    return 0\n",
    )
    write(
        root,
        "child.py",
        "import runpy, sys\n"
        "subject = runpy.run_path('src/subject.py')\n"
        "expected = 1 if sys.argv[1] == 'true' else 0\n"
        "assert subject['choose'](sys.argv[1] == 'true') == expected\n",
    )
    write(
        root,
        "test_subject.py",
        "import subprocess, sys\n"
        "children = [subprocess.Popen([sys.executable, 'child.py', value]) "
        "for value in ('true', 'false')]\n"
        "assert [child.wait() for child in children] == [0, 0]\n",
    )
    candidate = commit(root)

    payload = produce(root, candidate, candidate, tmp_path / "parallel-subprocess-measurement")

    assert payload["counts"] == {
        "lines": 4,
        "covered_lines": 4,
        "branches": 2,
        "covered_branches": 2,
    }


@pytest.mark.parametrize(
    "change",
    [
        "altered-receipt",
        "altered-report",
        "altered-config",
        "stale-attempt",
        "stale-run",
        "wrong-base",
        "wrong-candidate",
        "missing-accepted",
        "wrong-accepted-digest",
        "wrong-current-digest",
        "missing-identity",
        "future",
        "expired",
        "invalid-schema",
        "missing-report-entry",
        "unknown-report-entry",
        "invalid-counts",
        "zero-lines",
        "wrong-scope",
        "wrong-config-path",
        "wrong-config-digest",
        "wrong-source-digest",
        "invalid-age",
        "wrong-report-binding",
        "wrong-measured-counts",
    ],
)
def test_receipt_admission_rejects_unbound_or_stale_evidence(tmp_path: Path, change: str) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    config, accepted, receipt = receipt_pair(root, tmp_path)
    if change == "altered-receipt":
        payload = json.loads(receipt.read_text())
        payload["counts"]["covered_lines"] = 0
        receipt.write_text(json.dumps(payload))
    elif change == "altered-report":
        report = Path(str(config["coverage_report"]))
        report.write_text(report.read_text() + "\n")
    elif change == "altered-config":
        write(root, "coverage-policy.toml", "line_floor = 0\n")
    elif change == "stale-attempt":
        config["attempt_id"] = "attempt-2"
    elif change == "stale-run":
        config["run_id"] = "run-2"
    elif change == "wrong-base":
        config["exact_base_commit"] = config["candidate_commit"]
    elif change == "wrong-candidate":
        config["candidate_commit"] = config["exact_base_commit"]
    elif change == "missing-accepted":
        accepted.unlink()
    elif change == "wrong-accepted-digest":
        config["accepted_coverage_digest"] = "sha256:" + "0" * 64
    elif change == "wrong-current-digest":
        config["coverage_receipt_digest"] = "sha256:" + "0" * 64
    elif change == "missing-identity":
        del config["attempt_id"]
    elif change == "invalid-age":
        config["max_age_seconds"] = True
    elif change == "wrong-report-binding":
        config["coverage_report"] = str(accepted.parent / "coverage.xml")
    elif change == "wrong-config-path":
        config["coverage_config"] = "/outside.toml"
    else:
        from datetime import UTC, datetime, timedelta

        payload = json.loads(receipt.read_text())
        if change in {"future", "expired"}:
            stamp = datetime.now(UTC) + timedelta(days=1 if change == "future" else -1)
            payload["execution"]["started_at"] = stamp.isoformat()
            payload["execution"]["finished_at"] = stamp.isoformat()
        elif change == "invalid-schema":
            payload["schema"] = "invalid"
        elif change == "missing-report-entry":
            del payload["reports"]["coverage.json"]
        elif change == "unknown-report-entry":
            payload["reports"]["other.json"] = "sha256:" + "0" * 64
        elif change == "invalid-counts":
            payload["counts"]["lines"] = "4"
        elif change == "zero-lines":
            payload["counts"]["lines"] = payload["counts"]["covered_lines"] = 0
        elif change == "wrong-scope":
            payload["roots"] = ["other"]
        elif change == "wrong-config-digest":
            payload["config_digest"] = "sha256:" + "0" * 64
        elif change == "wrong-source-digest":
            payload["source_digest"] = "sha256:" + "0" * 64
        elif change == "wrong-measured-counts":
            payload["counts"]["covered_lines"] -= 1
        config["coverage_receipt_digest"] = reseal(receipt, payload)
    evidence = dispatch(root, config, "coverage_floor")
    assert evidence.results[0].status == "error"
    assert evidence.findings[0].rule == "check-execution-error"


def test_ratchet_rejects_real_97_to_96_branch_regression_above_absolute_floor(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    command(root, "git", "init", "-q")
    write(root, ".gitignore", "__pycache__/\n")
    write(root, "coverage-policy.toml", "line_floor = 95\nbranch_floor = 95\n")
    write(
        root,
        "src/subject.py",
        "".join(f"def choice_{n}(flag):\n    if flag:\n        return 1\n    return 0\n" for n in range(100)),
    )
    test = "import runpy\nsubject = runpy.run_path('src/subject.py')\n"
    checks = [
        f"assert subject['choice_{n}'](True) == 1\nassert subject['choice_{n}'](False) == 0\n"
        for n in range(97)
    ]
    write(root, "test_subject.py", test + "".join(checks))
    base = commit(root)
    accepted = produce(root, base, base, tmp_path / "accepted")
    write(root, "test_subject.py", test + "".join(checks[:96]))
    candidate = commit(root)
    current = produce(root, base, candidate, tmp_path / "candidate")
    assert accepted["counts"]["covered_branches"] == 194
    assert current["counts"]["covered_branches"] == 192
    config = {
        "roots": ["src"],
        "floor_pct": 95,
        "branch_floor_pct": 95,
        "exact_base_commit": base,
        "candidate_commit": candidate,
        "coverage_report": str(tmp_path / "candidate/coverage.xml"),
        "coverage_receipt": str(tmp_path / "candidate/receipt.json"),
        "coverage_receipt_digest": current["digest"],
        "accepted_coverage_receipt": str(tmp_path / "accepted/receipt.json"),
        "accepted_coverage_digest": accepted["digest"],
        "coverage_config": "coverage-policy.toml",
        "run_id": "run-1",
        "attempt_id": "attempt-1",
        "max_age_seconds": 3600,
    }
    evidence = dispatch(root, config, "coverage_floor")
    assert evidence.results[0].status == "fail"
    assert any("branch coverage decreased" in finding.message for finding in evidence.findings)


def test_git_index_flags_cannot_hide_different_candidate_source(tmp_path: Path) -> None:
    config = repository(tmp_path)
    command(tmp_path, "git", "update-index", "--assume-unchanged", "src/subject.py")
    source = tmp_path / "src/subject.py"
    source.write_text(source.read_text().replace("return 2", "return 3"))
    assert dispatch(tmp_path, config).results[0].status == "error"


def test_exact_candidate_rejects_untracked_test_code(tmp_path: Path) -> None:
    config = repository(tmp_path)
    write(tmp_path, "test_uncommitted.py", "assert True\n")
    assert dispatch(tmp_path, config).results[0].status == "error"


@pytest.mark.parametrize("damage", ["parent-root", "empty-root", "symlink", "ignored-source"])
def test_exact_candidate_rejects_invalid_or_incomplete_source_scope(tmp_path: Path, damage: str) -> None:
    config = repository(tmp_path)
    if damage == "parent-root":
        config["roots"] = ["../src"]
    elif damage == "empty-root":
        write(tmp_path, "empty/.keep", "tracked\n")
        config["candidate_commit"] = commit(tmp_path)
        config["roots"] = ["empty"]
    elif damage == "symlink":
        (tmp_path / "src/link.py").symlink_to("subject.py")
        config["candidate_commit"] = commit(tmp_path)
    else:
        write(tmp_path, ".gitignore", "src/ignored.py\n")
        config["candidate_commit"] = commit(tmp_path)
        write(tmp_path, "src/ignored.py", "ignored = True\n")

    assert dispatch(tmp_path, config).results[0].status == "error"


@pytest.mark.parametrize(
    "damage",
    [
        "absolute-config",
        "changed-config",
        "empty-command",
        "missing-python",
        "failing-python",
        "unsafe-digest",
    ],
)
def test_public_producer_rejects_unbound_execution_inputs(tmp_path: Path, damage: str) -> None:
    from tc_fitness.coverage_admission import CoverageExecutionError, produce_coverage

    root = tmp_path / "repo"
    root.mkdir()
    config = repository(root)
    base = str(config["exact_base_commit"])
    candidate = str(config["candidate_commit"])
    config_name = "coverage-policy.toml"
    command_args = ["test_subject.py"]
    python_executable: Path | None = None
    digest_output: Path | None = None
    if damage == "absolute-config":
        config_name = str(root / config_name)
    elif damage == "changed-config":
        command(root, "git", "update-index", "--assume-unchanged", config_name)
        write(root, config_name, "line_floor = 0\n")
    elif damage == "empty-command":
        command_args = []
    elif damage == "missing-python":
        python_executable = tmp_path / "missing-python"
    elif damage == "failing-python":
        python_executable = Path("/usr/bin/false")
    else:
        digest_output = root / "digest.txt"

    expected = CoverageExecutionError if damage == "failing-python" else ValueError
    with pytest.raises(expected):
        produce_coverage(
            root=root,
            base=base,
            candidate=candidate,
            roots=["src"],
            config=config_name,
            run_id="run",
            attempt_id="attempt",
            output=tmp_path / ("measurement-" + damage),
            command=command_args,
            digest_output=digest_output,
            python_executable=python_executable,
        )


def test_public_producer_writes_independent_digest_handoff(tmp_path: Path) -> None:
    from tc_fitness.coverage_admission import produce_coverage

    root = tmp_path / "repo"
    root.mkdir()
    config = repository(root)
    candidate = str(config["candidate_commit"])
    handoff = tmp_path / "measurement.sha256"
    payload = produce_coverage(
        root=root,
        base=str(config["exact_base_commit"]),
        candidate=candidate,
        roots=["src"],
        config="coverage-policy.toml",
        run_id="run",
        attempt_id="attempt",
        output=tmp_path / "measurement",
        command=["test_subject.py"],
        digest_output=handoff,
    )

    assert handoff.read_text() == payload["digest"] + "\n"


def test_receipt_admission_accepts_external_digest_handoffs(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    config, accepted, current = receipt_pair(root, tmp_path)
    current_digest = tmp_path / "current.sha256"
    accepted_digest = tmp_path / "accepted.sha256"
    current_digest.write_text(json.loads(current.read_text())["digest"] + "\n")
    accepted_digest.write_text(json.loads(accepted.read_text())["digest"] + "\n")
    config["coverage_receipt_digest"] = "file:" + str(current_digest)
    config["accepted_coverage_digest"] = "file:" + str(accepted_digest)

    assert dispatch(root, config, "coverage_floor").results[0].status == "pass"


@pytest.mark.parametrize("handoff", ["relative", "inside", "symlink", "malformed"])
def test_receipt_admission_rejects_untrusted_digest_handoffs(tmp_path: Path, handoff: str) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    config, _, _ = receipt_pair(root, tmp_path)
    if handoff == "relative":
        value = "file:relative.sha256"
    elif handoff == "inside":
        path = write(root, "digest.sha256", str(config["coverage_receipt_digest"]))
        value = "file:" + str(path)
    elif handoff == "symlink":
        target = tmp_path / "digest.sha256"
        target.write_text(str(config["coverage_receipt_digest"]))
        path = tmp_path / "digest-link"
        path.symlink_to(target)
        value = "file:" + str(path)
    else:
        value = "not-a-digest"
    config["coverage_receipt_digest"] = value

    assert dispatch(root, config, "coverage_floor").results[0].status == "error"


def test_public_producer_detects_configuration_changed_by_test_execution(tmp_path: Path) -> None:
    from tc_fitness.coverage_admission import produce_coverage

    root = tmp_path / "repo"
    root.mkdir()
    config = repository(root)
    write(
        root,
        "change_config.py",
        "from pathlib import Path\n"
        "import subprocess\n"
        "path = Path('coverage-policy.toml')\n"
        "path.write_text('line_floor = 0\\n')\n"
        "subprocess.run(['git', 'update-index', '--assume-unchanged', str(path)], check=True)\n",
    )
    config["candidate_commit"] = commit(root)

    with pytest.raises(ValueError, match="configuration changed during execution"):
        produce_coverage(
            root=root,
            base=str(config["exact_base_commit"]),
            candidate=str(config["candidate_commit"]),
            roots=["src"],
            config="coverage-policy.toml",
            run_id="run",
            attempt_id="attempt",
            output=tmp_path / "measurement",
            command=["change_config.py"],
        )


def test_public_producer_main_returns_digest_for_completed_measurement(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from tc_fitness.coverage_admission import main

    root = tmp_path / "repo"
    root.mkdir()
    config = repository(root)
    output = tmp_path / "measurement"
    candidate = str(config["candidate_commit"])
    environment_name = "TC_FITNESS_TEST_COVERAGE_RUN_ID"
    previous = os.environ.get(environment_name)
    os.environ[environment_name] = "bound-run"
    try:
        result = main(
            [
                "produce",
                "--repo-root",
                str(root),
                "--base-commit",
                str(config["exact_base_commit"]),
                "--candidate-commit",
                candidate,
                "--source",
                "src",
                "--config",
                "coverage-policy.toml",
                "--run-id",
                "env:" + environment_name,
                "--attempt-id",
                "attempt",
                "--output",
                str(output),
                "--",
                "test_subject.py",
            ]
        )
    finally:
        if previous is None:
            del os.environ[environment_name]
        else:
            os.environ[environment_name] = previous

    assert result == 0
    receipt = json.loads((output / "receipt.json").read_text())
    assert receipt["execution"]["run_id"] == "bound-run"
    assert capsys.readouterr().out.strip() == receipt["digest"]


@pytest.mark.parametrize("check", ["coverage_floor", "new_code_coverage"])
def test_contract_policy_admits_reviewed_coverage_evidence_inputs(tmp_path: Path, check: str) -> None:
    from tc_fitness.check_contract_policy import validate_contract_configuration

    root = tmp_path / "repo"
    root.mkdir()
    config, _, _ = receipt_pair(root, tmp_path)
    if check == "new_code_coverage":
        config.pop("branch_floor_pct")
        config.pop("critical_branch_files")
        config["floor_pct"] = 100
    validate_contract_configuration("core:" + check, config)


def test_changed_line_admission_also_rejects_stale_receipts(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    config, _, _ = receipt_pair(root, tmp_path)
    config["floor_pct"] = 100
    assert dispatch(root, config).results[0].status == "pass"
    config["attempt_id"] = "another-attempt"
    assert dispatch(root, config).results[0].status == "error"


@pytest.mark.parametrize("check", ["coverage_floor", "new_code_coverage"])
def test_receipt_configuration_cannot_fall_back_to_legacy_admission(tmp_path: Path, check: str) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    config, _, _ = receipt_pair(root, tmp_path)
    if check == "coverage_floor":
        config["branch_floor_pct"] = None
        config["critical_branch_files"] = []
    else:
        config.pop("exact_base_commit")
        config.pop("candidate_commit")
    assert dispatch(root, config, check).results[0].status == "error"


def reseal(path: Path, payload: dict[str, object]) -> str:
    payload.pop("digest", None)
    token = (
        "sha256:"
        + hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        ).hexdigest()
    )
    payload["digest"] = token
    path.write_text(json.dumps(payload))
    return token


@pytest.mark.parametrize("alter_json", [False, True])
def test_new_candidate_branch_cannot_disappear_from_xml_metadata(tmp_path: Path, alter_json: bool) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    config, accepted, current = receipt_pair(root, tmp_path)
    assert json.loads(accepted.read_text())["counts"]["branches"] == 0
    report = current.parent / "coverage.xml"
    text = re.sub(r'branch-rate="[^"]+"', 'branch-rate="1"', report.read_text())
    text = re.sub(r'branches-(valid|covered)="[0-9]+"', r'branches-\1="0"', text)
    report.write_text(re.sub(r' (?:branch|condition-coverage|missing-branches)="[^"]*"', "", text))
    payload = json.loads(current.read_text())
    for counts in [payload["counts"], *payload["files"].values()]:
        counts["branches"] = counts["covered_branches"] = 0
    payload["reports"]["coverage.xml"] = "sha256:" + hashlib.sha256(report.read_bytes()).hexdigest()
    if alter_json:
        json_report = current.parent / "coverage.json"
        content = json.loads(json_report.read_text())
        for detail in content["files"].values():
            detail["executed_branches"] = detail["missing_branches"] = []
        for summary in [content["totals"], *(detail["summary"] for detail in content["files"].values())]:
            for name in ("num_branches", "covered_branches", "missing_branches", "num_partial_branches"):
                summary[name] = 0
        json_report.write_text(json.dumps(content))
        payload["reports"]["coverage.json"] = "sha256:" + hashlib.sha256(json_report.read_bytes()).hexdigest()
    config["coverage_receipt_digest"] = reseal(current, payload)
    evidence = dispatch(root, config, "coverage_floor")
    assert evidence.results[0].status == "error"
    assert evidence.findings[0].rule == "check-execution-error"


@pytest.mark.parametrize(
    "damage",
    [
        "line-type",
        "duplicate-line",
        "arc-shape",
        "duplicate-arc",
        "branch-disabled",
        "missing-document",
        "excluded-line",
        "execution-disagreement",
        "summary-disagreement",
        "malformed-xml-branch",
    ],
)
def test_admission_rejects_internally_inconsistent_native_coverage_detail(
    tmp_path: Path, damage: str
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    config, _, current = receipt_pair(root, tmp_path)
    receipt = json.loads(current.read_text())
    json_report = current.parent / "coverage.json"
    document = json.loads(json_report.read_text())
    detail = next(iter(document["files"].values()))

    if damage == "line-type":
        detail["executed_lines"] = "1,2,3,4"
    elif damage == "duplicate-line":
        detail["executed_lines"].append(detail["executed_lines"][0])
    elif damage == "arc-shape":
        detail["executed_branches"] = [[2]]
    elif damage == "duplicate-arc":
        detail["executed_branches"].append(detail["executed_branches"][0])
    elif damage == "branch-disabled":
        document["meta"]["branch_coverage"] = False
    elif damage == "missing-document":
        document["files"] = {}
    elif damage == "excluded-line":
        detail["excluded_lines"] = [1]
    elif damage == "execution-disagreement":
        removed = detail["executed_lines"].pop()
        detail["missing_lines"].append(removed)
    elif damage == "summary-disagreement":
        detail["summary"]["covered_lines"] -= 1
    else:
        xml_report = current.parent / "coverage.xml"
        original = xml_report.read_text()
        altered = re.sub(r'condition-coverage="[^"]+"', 'condition-coverage="invalid"', original, count=1)
        assert altered != original
        xml_report.write_text(altered)
        receipt["reports"]["coverage.xml"] = "sha256:" + hashlib.sha256(xml_report.read_bytes()).hexdigest()

    if damage != "malformed-xml-branch":
        json_report.write_text(json.dumps(document))
        receipt["reports"]["coverage.json"] = "sha256:" + hashlib.sha256(json_report.read_bytes()).hexdigest()
    config["coverage_receipt_digest"] = reseal(current, receipt)

    evidence = dispatch(root, config, "coverage_floor")

    assert evidence.results[0].status == "error"
    assert evidence.findings[0].rule == "check-execution-error"
