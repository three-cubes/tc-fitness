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
    NoLlmAttribution,
    build,
    main,
    scan_text,
    strip_text,
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
    msg = "fix: y\n\nCo-Authored-By: Jane Doe <jane@example.com>\n"
    cleaned, stripped = strip_text(msg)
    assert stripped == []
    assert "Jane Doe" in cleaned


def test_strip_text_preserves_multiple_trailing_newlines() -> None:
    msg = "feat: x\n\nCo-Authored-By: Claude <bot@example.com>\n\n"

    cleaned, dropped = strip_text(msg)

    assert dropped == ["Co-Authored-By: Claude <bot@example.com>"]
    assert cleaned == "feat: x\n\n"


def test_scan_file_reports_residue_and_clean_messages(tmp_path: Path) -> None:
    contaminated = _seed(tmp_path, "contaminated.txt", "Co-Authored-By: Claude <bot@example.com>\n")
    clean = _seed(tmp_path, "clean.txt", "Co-Authored-By: Jane <jane@example.com>\n")

    assert main(["--scan-file", str(contaminated)]) == 1
    assert main(["--scan-file", str(clean)]) == 0
    assert main(["--scan-file"]) == 2
    assert main(["--scan-file", str(tmp_path / "missing.txt")]) == 2


def test_strip_file_removes_whole_credit_lines_and_rejects_inline_residue(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "message.txt",
        "feat: x\nGenerated with Claude Code\ninline robot 🤖 stays\n",
    )

    assert main(["--strip-file", str(path)]) == 1
    assert path.read_text(encoding="utf-8") == "feat: x\ninline robot 🤖 stays\n"


def test_strip_file_with_only_removable_lines_passes_after_rewrite(tmp_path: Path) -> None:
    path = _seed(tmp_path, "message.txt", f"feat: x\n{ROBOT}\n")

    assert main(["--strip-file", str(path)]) == 0
    assert path.read_text(encoding="utf-8") == "feat: x\n"


def test_strip_file_leaves_non_strippable_residue_untouched(tmp_path: Path) -> None:
    original = "robot in a sentence 🤖\n"
    path = _seed(tmp_path, "message.txt", original)

    assert main(["--strip-file", str(path)]) == 1
    assert path.read_text(encoding="utf-8") == original


def test_file_rule_finds_attribution_and_ignores_unreadable_paths(tmp_path: Path) -> None:
    _seed(tmp_path, "src/bad.py", "Generated with Copilot\n")
    clean = _seed(tmp_path, "src/clean.py", "Mention Copilot as a product, not authorship.\n")
    binary = tmp_path / "src/binary.py"
    binary.write_bytes(b"Co-Authored-By: Claude\n\xff")
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert {str(path) for path in rule.collect_violations()} == {"src/bad.py"}
    assert rule.file_has_violation(clean) is False
    assert rule.file_has_violation(tmp_path / "src/missing.py") is False
    assert rule.file_has_violation(binary) is False
    assert isinstance(NoLlmAttribution.from_config({}), NoLlmAttribution)
