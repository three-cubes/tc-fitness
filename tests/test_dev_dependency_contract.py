"""Pin the repository's canonical development dependency contract."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration
ROOT = Path(__file__).parents[1]


def test_dev_tools_use_one_locked_dependency_group_across_local_surfaces() -> None:
    manifest = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = manifest["project"]
    groups = manifest["dependency-groups"]

    assert "dev" not in project.get("optional-dependencies", {})
    assert groups["dev"] == [
        "pytest>=8.0",
        "pytest-cov>=5.0",
        "ruff>=0.15,<0.16",
        "mypy>=1.11",
        "checkov==3.2.531",
    ]

    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    qualification = (ROOT / "scripts/qualification/distribution.sh").read_text(encoding="utf-8")
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "uv sync --locked --group dev" in makefile
    assert "[project.optional-dependencies]" in readme
    assert "uv sync --all-extras --all-groups" not in readme
    assert "uv sync --locked --all-extras --all-groups" not in readme
    assert "--group dev" in qualification
    assert "--all-extras" not in qualification
    assert "--all-groups" not in qualification
    assert "--group dev" in workflow
    assert "--all-extras" not in workflow


def test_readme_distinguishes_consumer_extra_bootstrap_from_daily_locked_sync() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "uv lock" in readme
    onboarding = readme.split("3. **Run it locally.**", 1)[1].split("4. **Point CI", 1)[0]
    assert "uv sync --locked --extra dev" in onboarding
    assert "uv sync --locked --group dev" not in onboarding


def test_readme_describes_coverage_compatibility_provisioning() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "Each detached checkout gets its own external environment provisioned with" in readme
    assert "uv sync --locked --all-extras" in readme
