"""Tests for the CORE check path_naming (v0.6.0)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness.core_checks.path_naming import (
    name_violates_convention,
)

pytestmark = pytest.mark.unit


def _seed(tmp_path: Path, rel: str, body: str = "x\n") -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_bad_kebab_md() -> None:
    assert (
        name_violates_convention(
            "docs/MyNote.md",
            kebab_roots=("docs/",),
            snake_roots=(),
        )
        is True
    )


def test_detection_good_kebab_md() -> None:
    assert (
        name_violates_convention(
            "docs/my-note.md",
            kebab_roots=("docs/",),
            snake_roots=(),
        )
        is False
    )


def test_detection_bad_snake_py() -> None:
    assert (
        name_violates_convention(
            "scripts/My-Check.py",
            kebab_roots=(),
            snake_roots=("scripts/",),
        )
        is True
    )


def test_detection_good_snake_py() -> None:
    assert (
        name_violates_convention(
            "scripts/my_check.py",
            kebab_roots=(),
            snake_roots=("scripts/",),
        )
        is False
    )


def test_allowed_name_exempt() -> None:
    assert (
        name_violates_convention(
            "docs/README.md",
            kebab_roots=("docs/",),
            snake_roots=(),
        )
        is False
    )


def test_path_under_no_root_is_clean() -> None:
    assert (
        name_violates_convention(
            "vendor/BadName.md",
            kebab_roots=("docs/",),
            snake_roots=(),
        )
        is False
    )
