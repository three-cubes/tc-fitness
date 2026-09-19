"""Tests for the CORE check harness_canon_reference (fleet harness canon)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tc_fitness.core_checks.harness_canon_reference import (
    banner_present,
    has_canon_reference,
    normalise_banner,
)

pytestmark = pytest.mark.unit

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


# --------------------------------------------------------------------------- #
# Reference arm.
# --------------------------------------------------------------------------- #


def test_banner_present_empty_pin_is_present() -> None:
    # An empty pin has nothing to drift from, so drift never trips on it.
    assert banner_present([], "") is True


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


# --------------------------------------------------------------------------- #
# CLI + engine-conformance parity with the sibling CORE checks.
# --------------------------------------------------------------------------- #
