"""Keep every GitHub Actions uv installer on the reviewed repository pin."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = REPO_ROOT / ".github" / "workflows"
CI_WORKFLOW = WORKFLOWS / "ci.yml"
RESOLVER_ACTION = REPO_ROOT / ".github" / "actions" / "resolve-uv-version" / "action.yml"
RESOLVER_USE = "./.github/actions/resolve-uv-version"
DIRECT_SETUP_UV = "astral-sh/setup-uv@"
SHARED_SETUP_UV = "three-cubes/tc-pipelines/actions/setup-uv-cached@"
EXACT_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
QUALITY_GATE_WORKERS = frozenset(
    {"check-static", "coverage-assurance", "distribution-qualification", "changed-mutation"}
)
FAN_IN_NEEDS_JSON = "${{ toJSON(needs) }}"
FAN_IN_RUN = "python3 scripts/qualification/quality_gate_fanin.py"


def _jobs(workflows: Path) -> list[tuple[Path, str, list[dict[str, Any]]]]:
    found: list[tuple[Path, str, list[dict[str, Any]]]] = []
    workflow_paths = sorted((*workflows.glob("*.yml"), *workflows.glob("*.yaml")))
    for workflow_path in workflow_paths:
        workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        for job_name, job in (workflow.get("jobs") or {}).items():
            if not isinstance(job, dict):
                continue
            steps = [step for step in job.get("steps") or [] if isinstance(step, dict)]
            found.append((workflow_path, str(job_name), steps))
    return found


def _uv_setup_violations(repo_root: Path) -> list[str]:
    pin_path = repo_root / ".uv-version"
    if not pin_path.is_file():
        return [".uv-version is missing"]

    pin = pin_path.read_text(encoding="utf-8").strip()
    violations: list[str] = []
    if not EXACT_VERSION.fullmatch(pin):
        violations.append(f".uv-version must contain one exact x.y.z version, got {pin!r}")

    jobs = _jobs(repo_root / ".github" / "workflows")
    resolver_path = repo_root / ".github" / "actions" / "resolve-uv-version" / "action.yml"
    has_setup = any(
        isinstance(step.get("uses"), str) and step["uses"].startswith((DIRECT_SETUP_UV, SHARED_SETUP_UV))
        for _, _, steps in jobs
        for step in steps
    )
    if has_setup and not resolver_path.is_file():
        violations.append("the .uv-version resolver action is missing")

    for workflow_path, job_name, steps in jobs:
        for index, step in enumerate(steps):
            uses = step.get("uses")
            if not isinstance(uses, str):
                continue
            inputs = step.get("with") or {}
            location = f"{workflow_path.relative_to(repo_root)}:{job_name}:{step.get('name', uses)}"

            if uses.startswith((DIRECT_SETUP_UV, SHARED_SETUP_UV)):
                preceding = steps[:index]
                if not any(
                    candidate.get("uses") == RESOLVER_USE and candidate.get("id") == "uv-version"
                    for candidate in preceding
                ):
                    violations.append(f"{location} must run the .uv-version resolver first")
                version_input = "version" if uses.startswith(DIRECT_SETUP_UV) else "uv-version"
                if inputs.get(version_input) != "${{ steps.uv-version.outputs.version }}":
                    violations.append(f"{location} must install the resolved .uv-version output")
                if "version-file" in inputs:
                    violations.append(f"{location} must not pass .uv-version as version-file")

    return violations


def _quality_gate_violations(workflow: dict[str, Any]) -> list[str]:
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        return ["workflow must declare jobs"]

    fan_ins = [
        (job_id, job)
        for job_id, job in jobs.items()
        if isinstance(job, dict) and job.get("name") == "Quality gate"
    ]
    if len(fan_ins) != 1:
        return ["workflow must declare exactly one job named Quality gate"]

    job_id, quality_gate = fan_ins[0]
    violations: list[str] = []
    if job_id in QUALITY_GATE_WORKERS:
        violations.append("Quality gate must be distinct from its worker jobs")
    if "strategy" in quality_gate:
        violations.append("Quality gate must be a non-matrix fan-in job")
    needs = quality_gate.get("needs", [])
    needed_jobs = {needs} if isinstance(needs, str) else set(needs) if isinstance(needs, list) else set()
    missing = sorted(QUALITY_GATE_WORKERS - needed_jobs)
    if missing:
        violations.append(f"Quality gate must need every worker: {', '.join(missing)}")
    if quality_gate.get("if") != "${{ always() }}":
        violations.append("Quality gate must run after failed workers to report their result")
    steps = quality_gate.get("steps", [])
    invokes_evaluator = any(
        isinstance(step, dict)
        and step.get("run") == FAN_IN_RUN
        and isinstance(step.get("env"), dict)
        and step["env"].get("NEEDS_JSON") == FAN_IN_NEEDS_JSON
        for step in steps
    )
    if not invokes_evaluator:
        violations.append("Quality gate must evaluate every worker result")
    return violations


def test_every_uv_setup_reads_the_reviewed_repository_pin() -> None:
    """Changing or adding any workflow installer must not create a second uv pin."""
    assert _uv_setup_violations(REPO_ROOT) == []


def test_quality_gate_is_a_non_matrix_fan_in_for_all_qualification_workers() -> None:
    """A worker matrix must not replace branch protection's one Quality gate result."""
    workflow = yaml.safe_load(CI_WORKFLOW.read_text(encoding="utf-8"))
    assert _quality_gate_violations(workflow) == []


def test_resolver_action_accepts_only_an_exact_uv_version(tmp_path: Path) -> None:
    """The adapter proves the file before passing it to setup-uv's version input."""
    action = yaml.safe_load(RESOLVER_ACTION.read_text(encoding="utf-8"))
    script = action["runs"]["steps"][0]["run"]

    def run(value: str | None) -> subprocess.CompletedProcess[str]:
        if value is not None:
            (tmp_path / ".uv-version").write_text(value, encoding="utf-8")
        output = tmp_path / "github-output"
        return subprocess.run(
            ["bash", "-c", script],
            cwd=tmp_path,
            env={**os.environ, "GITHUB_OUTPUT": str(output)},
            capture_output=True,
            check=False,
            text=True,
        )

    assert run("0.12.5\n").returncode == 0
    assert (tmp_path / "github-output").read_text(encoding="utf-8") == "version=0.12.5\n"
    (tmp_path / "github-output").unlink()
    assert run("latest\n").returncode != 0
    (tmp_path / ".uv-version").unlink()
    assert run(None).returncode != 0


def test_parity_check_examines_every_setup_occurrence(tmp_path: Path) -> None:
    """One correct installer must not hide a stale installer later in the workflow."""
    (tmp_path / ".uv-version").write_text("0.12.5\n", encoding="utf-8")
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "release.yml").write_text(
        """\
jobs:
  release:
    steps:
      - name: Correct installer
        id: uv-version
        uses: ./.github/actions/resolve-uv-version
      - name: Correct setup
        uses: astral-sh/setup-uv@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        with:
          version: ${{ steps.uv-version.outputs.version }}
      - name: Stale installer
        uses: astral-sh/setup-uv@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        with:
          version-file: .uv-version
""",
        encoding="utf-8",
    )

    assert _uv_setup_violations(tmp_path) == [
        "the .uv-version resolver action is missing",
        ".github/workflows/release.yml:release:Stale installer must install the resolved .uv-version output",
        ".github/workflows/release.yml:release:Stale installer must not pass .uv-version as version-file",
    ]


def _shared_setup_fixture(tmp_path: Path, inputs: dict[str, str], *, resolver: bool = True) -> None:
    (tmp_path / ".uv-version").write_text("0.12.5\n", encoding="utf-8")
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    action = tmp_path / ".github" / "actions" / "resolve-uv-version" / "action.yml"
    action.parent.mkdir(parents=True)
    action.write_text(RESOLVER_ACTION.read_text(encoding="utf-8"), encoding="utf-8")
    steps: list[dict[str, Any]] = []
    if resolver:
        steps.append({"id": "uv-version", "uses": RESOLVER_USE})
    steps.append(
        {
            "name": "Shared installer",
            "uses": SHARED_SETUP_UV + "b" * 40,
            "with": inputs,
        }
    )
    (workflows / "ci.yaml").write_text(
        yaml.safe_dump({"jobs": {"check": {"steps": steps}}}), encoding="utf-8"
    )


def test_parity_check_rejects_a_shared_setup_override(tmp_path: Path) -> None:
    """An explicit but different pin must not bypass the repository version."""
    _shared_setup_fixture(tmp_path, {"uv-version": "0.11.0"})
    assert _uv_setup_violations(tmp_path) == [
        ".github/workflows/ci.yaml:check:Shared installer must install the resolved .uv-version output"
    ]


def test_parity_check_rejects_a_shared_setup_without_a_pin(tmp_path: Path) -> None:
    """The pinned shared action's default is not the repository's exact uv pin."""
    _shared_setup_fixture(tmp_path, {})
    assert _uv_setup_violations(tmp_path) == [
        ".github/workflows/ci.yaml:check:Shared installer must install the resolved .uv-version output"
    ]


def test_parity_check_accepts_a_shared_setup_using_resolved_pin(tmp_path: Path) -> None:
    """The supported shared-action input must accept the validated resolver output."""
    _shared_setup_fixture(tmp_path, {"uv-version": "${{ steps.uv-version.outputs.version }}"})
    assert _uv_setup_violations(tmp_path) == []


def test_parity_check_requires_shared_setup_resolver_first(tmp_path: Path) -> None:
    """A reference to an output is invalid if its producer never ran in this job."""
    _shared_setup_fixture(tmp_path, {"uv-version": "${{ steps.uv-version.outputs.version }}"}, resolver=False)
    assert _uv_setup_violations(tmp_path) == [
        ".github/workflows/ci.yaml:check:Shared installer must run the .uv-version resolver first"
    ]


def test_parity_check_requires_shared_setup_resolver_action(tmp_path: Path) -> None:
    """A missing local action must fail even when only shared installers are used."""
    _shared_setup_fixture(tmp_path, {"uv-version": "${{ steps.uv-version.outputs.version }}"})
    (tmp_path / ".github" / "actions" / "resolve-uv-version" / "action.yml").unlink()
    assert _uv_setup_violations(tmp_path) == ["the .uv-version resolver action is missing"]
