"""Fresh exact-Git coverage transactions through the installed public command."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


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
        assert toolchain["pytest"] == "9.1.0"
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
    code, result = invoke(root, base, candidate, tmp_path / "result.json")
    assert code == 1, result
    assert any("branch coverage decreased from fresh exact base" in item for item in result["failures"])
    assert not any("below" in item for item in result["failures"])


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
    assert json.loads((retained / "transaction.json").read_text()) == result
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
    assert result["base"]["toolchain"]["pytest"] == "9.1.0"
    assert result["candidate"]["toolchain"]["pytest"] == "9.0.2"
    assert result["base"]["toolchain"]["lock_digest"] != result["candidate"]["toolchain"]["lock_digest"]
