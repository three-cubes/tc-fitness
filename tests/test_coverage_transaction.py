"""Fresh exact-Git coverage transactions through the installed public command."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from tc_fitness.coverage_transaction import _fresh_measurement

pytestmark = pytest.mark.integration


def test_measurement_rejects_an_untrusted_uv_identity(tmp_path: Path) -> None:
    snapshot = tmp_path / "snapshot"
    scratch = tmp_path / "evidence"
    tools = tmp_path / "tools"
    snapshot.mkdir()
    scratch.mkdir()
    tools.mkdir()
    uv = tools / "uv"
    uv.write_text("#!/bin/sh\nexit 17\n")
    uv.chmod(0o755)
    original = os.environ.get("PATH")
    os.environ["PATH"] = str(tools)
    try:
        with pytest.raises(ValueError, match="trusted uv identity is unavailable"):
            _fresh_measurement(snapshot, "0" * 40, scratch, "test")
    finally:
        if original is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = original


@pytest.mark.parametrize("binding", ["valid", "malformed", "unregistered"])
def test_fixed_profile_distinguishes_contract_fixtures_from_outer_tests(tmp_path: Path, binding: str) -> None:
    root = tmp_path / "repo"
    base, _ = repository(root)
    name = "every_test_has_tier_marker"
    fixture = root / "tests/check_contracts" / (name if binding != "unregistered" else "unregistered")
    shutil.copytree(Path(__file__).parent / "check_contracts" / name, fixture)
    if binding == "malformed":
        (fixture / "contract.yaml").write_text("not-a-contract: true\n")
    candidate = commit(root)
    code, payload = invoke(root, base, candidate, tmp_path / "result.json")
    assert code == (0 if binding == "valid" else 2), payload
    assert payload["status"] == ("pass" if binding == "valid" else "error")


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=20, check=True)
    return result.stdout.strip()


def _distributions(toolchain: dict[str, object]) -> dict[str, str]:
    """The receipt records the environment as ordered name/version pairs."""
    return {name: version for name, version in toolchain["distributions"]}


def commit(root: Path) -> str:
    git(root, "add", ".")
    git(
        root,
        "-c",
        "user.name=Contract",
        "-c",
        "user.email=contract@example.invalid",
        "commit",
        "-qm",
        "fixture",
    )
    return git(root, "rev-parse", "HEAD")


def repository(root: Path, *, covered: bool = True) -> tuple[str, str]:
    root.mkdir()
    git(root, "init", "-q")
    (root / ".gitignore").write_text("__pycache__/\n.pytest_cache/\n")
    (root / "src/tc_fitness").mkdir(parents=True)
    (root / "tests").mkdir()
    # Candidate-owned configuration tries to hide all tests and change scope.
    # The trusted self-assurance profile must ignore those selectors.
    (root / "pyproject.toml").write_text(
        "[project]\nname='coverage-transaction-fixture'\nversion='0.0.0'\n"
        "requires-python='>=3.12,<3.13'\n"
        "[project.optional-dependencies]\nassurance=['coverage==7.14.2','pytest==9.1.0']\n"
        "[tool.pytest.ini_options]\ntestpaths=['missing']\naddopts='--ignore=tests'\n"
        "[tool.tc_fitness.core_checks.coverage_floor]\nroots=['missing']\nfloor_pct=0\n"
        "accepted_coverage_receipt='forged.json'\naccepted_coverage_digest='reset'\n"
    )
    subprocess.run(
        ["uv", "lock", "--python", sys.executable], cwd=root, capture_output=True, check=True, timeout=30
    )
    names = ("subject", "gate", "runner", "gate_config", "runtime_contract")
    test = (
        "import runpy\nimport pytest\npytestmark=pytest.mark.integration\n"
        "@pytest.mark.parametrize('name', " + repr(names) + ")\n"
        "def test_choices(name):\n"
        "    choose=runpy.run_path(f'src/tc_fitness/{name}.py')['choose']\n"
        "    assert choose(False)==1\n"
    )
    for name in names:
        (root / f"src/tc_fitness/{name}.py").write_text("def choose(flag):\n    return 1\n")
    (root / "tests/test_subject.py").write_text(test)
    base = commit(root)
    for name in names:
        (root / f"src/tc_fitness/{name}.py").write_text(
            "def choose(flag):\n    if flag:\n        return 2\n    return 1\n"
        )
    (root / "tests/test_subject.py").write_text(test + ("    assert choose(True)==2\n" if covered else ""))
    return base, commit(root)


def invoke(
    root: Path,
    base: str,
    candidate: str,
    output: Path,
    *extra: str,
    environment: dict[str, str] | None = None,
) -> tuple[int, dict[str, object]]:
    result = subprocess.run(
        [
            str(Path(sys.executable).with_name("tc-fitness")),
            "assure-coverage",
            "--repo-root",
            str(root),
            "--base-commit",
            base,
            "--candidate-commit",
            candidate,
            "--output",
            str(output),
            "--evidence-dir",
            str(output.with_suffix(".evidence")),
            *extra,
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
        env=environment,
    )
    return result.returncode, json.loads(output.read_text()) if output.exists() else {"stderr": result.stderr}


def test_public_transaction_freshly_measures_both_commits_with_fixed_profile(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    base, candidate = repository(root)
    before = git(root, "worktree", "list", "--porcelain")
    retained = tmp_path / "result.evidence"
    retained.mkdir()
    code, result = invoke(root, base, candidate, tmp_path / "result.json")
    assert code == 0, result
    assert result["status"] == "pass"
    for label in ("base", "candidate"):
        assert (retained / label / "uv.stderr.log").is_file()
        for report in ("coverage.xml", "coverage.json", "receipt.json", "run.stdout.log", "run.stderr.log"):
            assert (retained / label / "measurement" / report).is_file()
        toolchain = result[label]["toolchain"]
        assert toolchain["coverage"] == "7.14.2"
        assert _distributions(toolchain)["pytest"] == "9.1.0"
        assert toolchain["python_executable"] != sys.executable
        assert toolchain["uv"].startswith("uv ")
        assert (
            toolchain["lock_digest"]
            == "sha256:" + hashlib.sha256((root / "uv.lock").read_bytes()).hexdigest()
        )
    assert (
        result["base"]["toolchain"]["python_executable"]
        != result["candidate"]["toolchain"]["python_executable"]
    )
    assert result["base"]["commit"] == base
    assert result["candidate"]["commit"] == candidate
    assert result["base"]["counts"] == {
        "lines": 10,
        "covered_lines": 10,
        "branches": 0,
        "covered_branches": 0,
    }
    assert result["candidate"]["counts"] == {
        "lines": 20,
        "covered_lines": 20,
        "branches": 10,
        "covered_branches": 10,
    }
    assert result["base"]["source_digest"] != result["candidate"]["source_digest"]
    assert json.loads((retained / "transaction.json").read_text()) == result
    assert git(root, "status", "--porcelain") == ""
    assert git(root, "worktree", "list", "--porcelain") == before


def test_public_transaction_starts_exact_base_and_candidate_measurements_together(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    base, _ = repository(root)
    barrier = tmp_path / "measurement-started"
    barrier.mkdir()

    git(root, "checkout", "--detach", base)
    test = root / "tests/test_subject.py"
    test.write_text(
        test.read_text()
        + "\nimport os, time\nfrom pathlib import Path\n"
        + "def test_both_exact_sides_are_running():\n"
        + "    shared = Path(os.environ['TC_FITNESS_TEST_OVERLAP_DIR'])\n"
        + "    side = Path.cwd().name\n"
        + "    assert side in {'base', 'candidate'}\n"
        + "    (shared / (side + '.started')).touch()\n"
        + "    deadline = time.monotonic() + 8\n"
        + "    while time.monotonic() < deadline:\n"
        + "        if all((shared / (name + '.started')).exists() for name in ('base', 'candidate')):\n"
        + "            return\n"
        + "        time.sleep(0.01)\n"
        + "    raise AssertionError('the other exact-commit measurement did not overlap this test')\n"
    )
    base = commit(root)
    for name in ("subject", "gate", "runner", "gate_config", "runtime_contract"):
        (root / f"src/tc_fitness/{name}.py").write_text(
            "def choose(flag):\n    if flag:\n        return 2\n    return 1\n"
        )
    test.write_text(
        test.read_text().replace(
            "    assert choose(False)==1\n", "    assert choose(False)==1\n    assert choose(True)==2\n"
        )
    )
    candidate = commit(root)
    evidence = tmp_path / "overlap.evidence"
    environment = {**os.environ, "TC_FITNESS_TEST_OVERLAP_DIR": str(barrier)}

    code, result = invoke(root, base, candidate, tmp_path / "overlap.json", environment=environment)

    assert code == 0, result
    assert result["status"] == "pass"
    assert (barrier / "base.started").is_file()
    assert (barrier / "candidate.started").is_file()
    assert result["base"]["commit"] == base
    assert result["candidate"]["commit"] == candidate
    assert json.loads((evidence / "transaction.json").read_text()) == result


def test_public_transaction_rejects_uncovered_changed_and_critical_branches(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    base, candidate = repository(root, covered=False)
    code, result = invoke(root, base, candidate, tmp_path / "result.json")
    assert code == 1, result
    assert result["status"] == "fail"
    assert any("uncovered changed executable" in item for item in result["failures"])
    assert any("critical branch" in item for item in result["failures"])


@pytest.mark.parametrize(
    "identity", ["moving-base", "wrong-candidate", "unknown-base", "non-ancestor", "dirty"]
)
def test_public_transaction_rejects_unbound_identity(tmp_path: Path, identity: str) -> None:
    root = tmp_path / "repo"
    base, candidate = repository(root)
    if identity == "moving-base":
        base = "HEAD~1"
    elif identity == "wrong-candidate":
        candidate = base
    elif identity == "non-ancestor":
        git(root, "checkout", "--orphan", "unrelated")
        base = commit(root)
        git(root, "checkout", "--detach", candidate)
    elif identity == "dirty":
        (root / "pyproject.toml").write_text("changed=true\n")
    else:
        base = "a" * 40
    code, result = invoke(root, base, candidate, tmp_path / "result.json")
    assert code == 2, result
    assert result["status"] == "error"


def test_public_transaction_preserves_existing_output_and_reports_structured_error(tmp_path: Path) -> None:
    output = tmp_path / "existing.json"
    output.write_text("retained evidence\n")
    result = subprocess.run(
        [
            str(Path(sys.executable).with_name("tc-fitness")),
            "assure-coverage",
            "--repo-root",
            str(tmp_path),
            "--base-commit",
            "a" * 40,
            "--candidate-commit",
            "b" * 40,
            "--output",
            str(output),
            "--evidence-dir",
            str(tmp_path / "evidence"),
        ],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 2
    assert json.loads(result.stdout)["status"] == "error"
    assert output.read_text() == "retained evidence\n"


@pytest.mark.parametrize("location", ["inside", "nonempty", "symlink", "file"])
def test_public_transaction_rejects_unsafe_or_reused_evidence_directory(
    tmp_path: Path, location: str
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    retained = tmp_path / "evidence"
    if location == "inside":
        retained = root / "evidence"
    elif location == "file":
        retained.write_text("existing evidence")
    else:
        retained.mkdir()
        (retained / "existing").write_text("existing evidence")
        if location == "symlink":
            link = tmp_path / "linked"
            link.symlink_to(retained, target_is_directory=True)
            retained = link
    code, result = invoke(root, "a" * 40, "b" * 40, tmp_path / "result.json", "--evidence-dir", str(retained))
    assert code == 2
    assert result["status"] == "error"
    assert "evidence directory" in result["error"]
    if location == "file":
        assert retained.read_text() == "existing evidence"
    elif location != "inside":
        assert (retained / "existing").read_text() == "existing evidence"


def test_transaction_ratchets_against_fresh_base_above_absolute_floor(tmp_path: Path) -> None:
    from tc_fitness.coverage_transaction import assure_coverage

    root = tmp_path / "repo"
    repository(root)
    source = root / "src/tc_fitness/subject.py"
    source.write_text(
        "".join(f"def choice_{n}(flag):\n    if flag:\n        return 1\n    return 0\n" for n in range(100))
    )
    test = root / "tests/test_subject.py"
    existing = test.read_text().replace(
        "('subject', 'gate', 'runner', 'gate_config', 'runtime_contract')",
        "('gate', 'runner', 'gate_config', 'runtime_contract')",
    )
    prefix = existing + "\ndef test_subject():\n    subject=runpy.run_path('src/tc_fitness/subject.py')\n"
    checks = [
        f"    assert subject['choice_{n}'](True)==1\n    assert subject['choice_{n}'](False)==0\n"
        for n in range(97)
    ]
    test.write_text(prefix + "".join(checks))
    base = commit(root)
    test.write_text(prefix + "".join(checks[:96]))
    candidate = commit(root)
    result = assure_coverage(root, base=base, candidate=candidate, evidence_dir=tmp_path / "evidence")
    assert "line coverage decreased from fresh exact base" in result.failures
    assert "branch coverage decreased from fresh exact base" in result.failures
    assert not any("below" in item for item in result.failures)


def test_failed_base_is_not_replaced_by_a_passing_candidate_measurement(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    repository(root)
    test = root / "tests/test_subject.py"
    passing = test.read_text()
    test.write_text(passing + "\ndef test_failure():\n    assert False\n")
    base = commit(root)
    test.write_text(passing)
    candidate = commit(root)
    before = git(root, "worktree", "list", "--porcelain")
    code, result = invoke(root, base, candidate, tmp_path / "result.json")
    assert code == 2, result
    assert result["status"] == "error"
    assert result["side"] == "base"
    assert result["phase"] == "run"
    retained = tmp_path / "result.evidence"
    assert "test_failure" in (retained / result["stdout_log"]).read_text()
    assert (retained / result["stderr_log"]).is_file()
    # The independent candidate still completes, and its fresh reports remain
    # available even though the transaction reports the deterministic base error.
    assert (retained / "candidate/measurement/receipt.json").is_file()
    assert (retained / "candidate/measurement/coverage.xml").is_file()
    assert json.loads((retained / "transaction.json").read_text()) == result
    assert git(root, "worktree", "list", "--porcelain") == before


@pytest.mark.parametrize(
    ("failing_sides", "expected_error_side"),
    [("candidate", "candidate"), ("base,candidate", "base")],
)
def test_parallel_measurement_retains_side_failures_and_selects_base_first(
    tmp_path: Path, failing_sides: str, expected_error_side: str
) -> None:
    root = tmp_path / "repo"
    base, _ = repository(root)
    git(root, "checkout", "--detach", base)
    test = root / "tests/test_subject.py"
    test.write_text(
        test.read_text()
        + "\nimport os\nfrom pathlib import Path\n"
        + "def test_selected_measurement_failure():\n"
        + "    failing = os.environ['TC_FITNESS_TEST_FAIL_SIDES'].split(',')\n"
        + "    if Path.cwd().name in failing:\n"
        + "        raise AssertionError('failure requested for ' + Path.cwd().name)\n"
    )
    base = commit(root)
    for name in ("subject", "gate", "runner", "gate_config", "runtime_contract"):
        (root / f"src/tc_fitness/{name}.py").write_text(
            "def choose(flag):\n    if flag:\n        return 2\n    return 1\n"
        )
    test.write_text(
        test.read_text().replace(
            "    assert choose(False)==1\n", "    assert choose(False)==1\n    assert choose(True)==2\n"
        )
    )
    candidate = commit(root)
    result_path = tmp_path / "result.json"
    environment = {**os.environ, "TC_FITNESS_TEST_FAIL_SIDES": failing_sides}

    code, result = invoke(root, base, candidate, result_path, environment=environment)

    retained = result_path.with_suffix(".evidence")
    assert code == 2, result
    assert result["status"] == "error"
    assert result["side"] == expected_error_side
    assert result["phase"] == "run"
    assert "failure requested" in (retained / result["stdout_log"]).read_text()
    failed = set(failing_sides.split(","))
    for side in ("base", "candidate"):
        run_log = retained / side / "measurement/run.stdout.log"
        assert run_log.is_file()
        if side in failed:
            assert "failure requested" in run_log.read_text()
            assert not (retained / side / "measurement/receipt.json").exists()
        else:
            assert (retained / side / "measurement/receipt.json").is_file()
    assert json.loads((retained / "transaction.json").read_text()) == result
    assert git(root, "worktree", "list", "--porcelain").count("worktree ") == 1


def test_interrupted_parallel_measurement_waits_for_children_and_cleans_worktrees(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    base, _ = repository(root)
    git(root, "checkout", "--detach", base)
    marker_dir = tmp_path / "interruption-markers"
    marker_dir.mkdir()
    test = root / "tests/test_subject.py"
    test.write_text(
        test.read_text()
        + "\nimport os, time\nfrom pathlib import Path\n"
        + "def test_running_marker_is_external_and_isolated():\n"
        + "    markers = Path(os.environ['TC_FITNESS_TEST_INTERRUPT_DIR'])\n"
        + "    side = Path.cwd().name\n"
        + "    (markers / (side + '.started')).touch()\n"
        + "    time.sleep(2)\n"
        + "    (markers / (side + '.finished')).touch()\n"
    )
    base = commit(root)
    for name in ("subject", "gate", "runner", "gate_config", "runtime_contract"):
        (root / f"src/tc_fitness/{name}.py").write_text(
            "def choose(flag):\n    if flag:\n        return 2\n    return 1\n"
        )
    test.write_text(
        test.read_text().replace(
            "    assert choose(False)==1\n", "    assert choose(False)==1\n    assert choose(True)==2\n"
        )
    )
    candidate = commit(root)
    before = git(root, "worktree", "list", "--porcelain")
    evidence = tmp_path / "interrupted.evidence"
    environment = {**os.environ, "TC_FITNESS_TEST_INTERRUPT_DIR": str(marker_dir)}
    process = subprocess.Popen(
        [
            str(Path(sys.executable).with_name("tc-fitness")),
            "assure-coverage",
            "--repo-root",
            str(root),
            "--base-commit",
            base,
            "--candidate-commit",
            candidate,
            "--evidence-dir",
            str(evidence),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=environment,
    )
    try:
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            if all((marker_dir / f"{side}.started").exists() for side in ("base", "candidate")):
                break
            if process.poll() is not None:
                pytest.fail("coverage transaction exited before both measurements started")
            time.sleep(0.02)
        else:
            pytest.fail("both exact worktree measurements did not start")
        process.send_signal(signal.SIGINT)
        stdout, stderr = process.communicate(timeout=20)
    finally:
        if process.poll() is None:
            process.kill()
            process.communicate(timeout=5)

    assert process.returncode != 0, (stdout, stderr)
    assert all((marker_dir / f"{side}.finished").is_file() for side in ("base", "candidate"))
    assert git(root, "worktree", "list", "--porcelain") == before


def test_transaction_measurements_are_immutable_and_never_reused(tmp_path: Path) -> None:
    from dataclasses import FrozenInstanceError

    from tc_fitness.coverage_transaction import assure_coverage

    root = tmp_path / "repo"
    base, candidate = repository(root)
    first = assure_coverage(root, base=base, candidate=candidate, evidence_dir=tmp_path / "first")
    with pytest.raises(FrozenInstanceError):
        first.base.counts.covered_lines = 0
    exported = first.as_payload()
    exported["base"]["counts"]["covered_lines"] = 0
    assert first.base.counts.covered_lines == 10
    second = assure_coverage(root, base=base, candidate=candidate, evidence_dir=tmp_path / "second")
    assert second.execution_id != first.execution_id
    assert second.failures == first.failures == ()


def test_candidate_pytest_plugin_cannot_take_over_the_fixed_measurement_profile(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    base, _ = repository(root)
    (root / "src/tc_fitness/__init__.py").write_text("")
    (root / "src/tc_fitness/pytest_tiers.py").write_text(
        "def pytest_addoption(parser):\n    raise RuntimeError('candidate plugin was loaded')\n"
    )
    test = root / "tests/test_subject.py"
    test.write_text(
        test.read_text() + "\ndef test_plugin_behavior():\n"
        "    hook=runpy.run_path('src/tc_fitness/pytest_tiers.py')['pytest_addoption']\n"
        "    with pytest.raises(RuntimeError):\n        hook(None)\n"
    )
    candidate = commit(root)
    code, result = invoke(root, base, candidate, tmp_path / "result.json")
    assert code == 0, result
    assert result["candidate"]["counts"]["covered_lines"] == 22


def test_stale_candidate_lock_is_terminal_error_not_controller_environment_fallback(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    base, _ = repository(root)
    config = root / "pyproject.toml"
    config.write_text(config.read_text().replace("pytest==9.1.0", "pytest==9.0.2"))
    candidate = commit(root)
    code, result = invoke(root, base, candidate, tmp_path / "result.json")
    assert code == 2, result
    assert result["status"] == "error"
    assert result["side"] == "candidate"
    assert result["phase"] == "provision"
    retained = tmp_path / "result.evidence"
    assert (retained / result["stderr_log"]).read_text()
    assert json.loads((retained / "transaction.json").read_text()) == result


def test_missing_uv_retains_real_provisioning_diagnostics(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    base, candidate = repository(root)
    binaries = tmp_path / "bin"
    binaries.mkdir()
    (binaries / "git").symlink_to(shutil.which("git"))
    code, result = invoke(
        root, base, candidate, tmp_path / "result.json", environment={**os.environ, "PATH": str(binaries)}
    )
    assert code == 2
    assert result["side"] == "base"
    assert result["phase"] == "provision"
    assert "uv" in (tmp_path / "result.evidence" / result["stderr_log"]).read_text()


def test_each_commit_uses_its_own_locked_pytest_version(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    base, _ = repository(root)
    config = root / "pyproject.toml"
    config.write_text(config.read_text().replace("pytest==9.1.0", "pytest==9.0.2"))
    subprocess.run(
        ["uv", "lock", "--python", sys.executable], cwd=root, capture_output=True, check=True, timeout=30
    )
    test = root / "tests/test_subject.py"
    test.write_text(
        test.read_text() + "\ndef test_locked_pytest():\n    assert pytest.__version__=='9.0.2'\n"
    )
    candidate = commit(root)
    code, result = invoke(root, base, candidate, tmp_path / "result.json")
    assert code == 0, result
    assert _distributions(result["base"]["toolchain"])["pytest"] == "9.1.0"
    assert _distributions(result["candidate"]["toolchain"])["pytest"] == "9.0.2"
    assert result["base"]["toolchain"]["lock_digest"] != result["candidate"]["toolchain"]["lock_digest"]


def test_in_process_transaction_retains_terminal_error_for_invalid_identity(tmp_path: Path) -> None:
    from tc_fitness.coverage_transaction import assure_coverage

    root = tmp_path / "repo"
    _, candidate = repository(root)
    evidence = tmp_path / "evidence"

    with pytest.raises(ValueError, match="explicit full immutable commit IDs"):
        assure_coverage(root, base="HEAD~1", candidate=candidate, evidence_dir=evidence)

    payload = json.loads((evidence / "transaction.json").read_text())
    assert payload["status"] == "error"
    assert payload["phase"] == "transaction"
    assert payload["side"] is None


@pytest.mark.parametrize("output_location", ["external", "inside-evidence", "missing-parent"])
def test_transaction_main_reports_errors_without_overwriting_unsafe_output(
    tmp_path: Path, output_location: str, capsys: pytest.CaptureFixture[str]
) -> None:
    from tc_fitness.coverage_transaction import main

    root = tmp_path / "repo"
    root.mkdir()
    evidence = tmp_path / "evidence"
    if output_location == "external":
        output = tmp_path / "result.json"
    elif output_location == "inside-evidence":
        output = evidence / "result.json"
    else:
        output = tmp_path / "missing" / "result.json"

    code = main(
        [
            "--repo-root",
            str(root),
            "--base-commit",
            "a" * 40,
            "--candidate-commit",
            "b" * 40,
            "--evidence-dir",
            str(evidence),
            "--output",
            str(output),
        ]
    )

    assert code == 2
    if output_location == "external":
        assert json.loads(output.read_text())["status"] == "error"
        assert capsys.readouterr().out == ""
    else:
        assert not output.exists()
        assert json.loads(capsys.readouterr().out)["status"] == "error"


def test_in_process_transaction_retains_locked_provision_failure(tmp_path: Path) -> None:
    from tc_fitness.coverage_transaction import TransactionError, assure_coverage

    root = tmp_path / "repo"
    base, _ = repository(root)
    config = root / "pyproject.toml"
    config.write_text(config.read_text().replace("pytest==9.1.0", "pytest==9.0.2"))
    candidate = commit(root)

    with pytest.raises(TransactionError) as raised:
        assure_coverage(root, base=base, candidate=candidate, evidence_dir=tmp_path / "evidence")

    assert raised.value.details["side"] == "candidate"
    assert raised.value.details["phase"] == "provision"


def test_in_process_transaction_wraps_controller_measurement_failure(tmp_path: Path) -> None:
    from tc_fitness.coverage_transaction import TransactionError, assure_coverage

    root = tmp_path / "repo"
    repository(root)
    git(root, "rm", "-q", "uv.lock")
    candidate = commit(root)
    evidence = tmp_path / "evidence"

    with pytest.raises(TransactionError) as raised:
        assure_coverage(root, base=candidate, candidate=candidate, evidence_dir=evidence)

    assert raised.value.details["side"] == "base"
    assert raised.value.details["phase"] == "measurement"
    assert "uv.lock" in (evidence / str(raised.value.details["stderr_log"])).read_text()


def test_transaction_rejects_lock_changed_after_provisioning_starts(tmp_path: Path) -> None:
    from tc_fitness.coverage_transaction import TransactionError, assure_coverage

    root = tmp_path / "repo"
    _, candidate = repository(root)
    evidence = tmp_path / "evidence"
    changed: list[Path] = []

    def change_detached_lock() -> None:
        deadline = time.monotonic() + 10
        log = evidence / "base/uv.stdout.log"
        while time.monotonic() < deadline and not log.exists():
            time.sleep(0.001)
        if not log.exists():
            return
        worktrees = git(root, "worktree", "list", "--porcelain").splitlines()
        snapshots = [
            Path(line.removeprefix("worktree "))
            for line in worktrees
            if line.startswith("worktree ")
            and "tc-fitness-coverage-transaction-" in line
            and line.endswith("/base")
        ]
        if snapshots:
            lock = snapshots[0] / "uv.lock"
            lock.write_text(lock.read_text() + "\n# concurrent drift\n")
            changed.append(lock)

    writer = threading.Thread(target=change_detached_lock)
    writer.start()
    try:
        with pytest.raises(TransactionError, match="changed the bound lockfile"):
            assure_coverage(root, base=candidate, candidate=candidate, evidence_dir=evidence)
    finally:
        writer.join(timeout=10)

    assert changed


def test_in_process_transaction_classifies_only_registered_contract_fixtures(tmp_path: Path) -> None:
    from tc_fitness.coverage_transaction import assure_coverage

    root = tmp_path / "repo"
    base, _ = repository(root)
    registry = root / "tests/check_contracts"
    name = "every_test_has_tier_marker"
    shutil.copytree(Path(__file__).parent / "check_contracts" / name, registry / name)
    (registry / "unknown").mkdir()
    (registry / "unknown/contract.yaml").write_text("not-a-contract: true\n")
    candidate = commit(root)

    result = assure_coverage(root, base=base, candidate=candidate, evidence_dir=tmp_path / "evidence")

    assert result.failures == ()


@pytest.mark.parametrize("write_output", [False, True])
def test_transaction_main_returns_public_result_for_successful_measurement(
    tmp_path: Path, write_output: bool, capsys: pytest.CaptureFixture[str]
) -> None:
    from tc_fitness.coverage_transaction import main

    root = tmp_path / "repo"
    _, candidate = repository(root)
    arguments = [
        "--repo-root",
        str(root),
        "--base-commit",
        candidate,
        "--candidate-commit",
        candidate,
        "--evidence-dir",
        str(tmp_path / "evidence"),
    ]
    output = tmp_path / "result.json"
    if write_output:
        arguments.extend(["--output", str(output)])

    code = main(arguments)

    assert code == 0
    payload = json.loads(output.read_text() if write_output else capsys.readouterr().out)
    assert payload["status"] == "pass"
