"""Tests for the CORE check adr_number_unique (v0.6.0 security-freshness batch)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tc_fitness.core_checks.adr_number_unique import (
    DEFAULT_RECORD_PATTERN,
    build,
    find_collisions,
)

pytestmark = pytest.mark.integration

_PATTERN = re.compile(DEFAULT_RECORD_PATTERN)


def _seed(tmp_path: Path, rel: str, body: str = "x\n") -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_collision_detected(tmp_path: Path) -> None:
    d = tmp_path / "docs" / "decisions"
    _seed(tmp_path, "docs/decisions/ADR-041-foo.md")
    _seed(tmp_path, "docs/decisions/ADR-041-bar.md")
    collisions = find_collisions(d, pattern=_PATTERN)
    assert set(collisions) == {"041"}
    assert len(collisions["041"]) == 2


def test_unique_numbers_no_collision(tmp_path: Path) -> None:
    d = tmp_path / "docs" / "decisions"
    _seed(tmp_path, "docs/decisions/ADR-041-foo.md")
    _seed(tmp_path, "docs/decisions/ADR-042-bar.md")
    assert find_collisions(d, pattern=_PATTERN) == {}


def test_missing_record_directory_has_no_collisions(tmp_path: Path) -> None:
    assert find_collisions(tmp_path / "not-created", pattern=_PATTERN) == {}


def test_only_matching_files_participate_in_collision_groups(tmp_path: Path) -> None:
    records = tmp_path / "docs" / "decisions"
    _seed(tmp_path, "docs/decisions/ADR-041-directory.md/child.txt")
    _seed(tmp_path, "docs/decisions/ADR-041-not-a-record.txt")
    _seed(tmp_path, "docs/decisions/ADR-042-only-one.md")

    assert find_collisions(records, pattern=_PATTERN) == {}


def test_collision_paths_are_sorted_for_stable_output(tmp_path: Path) -> None:
    records = tmp_path / "docs" / "decisions"
    _seed(tmp_path, "docs/decisions/ADR-041-zulu.md")
    _seed(tmp_path, "docs/decisions/ADR-041-alpha.md")

    assert find_collisions(records, pattern=_PATTERN)["041"] == [
        records / "ADR-041-alpha.md",
        records / "ADR-041-zulu.md",
    ]


def test_invalid_consumer_pattern_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(re.error):
        build({"record_pattern": "("}, repo_root=tmp_path)


def test_collect_violations_returns_colliding_files(tmp_path: Path) -> None:
    _seed(tmp_path, "docs/decisions/ADR-041-foo.md")
    _seed(tmp_path, "docs/decisions/ADR-041-bar.md")
    _seed(tmp_path, "docs/decisions/ADR-042-ok.md")
    rule = build({}, repo_root=tmp_path)
    rels = {str(p) for p in rule.collect_violations()}
    assert rels == {"docs/decisions/ADR-041-foo.md", "docs/decisions/ADR-041-bar.md"}


def test_single_file_predicate_is_false_for_cross_file_invariant(tmp_path: Path) -> None:
    record = _seed(tmp_path, "docs/decisions/ADR-041-only.md")

    assert build({}, repo_root=tmp_path).file_has_violation(record) is False


def test_custom_dir_and_pattern_via_config(tmp_path: Path) -> None:
    _seed(tmp_path, "rfc/RFC-7-a.md")
    _seed(tmp_path, "rfc/RFC-7-b.md")
    rule = build({"record_dir": "rfc", "record_pattern": r"^RFC-(\d+)-.+\.md$"}, repo_root=tmp_path)
    assert len(rule.collect_violations()) == 2
