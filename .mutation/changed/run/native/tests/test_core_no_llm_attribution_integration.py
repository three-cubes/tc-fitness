"""Tests for the CORE check no_llm_attribution (Autonomous Delivery Platform SP-A / SGO-156).

The check has two surfaces that share ONE detector (:func:`scan_text`):
* a :class:`FitnessRule` that scans in-repo files for LLM-attribution residue, and
* the standalone ``scan_text`` helper reused by the commit-msg strip hook (SGO-159)
  and the CI trailer-reject leg (SGO-160) to scan commit messages + PR title/body.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tc_fitness.core_checks.no_llm_attribution import (
    build,
    main,
    scan_text,
)

pytestmark = pytest.mark.integration

ROBOT = "\U0001f916"  # 🤖


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


# ── scan_text: the shared detector (hook + CI legs + file scan all key on it) ──


# ── FitnessRule surface: file scan, baseline grandfathering (guard-forward) ──


def test_file_has_violation_true_and_false(tmp_path: Path) -> None:
    rule = build({"roots": ["."], "extensions": [".py", ".md"]}, repo_root=tmp_path)
    dirty = _seed(tmp_path, "src/a.py", f"# {ROBOT} Generated with Claude Code\nx = 1\n")
    clean = _seed(tmp_path, "src/b.py", "x = 1  # ordinary code\n")
    assert rule.file_has_violation(dirty) is True
    assert rule.file_has_violation(clean) is False


def test_functional_claude_string_is_not_authorship(tmp_path: Path) -> None:
    # A functional in-source string that merely names the tool (no attribution
    # signature) must NOT be flagged — only attribution residue is.
    rule = build({"roots": ["."], "extensions": [".py"]}, repo_root=tmp_path)
    p = _seed(tmp_path, "src/c.py", 'PREFIX = "Claude Code sub-agent worktrees"\n')
    assert rule.file_has_violation(p) is False


# ── message-scan / strip CLI: the seam the commit-msg hook + CI leg consume ──


def test_main_scan_file_flags_dirty_and_passes_clean(tmp_path: Path) -> None:
    dirty = tmp_path / "MSG_DIRTY"
    dirty.write_text("feat: x\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n", encoding="utf-8")
    assert main(["--scan-file", str(dirty)]) == 1
    # --scan-file does NOT modify the file (CI must not rewrite history).
    assert "Co-Authored-By: Claude" in dirty.read_text(encoding="utf-8")

    clean = tmp_path / "MSG_CLEAN"
    clean.write_text("feat: x\n\nplain body\n", encoding="utf-8")
    assert main(["--scan-file", str(clean)]) == 0


def test_main_strip_file_cleans_then_passes(tmp_path: Path) -> None:
    msg = tmp_path / "COMMIT_EDITMSG"
    msg.write_text(
        f"feat: x\n\nbody\n{ROBOT} Generated with Claude Code\nCo-Authored-By: Claude <noreply@anthropic.com>\n",
        encoding="utf-8",
    )
    assert main(["--strip-file", str(msg)]) == 0
    after = msg.read_text(encoding="utf-8")
    assert scan_text(after) == []
    assert "feat: x" in after and "body" in after


def test_main_strip_file_rejects_nonstrippable_inline_residue(tmp_path: Path) -> None:
    # A robot emoji embedded mid-line is not a whole strippable line → hard-reject.
    msg = tmp_path / "COMMIT_EDITMSG"
    msg.write_text(f"feat: shipped it {ROBOT} finally\n", encoding="utf-8")
    assert main(["--strip-file", str(msg)]) == 1
