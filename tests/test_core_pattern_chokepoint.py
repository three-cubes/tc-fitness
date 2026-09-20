"""Tests for the pattern_chokepoint CORE check."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks.pattern_chokepoint import build, file_matches_any_pattern, main

pytestmark = pytest.mark.integration

_PATTERN = r"default_access_mode\s*="
_BAD = 'session = driver.session(default_access_mode="WRITE")\n'
_OK = "rows = client.cypher(query, params)\n"


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_flags_match(tmp_path: Path) -> None:
    p = _seed(tmp_path, "bad.py", _BAD)
    assert file_matches_any_pattern(p, patterns=(_PATTERN,)) is True


def test_detection_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "ok.py", _OK)
    assert file_matches_any_pattern(p, patterns=(_PATTERN,)) is False


def test_empty_patterns_flags_nothing(tmp_path: Path) -> None:
    p = _seed(tmp_path, "bad.py", _BAD)
    assert file_matches_any_pattern(p, patterns=()) is False


def test_unreadable_input_is_not_reported_as_a_pattern_match(tmp_path: Path) -> None:
    assert file_matches_any_pattern(tmp_path, patterns=(_PATTERN,)) is False


def test_no_patterns_configured_is_clean(tmp_path: Path) -> None:
    """A consumer that configures no patterns flags nothing (safe default)."""
    _seed(tmp_path, "src/bad.py", _BAD)
    rule = build({"roots": ["src"]}, repo_root=tmp_path)
    assert rule.collect_violations() == set()


def test_pattern_outside_chokepoint_is_flagged(tmp_path: Path) -> None:
    """The pattern is forbidden outside the chokepoint (exempt_files)."""
    _seed(tmp_path, "src/drain.py", _BAD)
    _seed(tmp_path, "src/client.py", _BAD)  # the chokepoint — legitimate here
    rule = build(
        {"roots": ["src"], "patterns": [_PATTERN], "exempt_files": ["src/client.py"]},
        repo_root=tmp_path,
    )
    violations = rule.collect_violations()
    assert Path("src/drain.py") in violations
    assert Path("src/client.py") not in violations


def test_chokepoint_file_alone_is_clean(tmp_path: Path) -> None:
    """When the pattern lives only at its chokepoint, the rule is green."""
    _seed(tmp_path, "src/client.py", _BAD)
    rule = build(
        {"roots": ["src"], "patterns": [_PATTERN], "exempt_files": ["src/client.py"]},
        repo_root=tmp_path,
    )
    assert rule.collect_violations() == set()


def test_multiple_patterns_any_match_flags(tmp_path: Path) -> None:
    _seed(tmp_path, "src/a.py", "x = _is_write_query(q)\n")
    rule = build(
        {"roots": ["src"], "patterns": [_PATTERN, r"_is_write_query"], "exempt_files": ["src/client.py"]},
        repo_root=tmp_path,
    )
    assert Path("src/a.py") in rule.collect_violations()


def test_module_cli_runs_the_real_hard_gate(tmp_path: Path) -> None:
    assert main(["--repo-root", str(tmp_path)]) == 0


def test_python_module_entrypoint_runs_the_real_hard_gate(tmp_path: Path) -> None:
    previous_argv = sys.argv
    sys.argv = ["pattern_chokepoint", "--repo-root", str(tmp_path)]
    try:
        with pytest.raises(SystemExit) as exc:
            runpy.run_path(
                str(Path(__file__).parents[1] / "src/tc_fitness/core_checks/pattern_chokepoint.py"),
                run_name="__main__",
            )
    finally:
        sys.argv = previous_argv

    assert exc.value.code == 0
