"""Behavioural checks for the CI Quality gate fan-in evaluator."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
FAN_IN = REPO_ROOT / "scripts" / "qualification" / "quality_gate_fanin.py"

pytestmark = pytest.mark.integration


def _run(needs: dict[str, dict[str, str]]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(FAN_IN)],
        cwd=REPO_ROOT,
        env={**os.environ, "NEEDS_JSON": json.dumps(needs)},
        capture_output=True,
        check=False,
        text=True,
    )


def test_fan_in_accepts_only_successful_required_workers() -> None:
    """Branch protection requires qualification and mutation workers to succeed."""
    needs = {
        "check-static": {"result": "success"},
        "coverage-assurance": {"result": "success"},
        "distribution-qualification": {"result": "success"},
        "changed-mutation": {"result": "success"},
    }
    result = _run(needs)

    assert result.returncode == 0, result.stderr


def test_fan_in_rejects_a_non_successful_required_worker() -> None:
    """A cancelled or failed matrix worker must make the protected result fail."""
    result = _run(
        {
            "check-static": {"result": "success"},
            "coverage-assurance": {"result": "success"},
            "distribution-qualification": {"result": "cancelled"},
            "changed-mutation": {"result": "success"},
        }
    )

    assert result.returncode == 1
    assert "distribution-qualification=cancelled" in result.stderr


@pytest.mark.parametrize("state", ["failure", "cancelled", "skipped", None])
def test_mutation_failure_or_missing_worker_cannot_pass_branch_protection(state: str | None) -> None:
    needs = {
        "check-static": {"result": "success"},
        "coverage-assurance": {"result": "success"},
        "distribution-qualification": {"result": "success"},
    }
    if state is not None:
        needs["changed-mutation"] = {"result": state}
    assert _run(needs).returncode == 1


@pytest.mark.parametrize("state", ["failure", "cancelled", "skipped", None])
def test_coverage_failure_or_missing_worker_cannot_pass_branch_protection(state: str | None) -> None:
    needs = {
        "check-static": {"result": "success"},
        "distribution-qualification": {"result": "success"},
        "changed-mutation": {"result": "success"},
    }
    if state is not None:
        needs["coverage-assurance"] = {"result": state}
    assert _run(needs).returncode == 1
