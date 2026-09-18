"""Keep every GitHub Actions uv installer on the reviewed repository pin."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = REPO_ROOT / ".github" / "workflows"
RESOLVER_ACTION = REPO_ROOT / ".github" / "actions" / "resolve-uv-version" / "action.yml"
RESOLVER_USE = "./.github/actions/resolve-uv-version"
DIRECT_SETUP_UV = "astral-sh/setup-uv@"
SHARED_SETUP_UV = "three-cubes/tc-pipelines/actions/setup-uv-cached@"
EXACT_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


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
    has_direct_setup = any(
        isinstance(step.get("uses"), str) and step["uses"].startswith(DIRECT_SETUP_UV)
        for _, _, steps in jobs
        for step in steps
    )
    if has_direct_setup and not resolver_path.is_file():
        violations.append("the .uv-version resolver action is missing")

    for workflow_path, job_name, steps in jobs:
        for index, step in enumerate(steps):
            uses = step.get("uses")
            if not isinstance(uses, str):
                continue
            inputs = step.get("with") or {}
            location = f"{workflow_path.relative_to(repo_root)}:{job_name}:{step.get('name', uses)}"

            if uses.startswith(DIRECT_SETUP_UV):
                preceding = steps[:index]
                if not any(
                    candidate.get("uses") == RESOLVER_USE and candidate.get("id") == "uv-version"
                    for candidate in preceding
                ):
                    violations.append(f"{location} must run the .uv-version resolver first")
                if inputs.get("version") != "${{ steps.uv-version.outputs.version }}":
                    violations.append(f"{location} must install the resolved .uv-version output")
                if "version-file" in inputs:
                    violations.append(f"{location} must not pass .uv-version as version-file")
            elif uses.startswith(SHARED_SETUP_UV) and "uv-version" in inputs:
                violations.append(f"{location} must let setup-uv-cached read .uv-version")

    return violations


def test_every_uv_setup_reads_the_reviewed_repository_pin() -> None:
    """Changing or adding any workflow installer must not create a second uv pin."""
    assert _uv_setup_violations(REPO_ROOT) == []


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


def test_parity_check_rejects_a_shared_setup_override(tmp_path: Path) -> None:
    """The shared installer must use its repository-file path, not a workflow literal."""
    (tmp_path / ".uv-version").write_text("0.12.5\n", encoding="utf-8")
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yaml").write_text(
        """\
jobs:
  check:
    steps:
      - name: Shared installer
        uses: three-cubes/tc-pipelines/actions/setup-uv-cached@bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
        with:
          uv-version: 0.11.0
""",
        encoding="utf-8",
    )

    assert _uv_setup_violations(tmp_path) == [
        ".github/workflows/ci.yaml:check:Shared installer must let setup-uv-cached read .uv-version"
    ]
