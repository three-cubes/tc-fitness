"""Tests for the CORE check license_present (v0.6.0 security-freshness batch)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness.core_checks.license_present import (
    DEFAULT_MARKERS,
    build,
    file_missing_license,
)

pytestmark = pytest.mark.integration


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_missing_header_flagged(tmp_path: Path) -> None:
    p = _seed(tmp_path, "m.py", "def f():\n    return 1\n")
    assert file_missing_license(p, markers=DEFAULT_MARKERS, header_lines=20) is True


def test_spdx_header_is_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "m.py", "# SPDX-License-Identifier: MIT\ndef f():\n    return 1\n")
    assert file_missing_license(p, markers=DEFAULT_MARKERS, header_lines=20) is False


def test_copyright_header_is_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "m.py", "# Copyright 2026 Someone\ndef f():\n    return 1\n")
    assert file_missing_license(p, markers=DEFAULT_MARKERS, header_lines=20) is False


def test_marker_below_window_still_flagged(tmp_path: Path) -> None:
    body = "\n" * 30 + "# SPDX-License-Identifier: MIT\n"
    p = _seed(tmp_path, "m.py", body)
    assert file_missing_license(p, markers=DEFAULT_MARKERS, header_lines=20) is True


def test_invalid_utf8_in_configured_python_file_is_not_clean(tmp_path: Path) -> None:
    source = tmp_path / "src" / "broken.py"
    source.parent.mkdir()
    source.write_bytes(b"# SPDX-License-Identifier: MIT\n" + bytes([255]) + b"\n")
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.run() == 1


def test_custom_markers_via_config(tmp_path: Path) -> None:
    rule = build({"roots": ["."], "markers": ["MY-LICENSE-TAG"]}, repo_root=tmp_path)
    ok = _seed(tmp_path, "ok.py", "# MY-LICENSE-TAG\nx = 1\n")
    bad = _seed(tmp_path, "bad.py", "# SPDX-License-Identifier: MIT\nx = 1\n")
    assert rule.file_has_violation(ok) is False
    assert rule.file_has_violation(bad) is True


def test_configured_header_window_controls_visibility(tmp_path: Path) -> None:
    rule = build({"roots": ["src"], "header_lines": 1}, repo_root=tmp_path)
    _seed(tmp_path, "src/visible.py", "# SPDX-License-Identifier: MIT\nx = 1\n")
    _seed(tmp_path, "src/late.py", "# no license here\n# Copyright 2026\n")

    assert {str(path) for path in rule.collect_violations()} == {"src/late.py"}
