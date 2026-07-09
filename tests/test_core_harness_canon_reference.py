"""Tests for the CORE check harness_canon_reference (fleet harness canon)."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from tc_fitness.core_checks.harness_canon_reference import (
    HarnessCanonReference,
    banner_present,
    build,
    has_canon_reference,
    main,
    missing_required_groups,
    normalise_banner,
)

# A harness snippet that satisfies the reference arm: it carries the canon
# marker AND a link matching the default governance/STANDARDS reference regex.
_CANON_REF = (
    "## Canonical standards\n"
    "Read the central STANDARDS index at governance/STANDARDS.md first — it is\n"
    "the index over everything. Do not fork a parallel standard.\n"
)

_PRODUCT_FILES = (
    "CLAUDE.md",
    "AGENTS.md",
    "RESOLVER.md",
    "ETHOS.md",
    "SCORECARD.md",
    "CONTRIBUTING.md",
)


def _write(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _full_product_harness(tmp_path: Path) -> None:
    """Every product entrypoint present; CLAUDE.md carries the canon reference."""
    for name in _PRODUCT_FILES:
        _write(tmp_path, name, _CANON_REF if name == "CLAUDE.md" else f"# {name}\n")


# --------------------------------------------------------------------------- #
# Pure-helper unit tests (the detection cores).
# --------------------------------------------------------------------------- #


def test_missing_required_groups_any_of_satisfied(tmp_path: Path) -> None:
    _write(tmp_path, "AGENTS.md", "# AGENTS\n")
    # Group {CLAUDE.md or AGENTS.md} is satisfied by AGENTS.md alone.
    assert missing_required_groups(tmp_path, [frozenset({"CLAUDE.md", "AGENTS.md"})]) == []


def test_missing_required_groups_singletons_report_absent(tmp_path: Path) -> None:
    _write(tmp_path, "CLAUDE.md", "# CLAUDE\n")
    groups = [frozenset({"CLAUDE.md"}), frozenset({"AGENTS.md"})]
    assert missing_required_groups(tmp_path, groups) == ["AGENTS.md"]


def test_has_canon_reference_requires_both_in_one_file() -> None:
    pattern = re.compile(r"governance/STANDARDS")
    assert has_canon_reference([_CANON_REF], marker="Canonical standards", ref_pattern=pattern)
    # Marker in one file, link in another → not a proof that a file names canon.
    split = ["## Canonical standards\n", "see governance/STANDARDS.md\n"]
    assert not has_canon_reference(split, marker="Canonical standards", ref_pattern=pattern)


def test_normalise_and_banner_present_ignore_layout() -> None:
    pinned = "Canonical standards\n   Read governance/STANDARDS.md first.\n"
    reflowed = "\n\n## Canonical standards\n\nRead governance/STANDARDS.md first.\n\n"
    assert normalise_banner(pinned) in normalise_banner(reflowed)
    assert banner_present([reflowed], pinned)
    assert not banner_present(["nothing pinned here"], pinned)


# --------------------------------------------------------------------------- #
# Presence arm.
# --------------------------------------------------------------------------- #


def test_pass_full_product_harness_with_reference(tmp_path: Path) -> None:
    _full_product_harness(tmp_path)
    assert build({}, repo_root=tmp_path).run() == 0


def test_fail_on_missing_file(tmp_path: Path) -> None:
    _full_product_harness(tmp_path)
    (tmp_path / "RESOLVER.md").unlink()  # drop one product entrypoint
    assert build({}, repo_root=tmp_path).run() == 1


def test_repo_type_core_relaxation(tmp_path: Path) -> None:
    # A core/framework repo needs only AGENTS.md — carrying the reference there
    # passes even though CLAUDE.md/RESOLVER.md/ETHOS.md/etc. are absent.
    _write(tmp_path, "AGENTS.md", _CANON_REF)
    assert build({"repo_type": "core"}, repo_root=tmp_path).run() == 0


def test_repo_type_core_still_requires_agents(tmp_path: Path) -> None:
    _write(tmp_path, "CLAUDE.md", _CANON_REF)  # present, but not AGENTS.md
    assert build({"repo_type": "core"}, repo_root=tmp_path).run() == 1


def test_required_files_override_is_any_of(tmp_path: Path) -> None:
    # Explicit list is satisfied when at least one member exists.
    _write(tmp_path, "AGENTS.md", _CANON_REF)
    cfg = {"required_files": ["CLAUDE.md", "AGENTS.md"]}
    assert build(cfg, repo_root=tmp_path).run() == 0


# --------------------------------------------------------------------------- #
# Reference arm.
# --------------------------------------------------------------------------- #


def test_fail_on_missing_reference(tmp_path: Path) -> None:
    # Every product file present, but none names the canonical-standards index.
    for name in _PRODUCT_FILES:
        _write(tmp_path, name, f"# {name}\nno canon reference here\n")
    assert build({}, repo_root=tmp_path).run() == 1


def test_invalid_reference_pattern_fails_actionably(tmp_path: Path) -> None:
    _write(tmp_path, "AGENTS.md", _CANON_REF)
    cfg = {"repo_type": "core", "standards_ref_pattern": "["}  # not a valid regex
    assert build(cfg, repo_root=tmp_path).run() == 1


def test_banner_present_empty_pin_is_present() -> None:
    # An empty pin has nothing to drift from, so drift never trips on it.
    assert banner_present([], "") is True


def test_reference_pattern_is_config_driven(tmp_path: Path) -> None:
    body = "## House rules\nsee docs/local-canon.md\n"
    _write(tmp_path, "AGENTS.md", body)
    cfg = {
        "repo_type": "core",
        "banner_marker": "House rules",
        "standards_ref_pattern": r"docs/local-canon",
    }
    assert build(cfg, repo_root=tmp_path).run() == 0


# --------------------------------------------------------------------------- #
# Drift arm (opt-in via banner_path).
# --------------------------------------------------------------------------- #

_PINNED_BANNER = (
    "Canonical standards\n"
    "Read the central STANDARDS index at governance/STANDARDS.md first.\n"
    "Do not fork a parallel standard — converge up to the one canon.\n"
)


def _drift_cfg(banner_rel: str) -> dict[str, object]:
    # Isolate the drift arm: presence needs only CLAUDE.md, reference lives in it.
    return {"required_files": ["CLAUDE.md"], "banner_path": banner_rel}


def test_drift_pass_when_banner_inlined(tmp_path: Path) -> None:
    _write(tmp_path, "docs/canon-banner.md", _PINNED_BANNER)
    _write(tmp_path, "CLAUDE.md", f"# CLAUDE\n\n{_PINNED_BANNER}\nmore local guidance\n")
    assert build(_drift_cfg("docs/canon-banner.md"), repo_root=tmp_path).run() == 0


def test_drift_fail_when_banner_modified(tmp_path: Path) -> None:
    _write(tmp_path, "docs/canon-banner.md", _PINNED_BANNER)
    # Harness inlines a banner that DROPS the pinned "do not fork" line: the
    # reference arm still passes (marker + link present) but drift fails.
    truncated = "Canonical standards\nRead the central STANDARDS index at governance/STANDARDS.md first.\n"
    _write(tmp_path, "CLAUDE.md", f"# CLAUDE\n\n{truncated}\n")
    assert build(_drift_cfg("docs/canon-banner.md"), repo_root=tmp_path).run() == 1


def test_drift_arm_skipped_when_banner_path_unset(tmp_path: Path) -> None:
    # No banner_path → drift arm never runs even if no banner is inlined.
    _write(tmp_path, "CLAUDE.md", _CANON_REF)
    assert build({"required_files": ["CLAUDE.md"]}, repo_root=tmp_path).run() == 0


def test_drift_fail_when_pinned_banner_missing(tmp_path: Path) -> None:
    _write(tmp_path, "CLAUDE.md", _CANON_REF)
    cfg = {"required_files": ["CLAUDE.md"], "banner_path": "docs/does-not-exist.md"}
    assert build(cfg, repo_root=tmp_path).run() == 1


# --------------------------------------------------------------------------- #
# CLI + engine-conformance parity with the sibling CORE checks.
# --------------------------------------------------------------------------- #


def test_main_establish_baseline_mode(tmp_path: Path) -> None:
    _full_product_harness(tmp_path)
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / ".architecture" / "baseline" / "harness-canon-reference-files.txt").exists()


def test_from_config_binds_all_knobs(tmp_path: Path) -> None:
    rule = HarnessCanonReference.from_config(
        {
            "repo_type": "core",
            "banner_marker": "House rules",
            "standards_ref_pattern": r"docs/canon",
            "banner_path": "docs/banner.md",
            "required_files": ["AGENTS.md"],
        },
        repo_root=tmp_path,
    )
    assert rule.repo_type == "core"
    assert rule.banner_marker == "House rules"
    assert rule.standards_ref_pattern == r"docs/canon"
    assert rule.banner_path == "docs/banner.md"
    assert rule.required_files == ("AGENTS.md",)


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.harness_canon_reference as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(text)
    docstring_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None and node.body:
                first = node.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                    docstring_ids.add(id(first.value))
    repo_tokens = ("kairix", "tc-agent-zone", "agent-zone", "kata")
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if id(node) in docstring_ids:
                continue
            lowered = node.value.lower()
            for tok in repo_tokens:
                assert tok not in lowered, f"repo identity leaked in a code literal: {tok}"
