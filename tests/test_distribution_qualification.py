"""End-to-end proof that released distributions remain executable."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
QUALIFICATION = REPO_ROOT / "scripts" / "qualification" / "distribution.sh"

pytestmark = pytest.mark.e2e


def test_distribution_qualification_exercises_both_installed_artifact_paths() -> None:
    """A released wheel and an isolated wheel rebuilt from the sdist must both run."""
    result = subprocess.run(
        ["bash", str(QUALIFICATION), "--python", sys.executable],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "qualified direct wheel" in result.stdout
    assert "qualified wheel rebuilt from sdist" in result.stdout
    assert "qualified direct-wheel coverage transaction" in result.stdout
    assert "qualified wheel-from-sdist coverage transaction" in result.stdout
    assert "qualified direct-wheel locked assurance tools" in result.stdout
    assert "qualified wheel-from-sdist locked assurance tools" in result.stdout
