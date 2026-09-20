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
    scan_text,
)

pytestmark = pytest.mark.unit

ROBOT = "\U0001f916"  # 🤖


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


# ── scan_text: the shared detector (hook + CI legs + file scan all key on it) ──


def test_scan_text_flags_coauthor_claude_trailer() -> None:
    hits = scan_text("feat: x\n\nCo-Authored-By: Claude <noreply@anthropic.com>")
    assert hits, "the Co-Authored-By: Claude trailer must be flagged"


def test_scan_text_flags_generated_with_claude_code() -> None:
    hits = scan_text(f"{ROBOT} Generated with [Claude Code](https://claude.com/claude-code)")
    assert hits


def test_scan_text_flags_anthropic_noreply_email() -> None:
    assert scan_text("Signed-off-by: bot <noreply@anthropic.com>")


def test_scan_text_flags_bare_robot_emoji() -> None:
    assert scan_text(f"nice work {ROBOT}")


def test_scan_text_is_provider_generic() -> None:
    # Cursor / Copilot co-author trailers are the same class of residue.
    assert scan_text("Co-authored-by: Cursor Agent <cursor@cursor.com>")


def test_scan_text_clean_text_passes() -> None:
    # A bare mention of the word "Anthropic" and a genuine HUMAN co-author must NOT flag.
    clean = (
        "This module talks to the Anthropic API.\n\n"
        "Co-Authored-By: Jane Doe <jane@example.com>\n"
        "Reviewed-by: Sam <sam@example.com>"
    )
    assert scan_text(clean) == []


def test_scan_text_reports_signature_names() -> None:
    hits = scan_text("Co-Authored-By: Claude <noreply@anthropic.com>")
    sigs = {h.signature for h in hits}
    assert "attribution_trailer" in sigs
    assert "anthropic_noreply" in sigs


# ── FitnessRule surface: file scan, baseline grandfathering (guard-forward) ──


# ── message-scan / strip CLI: the seam the commit-msg hook + CI leg consume ──


def test_strip_text_removes_trailer_and_credit_lines() -> None:
    from tc_fitness.core_checks.no_llm_attribution import strip_text

    msg = (
        "feat: do the thing\n\n"
        "body line\n"
        f"{ROBOT} Generated with [Claude Code](https://claude.com/claude-code)\n"
        "Co-Authored-By: Claude <noreply@anthropic.com>\n"
    )
    cleaned, stripped = strip_text(msg)
    assert len(stripped) == 2
    assert scan_text(cleaned) == []  # nothing left to flag
    assert "feat: do the thing" in cleaned and "body line" in cleaned


def test_strip_text_keeps_genuine_human_coauthor() -> None:
    from tc_fitness.core_checks.no_llm_attribution import strip_text

    msg = "fix: y\n\nCo-Authored-By: Jane Doe <jane@example.com>\n"
    cleaned, stripped = strip_text(msg)
    assert stripped == []
    assert "Jane Doe" in cleaned
