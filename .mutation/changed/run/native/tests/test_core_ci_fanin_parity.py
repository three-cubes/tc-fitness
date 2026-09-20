"""Tests for the CORE check ci_fanin_parity (v0.6.0)."""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks.ci_fanin_parity import (
    build,
    main,
    workflow_fanin_is_dishonest,
)

pytestmark = pytest.mark.integration

_HONEST = """
name: ci
on: [push]
jobs:
  unit:
    name: "Unit tests"
    runs-on: ubuntu-latest
  security:
    name: "Security scan"
    runs-on: ubuntu-latest
  check:
    name: "CI gate"
    needs: [unit, security]
    runs-on: ubuntu-latest
"""

_DANGLING = """
name: ci
on: [push]
jobs:
  unit:
    name: "Unit tests"
    runs-on: ubuntu-latest
  license-scan:
    name: "License scan"
    runs-on: ubuntu-latest
  check:
    name: "CI gate"
    needs: [unit]
    runs-on: ubuntu-latest
"""

_MARKED = """
name: ci
on: [push]
jobs:
  unit:
    name: "Unit tests"
    runs-on: ubuntu-latest
  # fan-in: informational - advisory, posts a PR comment
  sonar:
    name: "Sonar scan"
    runs-on: ubuntu-latest
  check:
    name: "CI gate"
    needs: [unit]
    runs-on: ubuntu-latest
"""

_NO_AGGREGATOR = """
name: ci
on: [push]
jobs:
  unit:
    name: "Unit tests"
    runs-on: ubuntu-latest
"""


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_honest_fanin_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "ci.yml", _HONEST)
    assert workflow_fanin_is_dishonest(p, aggregator_name="CI gate") is False


def test_dangling_job_flagged(tmp_path: Path) -> None:
    p = _seed(tmp_path, "ci.yml", _DANGLING)
    assert workflow_fanin_is_dishonest(p, aggregator_name="CI gate") is True


def test_comment_cannot_suppress_a_dangling_job(tmp_path: Path) -> None:
    p = _seed(tmp_path, "ci.yml", _MARKED)
    assert workflow_fanin_is_dishonest(p, aggregator_name="CI gate") is True


def test_comment_position_cannot_suppress_a_dangling_job(tmp_path: Path) -> None:
    grouped = _seed(
        tmp_path,
        "grouped.yml",
        _MARKED.replace(
            "  # fan-in: informational - advisory, posts a PR comment\n  sonar:",
            "  # fan-in: informational - advisory, posts a PR comment\n  # additional context\n  sonar:",
        ),
    )
    separated = _seed(
        tmp_path,
        "separated.yml",
        _MARKED.replace(
            "  # fan-in: informational - advisory, posts a PR comment\n  sonar:",
            "  # fan-in: informational - advisory, posts a PR comment\n\n  sonar:",
        ),
    )

    assert workflow_fanin_is_dishonest(grouped, aggregator_name="CI gate") is True
    assert workflow_fanin_is_dishonest(separated, aggregator_name="CI gate") is True


def test_needs_accept_scalar_and_string_list_items(tmp_path: Path) -> None:
    scalar = _seed(
        tmp_path,
        "scalar.yml",
        "jobs:\n  build:\n    name: Build\n  gate:\n    name: Merge gate\n    needs: build\n",
    )
    sequence = _seed(
        tmp_path,
        "sequence.yml",
        "jobs:\n  build:\n    name: Build\n  gate:\n    name: Merge gate\n    needs: [build]\n",
    )

    for path in (scalar, sequence):
        assert workflow_fanin_is_dishonest(path, aggregator_name="Merge gate") is False


def test_transitive_valid_needs_are_in_the_gate_closure(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "transitive.yml",
        "jobs:\n  unit:\n    name: Unit tests\n  security:\n    needs: unit\n"
        "  gate:\n    name: Merge gate\n    needs: security\n",
    )

    assert workflow_fanin_is_dishonest(path, aggregator_name="Merge gate") is False


def test_shared_transitive_dependency_is_processed_once(tmp_path: Path) -> None:
    path = _seed(
        tmp_path,
        "shared.yml",
        "jobs:\n  shared:\n    name: Shared build\n  left:\n    needs: shared\n"
        "  right:\n    needs: shared\n  gate:\n    name: Merge gate\n    needs: [left, right]\n",
    )

    assert workflow_fanin_is_dishonest(path, aggregator_name="Merge gate") is False


@pytest.mark.parametrize(
    "workflow",
    ["jobs: []\n", "name: workflow without jobs\n", "- scalar\n", "jobs: invalid\n", "jobs: [unterminated\n"],
)
def test_unverifiable_workflow_shapes_are_violations(tmp_path: Path, workflow: str) -> None:
    path = _seed(tmp_path, "workflow.yml", workflow)

    assert workflow_fanin_is_dishonest(path, aggregator_name="Merge gate") is True


def test_invalid_dependency_graphs_are_violations(tmp_path: Path) -> None:
    invalid_workflows = (
        "jobs:\n  unit:\n    needs: [missing]\n  gate:\n    name: Merge gate\n",
        "jobs:\n  unit:\n    needs: [gate]\n  gate:\n    name: Merge gate\n    needs: unit\n",
        "jobs:\n  gate:\n    name: Merge gate\n    needs: [unit, 4]\n  unit: {}\n",
        "jobs:\n  gate:\n    name: Merge gate\n    needs: ['']\n",
        "jobs:\n  unit: opaque\n  gate:\n    name: Merge gate\n",
        "jobs:\n  gate:\n    name: Merge gate\n  other:\n    name: Merge gate\n",
    )

    for index, workflow in enumerate(invalid_workflows):
        path = _seed(tmp_path, f"invalid-{index}.yml", workflow)
        assert workflow_fanin_is_dishonest(path, aggregator_name="Merge gate") is True


def test_unreadable_workflow_is_a_violation(tmp_path: Path) -> None:
    binary = tmp_path / "binary.yml"
    binary.write_bytes(b"jobs:\n  gate: \xff\n")

    assert workflow_fanin_is_dishonest(tmp_path / "missing.yml", aggregator_name="Merge gate") is True
    assert workflow_fanin_is_dishonest(binary, aggregator_name="Merge gate") is True


def test_missing_required_yaml_parser_fails_import_in_a_clean_process(tmp_path: Path) -> None:
    source_root = Path(__file__).resolve().parents[1] / "src"
    code = "from tc_fitness.core_checks import ci_fanin_parity\nassert ci_fanin_parity.DEFAULT_WORKFLOW\n"
    env = {key: value for key, value in os.environ.items() if key not in {"PYTHONPATH", "PYTHONHOME"}}
    env["PYTHONPATH"] = str(source_root)
    result = subprocess.run(
        [sys.executable, "-S", "-c", code],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode != 0
    assert "yaml" in result.stderr.lower()


def test_missing_aggregator_flagged(tmp_path: Path) -> None:
    p = _seed(tmp_path, "ci.yml", _NO_AGGREGATOR)
    assert workflow_fanin_is_dishonest(p, aggregator_name="CI gate") is True


def test_aggregator_name_config_driven(tmp_path: Path) -> None:
    body = _DANGLING.replace("CI gate", "merge-gate")
    _seed(tmp_path, ".github/workflows/ci.yml", body)
    rule = build({"aggregator_name": "merge-gate"}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {".github/workflows/ci.yml"}


def test_workflow_is_config_driven_but_marker_cannot_suppress_a_job(tmp_path: Path) -> None:
    _seed(tmp_path, "ci/custom.yml", _MARKED.replace("# fan-in: informational", "# merge: advisory"))
    rule = build({"workflow": "ci/custom.yml", "aggregator_name": "CI gate"}, repo_root=tmp_path)
    assert rule.collect_violations() == {Path("ci/custom.yml")}


def test_rule_clean_on_honest(tmp_path: Path) -> None:
    _seed(tmp_path, ".github/workflows/ci.yml", _HONEST)
    rule = build({}, repo_root=tmp_path)
    assert rule.collect_violations() == set()


def test_absent_configured_workflow_is_a_violation(tmp_path: Path) -> None:
    rule = build({}, repo_root=tmp_path)
    assert {str(path) for path in rule.collect_violations()} == {".github/workflows/ci.yml"}


def test_invalid_configured_workflow_fails_through_rule_and_cli(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _seed(tmp_path, ".github/workflows/ci.yml", "jobs: [unterminated\n")

    assert {str(path) for path in build({}, repo_root=tmp_path).collect_violations()} == {
        ".github/workflows/ci.yml"
    }
    assert main(["--repo-root", str(tmp_path)]) == 1
    assert "ci-fanin-parity" in capsys.readouterr().out


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.ci_fanin_parity as mod

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
