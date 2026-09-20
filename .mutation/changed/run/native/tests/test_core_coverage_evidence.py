"""Behavioural controls for Cobertura evidence parsing and path admission."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from tc_fitness.core_checks._coverage_evidence import (
    CoverageCounts,
    count_class_coverage,
    coverage_integer,
    resolve_coverage_filename,
    validate_coverage_rate,
)

pytestmark = pytest.mark.contract


def _source(tmp_path: Path, relative: str = "src/pkg/example.py") -> Path:
    source = tmp_path / relative
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("first = 1\nsecond = 2\n", encoding="utf-8")
    return source


def _line(**attributes: str) -> ET.Element:
    return ET.Element("line", attributes)


def _class(*lines: ET.Element, line_rate: str = "1", branch_rate: str = "1") -> ET.Element:
    element = ET.Element("class", {"line-rate": line_rate, "branch-rate": branch_rate})
    details = ET.SubElement(element, "lines")
    details.extend(lines)
    return element


@pytest.mark.parametrize("value", ["0", "1", "24", "9000"])
def test_coverage_integer_accepts_explicit_non_negative_counts(value: str) -> None:
    assert coverage_integer(value) == int(value)


def test_coverage_counts_treats_empty_opportunity_sets_as_complete() -> None:
    assert CoverageCounts(0, 0, 0, 0).line_pct == 100
    assert CoverageCounts(1, 1, 0, 0).branch_pct == 100


@pytest.mark.parametrize("value", [None, "", "01", "-1", "+1", "1.0", "one"])
def test_coverage_integer_rejects_non_canonical_counts(value: str | None) -> None:
    with pytest.raises(ValueError, match="non-negative"):
        coverage_integer(value)


@pytest.mark.parametrize(
    ("rate", "covered", "total"),
    [("1", 1, 1), ("0.5", 1, 2), (".3333", 1, 3), ("1", 0, 0)],
)
def test_validate_coverage_rate_accepts_cobertura_summary(rate: str, covered: int, total: int) -> None:
    validate_coverage_rate(rate, covered, total)


@pytest.mark.parametrize(
    ("rate", "covered", "total", "message"),
    [
        (None, 1, 1, "missing"),
        ("nan", 1, 1, "finite"),
        ("1.1", 1, 1, "finite"),
        ("0", 0, 0, "zero-opportunity"),
        ("0.25", 1, 2, "disagrees"),
    ],
)
def test_validate_coverage_rate_rejects_unbound_summary(
    rate: str | None, covered: int, total: int, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        validate_coverage_rate(rate, covered, total)


def test_count_class_coverage_counts_real_line_and_branch_detail(tmp_path: Path) -> None:
    source = _source(tmp_path)
    element = _class(
        _line(number="1", hits="1", branch="true", **{"condition-coverage": "50% (1/2)"}),
        _line(number="2", hits="0", branch="false"),
        line_rate="0.5",
        branch_rate="0.5",
    )
    assert count_class_coverage(element, source) == CoverageCounts(2, 1, 2, 1)


@pytest.mark.parametrize(
    ("element", "message"),
    [
        (_class(), "missing coverage detail for non-empty source"),
        (_class(ET.Element("other", {"number": "1", "hits": "1"})), "unexpected coverage line detail"),
        (_class(_line(number="3", hits="1")), "outside source"),
        (_class(_line(number="1", hits="1"), _line(number="1", hits="1")), "duplicate"),
        (_class(_line(number="1", hits="1", branch="maybe")), "branch flag"),
        (_class(_line(number="1", hits="1", **{"condition-coverage": "100% (1/1)"})), "without a branch"),
        (_class(_line(number="1", hits="1", branch="true")), "malformed"),
        (
            _class(_line(number="1", hits="0", branch="true", **{"condition-coverage": "50% (1/2)"})),
            "invalid detailed",
        ),
        (
            _class(_line(number="1", hits="1", branch="true", **{"condition-coverage": "0% (1/2)"})),
            "percentage",
        ),
    ],
)
def test_count_class_coverage_rejects_invalid_evidence(
    tmp_path: Path, element: ET.Element, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        count_class_coverage(element, _source(tmp_path))


def test_count_class_coverage_rejects_missing_source(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="source file is missing"):
        count_class_coverage(_class(_line(number="1", hits="1")), tmp_path / "missing.py")


def test_count_class_coverage_requires_a_lines_element(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="missing coverage line detail"):
        count_class_coverage(ET.Element("class", {"line-rate": "1", "branch-rate": "1"}), _source(tmp_path))


def test_resolve_coverage_filename_selects_real_repository_source(tmp_path: Path) -> None:
    _source(tmp_path)
    assert resolve_coverage_filename("pkg/example.py", ["src"], repo_root=tmp_path) == "src/pkg/example.py"
    assert (
        resolve_coverage_filename(str(tmp_path / "src/pkg/example.py"), [], repo_root=tmp_path)
        == "src/pkg/example.py"
    )


@pytest.mark.parametrize(
    ("filename", "roots", "expected"),
    [
        ("pkg/example.py", [], "pkg/example.py"),
        ("pkg/example.py", ["src"], "src/pkg/example.py"),
        ("src/pkg/example.py", ["src"], "src/pkg/example.py"),
        ("pkg/example.py", ["/absolute/src"], "/absolute/src/pkg/example.py"),
    ],
)
def test_resolve_coverage_filename_has_deterministic_synthetic_fallback(
    filename: str, roots: list[str], expected: str
) -> None:
    assert resolve_coverage_filename(filename, roots, repo_root=None) == expected


def test_resolve_coverage_filename_handles_absolute_and_rootless_synthetic_reports() -> None:
    assert resolve_coverage_filename("/tmp/example.py", ["src"], repo_root=None) == "/tmp/example.py"
    assert resolve_coverage_filename("example.py", [], repo_root=None) == "example.py"


def test_resolve_coverage_filename_resolves_unmaterialised_repository_roots(tmp_path: Path) -> None:
    assert resolve_coverage_filename("unknown.py", [], repo_root=tmp_path) == "unknown.py"
    assert (
        resolve_coverage_filename("src/pkg/example.py", ["src", "lib"], repo_root=tmp_path)
        == "src/pkg/example.py"
    )
    assert resolve_coverage_filename("pkg/example.py", ["src"], repo_root=tmp_path) == "src/pkg/example.py"
    with pytest.raises(ValueError, match="ambiguous"):
        resolve_coverage_filename("pkg/example.py", ["src", "lib"], repo_root=tmp_path)


def test_resolve_coverage_filename_rejects_ambiguous_or_escaping_paths(tmp_path: Path) -> None:
    _source(tmp_path, "src/pkg/example.py")
    _source(tmp_path, "lib/pkg/example.py")
    with pytest.raises(ValueError, match="multiple"):
        resolve_coverage_filename("pkg/example.py", ["src", "lib"], repo_root=tmp_path)
    with pytest.raises(ValueError, match="outside"):
        resolve_coverage_filename(str(tmp_path.parent / "outside.py"), [], repo_root=tmp_path)
    with pytest.raises(ValueError, match="ambiguous"):
        resolve_coverage_filename("pkg/example.py", ["src", "lib"], repo_root=None)
