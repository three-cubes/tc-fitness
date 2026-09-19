"""The package version is sourced from installed distribution metadata."""

from __future__ import annotations

import importlib.metadata
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

import tc_fitness

pytestmark = pytest.mark.integration


def test_version_matches_installed_metadata() -> None:
    try:
        metadata_version = importlib.metadata.version("three-cubes-fitness")
    except importlib.metadata.PackageNotFoundError:  # pragma: no cover - only when not installed
        # Not installed in-tree: just prove the literal is non-empty + dotted.
        assert tc_fitness.__version__
        assert "." in tc_fitness.__version__
        return
    assert tc_fitness.__version__ == metadata_version


def test_version_matches_project_declaration() -> None:
    """Installed metadata reflects the single project declaration."""
    project = tomllib.loads((Path(__file__).parents[1] / "pyproject.toml").read_text(encoding="utf-8"))
    assert tc_fitness.__version__ == project["project"]["version"]


def test_bare_checkout_has_stable_unknown_version_without_release_literal() -> None:
    """A source-only import works without creating a second version authority."""
    source = Path(__file__).parents[1] / "src"
    process = subprocess.run(
        [
            sys.executable,
            "-S",
            "-c",
            (
                "import sys; "
                f"sys.path.insert(0, {str(source)!r}); "
                "import tc_fitness; "
                "print(tc_fitness.__version__)"
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert process.returncode == 0, process.stderr
    assert process.stdout.strip() == "0+unknown"
