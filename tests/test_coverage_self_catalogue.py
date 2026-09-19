"""The installed public gate cannot suppress its coverage catalogue."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


def seed(root: Path, relative: str, body: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    return path


def invoke(root: Path, *args: str) -> int:
    return subprocess.run(
        [str(Path(sys.executable).with_name("tc-fitness")), "run", "--repo-root", str(root), *args],
        capture_output=True,
        timeout=15,
        check=False,
    ).returncode


def consumer(root: Path, *, strict: bool = True, extra: str = "") -> None:
    seed(
        root,
        "checks.py",
        "from tc_fitness.catalogue import RuleEntry\nENTRIES = (RuleEntry(id='branches', gate='branches', check='core:coverage_includes_branches'),)\n",
    )
    seed(
        root,
        ".tc-fitness.toml",
        "[[steps]]\nid='coverage'\ncatalogue='checks:ENTRIES'\n"
        + ("baseline_free=true\n" if strict else "")
        + extra,
    )
    seed(root, "coverage.xml", '<coverage branch-rate="0" branches-valid="0"/>')


def test_catalogue_does_not_consume_baseline_debt(tmp_path: Path) -> None:
    consumer(tmp_path, strict=False)
    seed(tmp_path, ".architecture/baseline/coverage-includes-branches-files.txt", "coverage.xml\n")
    assert invoke(tmp_path) == 0
    consumer(tmp_path)
    assert invoke(tmp_path) == 1


def test_catalogue_rejects_public_establish_baseline(tmp_path: Path) -> None:
    consumer(tmp_path)
    assert invoke(tmp_path, "--establish-baseline") == 1
    assert not (tmp_path / ".architecture/baseline").exists()


def test_dispatched_python_check_cannot_write_a_baseline(tmp_path: Path) -> None:
    consumer(tmp_path)
    seed(
        tmp_path,
        "checks.py",
        "from tc_fitness.catalogue import RuleEntry\nENTRIES = (RuleEntry(id='escape', gate='escape', check='escape'),)\n",
    )
    seed(
        tmp_path,
        "scripts/checks/check_escape.py",
        "from pathlib import Path\nfrom tc_fitness.baseline import establish_baseline\ndef main():\n    establish_baseline('escape', ['coverage.xml'], Path("
        + repr(str(tmp_path))
        + "))\n    return 0\n",
    )
    assert invoke(tmp_path) == 1
    assert not (tmp_path / ".architecture/baseline").exists()


def test_baseline_free_step_rejects_conditional_python_subprocess(tmp_path: Path) -> None:
    consumer(tmp_path)
    seed(
        tmp_path,
        "checks.py",
        "from tc_fitness.catalogue import RuleEntry\n"
        "ENTRIES = (RuleEntry(id='escape', gate='escape', check='escape', "
        "subprocess_arg_env='COVERAGE_EVIDENCE', "
        "subprocess_arg_default='coverage.xml'),)\n",
    )
    seed(
        tmp_path,
        "scripts/checks/check_escape.py",
        "from pathlib import Path\n"
        "from tc_fitness.baseline import establish_baseline\n"
        "def main():\n"
        "    establish_baseline('escape', ['coverage.xml'], Path(" + repr(str(tmp_path)) + "))\n"
        "    return 0\n",
    )

    assert invoke(tmp_path) != 0
    assert not (tmp_path / ".architecture/baseline").exists()


@pytest.mark.parametrize(
    "extra",
    ['dispatch="subprocess"\n', "continue_on_error=true\n", "allow_missing=true\n", "parallel=true\n"],
)
def test_baseline_free_step_rejects_execution_escape_configuration(tmp_path: Path, extra: str) -> None:
    consumer(tmp_path, extra=extra)
    seed(tmp_path, "coverage.xml", '<coverage branch-rate="1" branches-valid="2"/>')
    assert invoke(tmp_path) != 0


def test_repository_coverage_catalogue_is_executable_and_requires_evidence(tmp_path: Path) -> None:
    repository = Path(__file__).resolve().parents[1]
    config = tomllib.loads((repository / "pyproject.toml").read_text())["tool"]["tc_fitness"]
    steps = [step for step in config["steps"] if step.get("id") == "coverage-assurance"]
    assert len(steps) == 1, "the public self gate must dispatch its coverage catalogue"
    from tc_fitness.check_evidence import capture_check_evidence
    from tc_fitness.gate import run_gate
    from tc_fitness.gate_config import load_config

    # Execute the actual repository declaration against an empty candidate:
    # a missing report/base/receipt must produce findings, never disappear.
    seed(tmp_path, "pyproject.toml", (repository / "pyproject.toml").read_text())
    with capture_check_evidence() as evidence:
        outcome = run_gate(load_config(tmp_path), tmp_path, only=["coverage-assurance"])
    assert outcome.exit_code != 0
    assert {result.check for result in evidence.results} == {
        "core:coverage_includes_branches",
        "core:coverage_floor",
        "core:new_code_coverage",
    }
    assert all(result.status in {"fail", "error"} for result in evidence.results)


def test_repository_test_step_produces_fresh_bound_evidence(tmp_path: Path) -> None:
    from tc_fitness.coverage_admission import produce_coverage

    repository = Path(__file__).resolve().parents[1]
    seed(tmp_path, "pyproject.toml", (repository / "pyproject.toml").read_text())
    seed(tmp_path, ".gitignore", "__pycache__/\n.coverage*\ncoverage.*\n")
    names = ["subject", "gate", "runner", "gate_config", "runtime_contract"]
    for name in names:
        seed(
            tmp_path,
            f"src/tc_fitness/{name}.py",
            "def choose(flag):\n    if flag:\n        return 1\n    return 0\n",
        )
    seed(
        tmp_path,
        "tests/test_subject.py",
        "import runpy\nimport pytest\npytestmark = pytest.mark.integration\n@pytest.mark.parametrize('name', "
        + repr(names)
        + ")\ndef test_choices(name):\n    choice = runpy.run_path(f'src/tc_fitness/{name}.py')['choose']\n    assert choice(True) == 1\n    assert choice(False) == 0\n",
    )

    def git(*args: str) -> str:
        result = subprocess.run(["git", *args], cwd=tmp_path, capture_output=True, text=True, check=True)
        return result.stdout.strip()

    git("init", "-q")
    git("add", ".")
    git("-c", "user.name=Contract", "-c", "user.email=contract@example.invalid", "commit", "-qm", "fixture")
    commit = git("rev-parse", "HEAD")
    output = tmp_path.parent / (tmp_path.name + "-measurement")
    accepted = output.with_name(output.name + "-accepted")
    prior = produce_coverage(
        root=tmp_path,
        base=commit,
        candidate=commit,
        roots=["src/tc_fitness"],
        config="pyproject.toml",
        run_id="accepted-run",
        attempt_id="1",
        output=accepted,
        command=["-m", "pytest", "-q"],
    )
    environment = {
        **os.environ,
        "TC_FITNESS_BASE_COMMIT": commit,
        "TC_FITNESS_CANDIDATE_COMMIT": commit,
        "TC_FITNESS_RUN_ID": "self-test",
        "TC_FITNESS_ATTEMPT_ID": "1",
        "TC_FITNESS_COVERAGE_OUTPUT": str(output),
        "TC_FITNESS_COVERAGE_DIGEST_FILE": str(output.parent / (output.name + ".sha256")),
        "TC_FITNESS_COVERAGE_RECEIPT": str(output / "receipt.json"),
        "TC_FITNESS_COVERAGE_REPORT": str(output / "coverage.xml"),
        "TC_FITNESS_ACCEPTED_COVERAGE_RECEIPT": str(accepted / "receipt.json"),
        "TC_FITNESS_ACCEPTED_COVERAGE_DIGEST": prior["digest"],
    }
    result = subprocess.run(
        [
            str(Path(sys.executable).with_name("tc-fitness")),
            "run",
            "--repo-root",
            str(tmp_path),
            "--only",
            "pytest",
            "--only",
            "coverage-assurance",
        ],
        env=environment,
        capture_output=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    receipt = output / "receipt.json"
    assert receipt.is_file(), "the actual self-test command must emit bound coverage, not only XML"
    payload = json.loads(receipt.read_text())
    assert payload["candidate_commit"] == commit
    assert payload["counts"] == {"lines": 20, "covered_lines": 20, "branches": 10, "covered_branches": 10}
    anchor = Path(environment["TC_FITNESS_COVERAGE_DIGEST_FILE"])
    assert anchor.is_file(), "the producing step must hand its digest to later admission"
    assert anchor.read_text().strip() == payload["digest"]
    receipt.write_text(receipt.read_text().replace('"attempt_id": "1"', '"attempt_id": "tampered"'))
    result = subprocess.run(
        [
            str(Path(sys.executable).with_name("tc-fitness")),
            "run",
            "--repo-root",
            str(tmp_path),
            "--only",
            "coverage-assurance",
        ],
        env=environment,
        capture_output=True,
        check=False,
        timeout=15,
    )
    assert result.returncode == 1


def test_catalogue_import_cannot_write_a_baseline_before_dispatch(tmp_path: Path) -> None:
    consumer(tmp_path)
    path = tmp_path / "checks.py"
    path.write_text(
        "from pathlib import Path\nfrom tc_fitness.baseline import establish_baseline\nestablish_baseline('escape', [], Path("
        + repr(str(tmp_path))
        + "))\n"
        + path.read_text()
    )
    assert invoke(tmp_path) == 1
    assert not (tmp_path / ".architecture/baseline").exists()
