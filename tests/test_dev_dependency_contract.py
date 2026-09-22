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
