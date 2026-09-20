"""Behavioural and declarative contracts for this repository's self gate."""

from __future__ import annotations

import subprocess
import tomllib
from pathlib import Path

import pytest
import yaml

REPOSITORY = Path(__file__).resolve().parents[1]

pytestmark = pytest.mark.integration


def test_static_evaluation_is_withheld_for_an_uncommitted_tree(tmp_path: Path) -> None:
    (tmp_path / "Makefile").write_bytes((REPOSITORY / "Makefile").read_bytes())
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "Makefile"], cwd=tmp_path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Contract",
            "-c",
            "user.email=contract@example.invalid",
            "commit",
            "-qm",
            "fixture",
        ],
        cwd=tmp_path,
        check=True,
    )
    (tmp_path / "uncommitted.py").write_text("value = 1\n")

    result = subprocess.run(
        ["make", "check-static"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "evaluation withheld: commit or remove every working-tree change" in (
        result.stdout + result.stderr
    )
    assert "tc-fitness run" not in result.stdout


def test_repository_gate_declares_static_evaluation_only() -> None:
    configuration = tomllib.loads((REPOSITORY / "pyproject.toml").read_text())
    fitness = configuration["tool"]["tc_fitness"]

    assert [step["id"] for step in fitness["steps"]] == [
        "ruff",
        "ruff-format",
        "mypy",
        "branch-naming",
    ]
    rendered = (REPOSITORY / "pyproject.toml").read_text()
    assert "TC_FITNESS_ACCEPTED_COVERAGE" not in rendered
    assert "accepted_coverage_receipt" not in rendered
    assert "coverage_admission" not in rendered
    assert "coverage_catalogue" not in rendered


def test_pull_request_ci_has_one_exact_commit_coverage_transaction() -> None:
    workflow = yaml.safe_load((REPOSITORY / ".github/workflows/ci.yml").read_text())
    triggers = workflow.get("on", workflow.get(True))
    assert set(triggers) == {"pull_request"}
    jobs = workflow["jobs"]
    assert "check-static" in jobs
    assert "coverage-assurance" in jobs
    assert "check" not in jobs

    static_steps = jobs["check-static"]["steps"]
    static_checkout = static_steps[0]
    assert static_checkout["with"]["ref"] == "${{ github.event.pull_request.head.sha }}"
    static_commands = [step["run"] for step in static_steps if "run" in step]
    assert any(
        command.index("make prepare") < command.index("make check-static") for command in static_commands
    )

    assurance_steps = jobs["coverage-assurance"]["steps"]
    assurance_checkout = assurance_steps[0]
    assert assurance_checkout["with"]["ref"] == "${{ github.event.pull_request.head.sha }}"
    assurance_step = next(step for step in assurance_steps if "assure-coverage" in step.get("run", ""))
    assert assurance_step["env"] == {
        "BASE_SHA": "${{ github.event.pull_request.base.sha }}",
        "HEAD_SHA": "${{ github.event.pull_request.head.sha }}",
        "EVIDENCE_DIR": "${{ runner.temp }}/coverage-assurance",
    }
    commands = [step["run"] for step in assurance_steps if "run" in step]
    assurance_commands = [command for command in commands if "assure-coverage" in command]
    assert len(assurance_commands) == 1
    command = assurance_commands[0]
    assert '--base-commit "$BASE_SHA"' in command
    assert '--candidate-commit "$HEAD_SHA"' in command
    assert '--evidence-dir "$EVIDENCE_DIR"' in command
    assert (
        command.index("make prepare") < command.index("make assert-clean") < command.index("assure-coverage")
    )

    assert set(jobs["quality-gate"]["needs"]) == {
        "check-static",
        "coverage-assurance",
        "distribution-qualification",
        "changed-mutation",
    }
