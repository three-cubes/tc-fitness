"""Tests for the CORE check no_language_suffix_in_package_names (v0.6.0)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness.core_checks.no_language_suffix_in_package_names import (
    name_has_language_suffix,
)

pytestmark = pytest.mark.unit


def _mkdir(tmp_path: Path, rel: str) -> Path:
    p = tmp_path / rel
    p.mkdir(parents=True, exist_ok=True)
    return p


def test_detection_flags_suffix() -> None:
    assert name_has_language_suffix("mcp-render-ts", suffixes=("-ts",)) is True


def test_detection_clean() -> None:
    assert name_has_language_suffix("mcp-render", suffixes=("-ts", "-py")) is False
