"""Tests for the CORE check coverage_includes_branches (v0.6.0)."""

from __future__ import annotations

import ast
import os
import subprocess
import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path

import pytest

from tc_fitness.core_checks.coverage_includes_branches import (
    build,
    main,
    report_lacks_branches,
)

pytestmark = pytest.mark.integration


def _seed(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "coverage.xml"
    p.write_text(body, encoding="utf-8")
    return p


_BRANCH_AWARE = '<coverage line-rate="0.9" branch-rate="0.38" branches-valid="3070" branches-covered="1196"/>'
_LINES_ONLY = '<coverage line-rate="0.9" branch-rate="0" branches-valid="0"/>'


def test_lines_only_report_violates(tmp_path: Path) -> None:
    p = _seed(tmp_path, _LINES_ONLY)
    assert report_lacks_branches(p) is True


def test_branch_aware_report_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, _BRANCH_AWARE)
    assert report_lacks_branches(p) is False


def test_standard_library_parser_observes_the_real_branch_report(tmp_path: Path) -> None:
    p = _seed(tmp_path, _BRANCH_AWARE)

    assert report_lacks_branches(p, element_tree=ElementTree) is False


def test_missing_report_is_a_violation(tmp_path: Path) -> None:
    assert report_lacks_branches(tmp_path / "absent.xml") is True


def test_rule_flags_lines_only(tmp_path: Path) -> None:
    _seed(tmp_path, _LINES_ONLY)
    rule = build({}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"coverage.xml"}


def test_rule_clean_on_branch_aware(tmp_path: Path) -> None:
    _seed(tmp_path, _BRANCH_AWARE)
    assert build({}, repo_root=tmp_path).collect_violations() == set()


def test_report_path_is_config_driven(tmp_path: Path) -> None:
    nested = tmp_path / "build" / "cov.xml"
    nested.parent.mkdir(parents=True)
    nested.write_text(_LINES_ONLY, encoding="utf-8")
    rule = build({"coverage_report": "build/cov.xml"}, repo_root=tmp_path)
    assert rule.run() == 1


def test_run_fails_when_no_report(tmp_path: Path) -> None:
    rule = build({}, repo_root=tmp_path)
    assert rule.collect_violations() == {Path("coverage.xml")}
    assert rule.run() == 1


def test_unsafe_xml_rejected(tmp_path: Path) -> None:
    p = _seed(tmp_path, "<!ENTITY x>\n<coverage/>")
    try:
        report_lacks_branches(p)
    except ValueError as exc:
        assert "DTD/entity" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected ValueError for ENTITY declaration")


def test_main_runs(tmp_path: Path) -> None:
    _seed(tmp_path, _BRANCH_AWARE)
    assert main(["--repo-root", str(tmp_path)]) == 0


def test_python_module_entrypoint_uses_stdlib_xml_when_site_packages_are_disabled(tmp_path: Path) -> None:
    _seed(tmp_path, _BRANCH_AWARE)
    source_root = Path(__file__).parents[1] / "src"
    result = subprocess.run(
        [
            sys.executable,
            "-S",
            "-m",
            "tc_fitness.core_checks.coverage_includes_branches",
            "--repo-root",
            str(tmp_path),
        ],
        capture_output=True,
        check=False,
        text=True,
        env={**os.environ, "PYTHONPATH": str(source_root)},
    )

    assert result.returncode == 0, result.stderr
    assert "coverage-includes-branches" in result.stdout


def test_python_module_entrypoint_reports_its_check_result(tmp_path: Path) -> None:
    _seed(tmp_path, _BRANCH_AWARE)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tc_fitness.core_checks.coverage_includes_branches",
            "--repo-root",
            str(tmp_path),
        ],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "coverage-includes-branches" in result.stdout


def test_report_path_can_be_bound_to_a_real_process_environment_value(tmp_path: Path) -> None:
    report = _seed(tmp_path, _BRANCH_AWARE)
    program = (
        "import os, sys; from pathlib import Path; "
        "from tc_fitness.core_checks.coverage_includes_branches import build; "
        "os.environ['FITNESS_COVERAGE_REPORT'] = sys.argv[1]; "
        "raise SystemExit(build({'coverage_report': 'env:FITNESS_COVERAGE_REPORT'}, "
        "repo_root=Path(sys.argv[2])).run())"
    )
    result = subprocess.run(
        [sys.executable, "-c", program, str(report), str(tmp_path)],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "coverage-includes-branches" in result.stdout


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.coverage_includes_branches as mod

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


def test_an_external_coverage_report_is_keyed_inside_the_repository(tmp_path: Path) -> None:
    """An external report is legitimate; its finding still has to relativise."""
    external = tmp_path / "evidence" / "coverage.xml"
    external.parent.mkdir()
    repo = tmp_path / "repo"
    repo.mkdir()
    rule = build({"coverage_report": str(external)}, repo_root=repo)

    assert rule.enumerate_files() == [repo / "coverage.xml"]
