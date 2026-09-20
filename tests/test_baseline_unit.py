"""Tests for the per-file baseline I/O (v0.6.0)."""

from __future__ import annotations

import pytest

from tc_fitness.baseline import (
    parse_baseline_text,
    render_baseline,
)

pytestmark = pytest.mark.unit


def test_parse_skips_comments_and_blanks() -> None:
    text = "# header\n\nsrc/a.py\n  src/b.py  \n# trailing comment\n"
    assert parse_baseline_text(text) == {"src/a.py", "src/b.py"}


def test_render_has_mandatory_header_and_shrink_contract() -> None:
    text = render_baseline("my-rule", ["src/b.py", "src/a.py", "src/a.py"])
    assert text.startswith("# Baseline for fitness check: my-rule")
    assert "may only SHRINK" in text
    # entries de-duplicated + sorted
    assert text.rstrip().endswith("src/a.py\nsrc/b.py")
