"""Tests for the CORE check schema_conformance (v0.6.0)."""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tc_fitness.core_checks.schema_conformance import (
    build,
    file_missing_required_keys,
)

pytestmark = pytest.mark.integration


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_missing_key_is_violation(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.yaml", "palette: blue\n")
    assert file_missing_required_keys(p, required_keys=("palette", "typeScale")) is True


def test_all_keys_present_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.yaml", "palette: blue\ntypeScale: 1.2\n")
    assert file_missing_required_keys(p, required_keys=("palette", "typeScale")) is False


def test_non_mapping_is_violation(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.yaml", "- item1\n- item2\n")
    assert file_missing_required_keys(p, required_keys=("palette",)) is True


def test_empty_required_keys_always_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.yaml", "anything: ok\n")
    assert file_missing_required_keys(p, required_keys=()) is False


def test_json_parses_via_yaml(tmp_path: Path) -> None:
    p = _seed(tmp_path, "a.json", '{"palette": "blue"}')
    assert file_missing_required_keys(p, required_keys=("palette",)) is False
    assert file_missing_required_keys(p, required_keys=("missing",)) is True


def test_malformed_yaml_cannot_prove_schema_conformance(tmp_path: Path) -> None:
    p = _seed(tmp_path, "invalid.yaml", "palette: [blue\n")

    assert file_missing_required_keys(p, required_keys=("palette",)) is True


def test_non_utf8_yaml_cannot_prove_schema_conformance(tmp_path: Path) -> None:
    p = tmp_path / "invalid.yaml"
    p.write_bytes(b"palette: \xff\n")

    assert file_missing_required_keys(p, required_keys=("palette",)) is True


def test_rule_scopes_roots_and_keys(tmp_path: Path) -> None:
    _seed(tmp_path, "tokens/acme.yaml", "palette: blue\n")
    _seed(tmp_path, "vendor/other.yaml", "palette: blue\n")
    rule = build({"roots": ["tokens"], "required_keys": ["palette", "typeScale"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"tokens/acme.yaml"}


def test_python_module_entrypoint_runs_the_public_gate(tmp_path: Path) -> None:
    source_root = Path(__file__).parents[1] / "src"
    result = subprocess.run(
        [
            sys.executable,
            "-S",
            "-m",
            "tc_fitness.core_checks.schema_conformance",
            "--repo-root",
            str(tmp_path),
        ],
        capture_output=True,
        check=False,
        text=True,
        env={**os.environ, "PYTHONPATH": str(source_root)},
    )

    assert result.returncode == 0, result.stderr


def test_python_module_entrypoint_reports_the_public_check_result(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "tc_fitness.core_checks.schema_conformance", "--repo-root", str(tmp_path)],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_optional_yaml_dependency_absence_fails_closed_in_an_isolated_interpreter(tmp_path: Path) -> None:
    document = _seed(tmp_path, "tokens.yaml", "palette: blue\n")
    source_root = Path(__file__).parents[1] / "src"
    program = (
        "import sys; sys.path.insert(0, sys.argv[1]); "
        "from pathlib import Path; "
        "from tc_fitness.core_checks.schema_conformance import file_missing_required_keys; "
        "assert file_missing_required_keys(Path(sys.argv[2]), required_keys=('palette',))"
    )
    result = subprocess.run(
        [sys.executable, "-S", "-c", program, str(source_root), str(document)],
        capture_output=True,
        check=False,
        text=True,
        env={**os.environ, "PYTHONPATH": str(source_root)},
    )

    assert result.returncode == 0, result.stderr


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.schema_conformance as mod

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
