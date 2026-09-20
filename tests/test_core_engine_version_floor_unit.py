"""Tests for the CORE check engine_version_floor (SGO-190).

Reads the consuming repo's pinned three-cubes-fitness tag and FAILS when it is
below a centrally-declared floor; a repo with no floor configured — or whose
version cannot be resolved — is a guard-forward no-op.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness.core_checks.engine_version_floor import (
    DEFAULT_PACKAGE,
    parse_version,
)

pytestmark = pytest.mark.unit

PKG = DEFAULT_PACKAGE


def _git_dep(tag: str) -> str:
    return f"{PKG} @ git+https://github.com/three-cubes/tc-fitness.git@{tag}"


def _manifest(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "pyproject.toml"
    path.write_text(body, encoding="utf-8")
    return path


def _project_with_dep(tmp_path: Path, dep: str) -> Path:
    return _manifest(tmp_path, f'[project]\nname = "consumer"\ndependencies = ["{dep}"]\n')


def test_parse_version_reads_dotted_release() -> None:
    assert parse_version("v0.6.1") == (0, 6, 1)
    assert parse_version("0.7.0") == (0, 7, 0)
    assert parse_version(" v1.2 ") == (1, 2)


def test_parse_version_rejects_non_numeric() -> None:
    assert parse_version("main") is None
    assert parse_version("") is None
