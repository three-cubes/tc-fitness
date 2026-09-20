"""Tests for the per-file baseline I/O (v0.6.0)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness.baseline import (
    BASELINE_SUFFIX,
    baseline_path,
    establish_baseline,
    load_baseline,
    parse_baseline_text,
)

pytestmark = pytest.mark.integration


def test_baseline_path_is_canonical_suffix(tmp_path: Path) -> None:
    p = baseline_path("no-duplicate-string", tmp_path)
    assert p == tmp_path / ".architecture" / "baseline" / f"no-duplicate-string{BASELINE_SUFFIX}"


def test_load_missing_baseline_is_empty(tmp_path: Path) -> None:
    assert load_baseline("nope", tmp_path) == set()


def test_establish_then_load_roundtrip(tmp_path: Path) -> None:
    written = establish_baseline("my-rule", {"src/x.py", "src/y.py"}, tmp_path)
    assert written.exists()
    assert load_baseline("my-rule", tmp_path) == {"src/x.py", "src/y.py"}


def test_establish_creates_baseline_dir(tmp_path: Path) -> None:
    assert not (tmp_path / ".architecture").exists()
    establish_baseline("r", [], tmp_path)
    assert (tmp_path / ".architecture" / "baseline").is_dir()


def test_establish_empty_writes_header_only(tmp_path: Path) -> None:
    establish_baseline("r", [], tmp_path)
    assert load_baseline("r", tmp_path) == set()


def test_render_reader_writer_agree(tmp_path: Path) -> None:
    establish_baseline("r", ["src/a.py"], tmp_path)
    raw = baseline_path("r", tmp_path).read_text()
    assert parse_baseline_text(raw) == load_baseline("r", tmp_path)
