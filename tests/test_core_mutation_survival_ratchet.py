"""Tests for the CORE check mutation_survival_ratchet (file-shape scope, v0.6.0)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tc_fitness.core_checks.mutation_survival_ratchet import (
    build,
    report_is_malformed,
)

pytestmark = pytest.mark.integration

_VALID = '{"schema_version": 1, "packages": {"pkg": {"survived": 0, "killed": 9}}}'
_BAD_VERSION = '{"schema_version": 2, "packages": {}}'
_BAD_PACKAGES = '{"schema_version": 1, "packages": []}'
_BAD_JSON = "{not json"


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_valid_report_not_malformed(tmp_path: Path) -> None:
    p = _seed(tmp_path, "r.json", _VALID)
    assert report_is_malformed(p) is False


def test_bad_version_malformed(tmp_path: Path) -> None:
    p = _seed(tmp_path, "r.json", _BAD_VERSION)
    assert report_is_malformed(p) is True


def test_bad_packages_malformed(tmp_path: Path) -> None:
    p = _seed(tmp_path, "r.json", _BAD_PACKAGES)
    assert report_is_malformed(p) is True


def test_missing_packages_object_is_malformed(tmp_path: Path) -> None:
    p = _seed(tmp_path, "r.json", '{"schema_version": 1}')

    assert report_is_malformed(p) is True


@pytest.mark.parametrize("body", ["[]", "null", "\xff"])
def test_non_object_or_non_utf8_report_is_malformed(tmp_path: Path, body: str) -> None:
    p = tmp_path / "r.json"
    p.write_bytes(body.encode("utf-8", errors="surrogateescape"))

    assert report_is_malformed(p) is True


def test_bad_json_malformed(tmp_path: Path) -> None:
    p = _seed(tmp_path, "r.json", _BAD_JSON)
    assert report_is_malformed(p) is True


def test_absent_report_not_judged_by_helper(tmp_path: Path) -> None:
    assert report_is_malformed(tmp_path / "absent.json") is False


def test_missing_baseline_is_violation(tmp_path: Path) -> None:
    rule = build({"baseline_report": "base.json", "current_report": "cur.json"}, repo_root=tmp_path)
    assert rule.run() == 1


@pytest.mark.parametrize("value", [True, False, []])
def test_allow_missing_current_option_is_rejected(tmp_path: Path, value: object) -> None:
    _seed(tmp_path, "base.json", _VALID)
    with pytest.raises(ValueError, match="allow_missing_current"):
        build(
            {"baseline_report": "base.json", "current_report": "cur.json", "allow_missing_current": value},
            repo_root=tmp_path,
        )


def test_missing_current_is_violation(tmp_path: Path) -> None:
    _seed(tmp_path, "base.json", _VALID)
    rule = build(
        {"baseline_report": "base.json", "current_report": "cur.json"},
        repo_root=tmp_path,
    )
    assert rule.run() == 1


def test_malformed_current_is_violation(tmp_path: Path) -> None:
    _seed(tmp_path, "base.json", _VALID)
    _seed(tmp_path, "cur.json", _BAD_VERSION)
    rule = build({"baseline_report": "base.json", "current_report": "cur.json"}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"cur.json"}


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.mutation_survival_ratchet as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(text)
    docstring_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                docstring_ids.add(id(first.value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstring_ids:
            lowered = node.value.lower()
            for tok in ("kairix", "tc-agent-zone", "agent-zone", "kata"):
                assert tok not in lowered, f"repo identity leaked in a code literal: {tok}"
