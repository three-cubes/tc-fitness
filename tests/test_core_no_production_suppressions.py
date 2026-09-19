"""Tests for the CORE check no_production_suppressions (v0.6.0)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from tc_fitness.core_checks.no_production_suppressions import (
    NoProductionSuppressions,
    build,
    file_contains_suppression,
    main,
)

pytestmark = pytest.mark.integration

_SUPPRESSED = "result = parse(payload)  # noqa: BLE001\n"
_CLEAN = "result = parse(payload)  # finding fixed upstream\n"


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_core_flags_suppression(tmp_path: Path) -> None:
    p = _seed(tmp_path, "s.py", _SUPPRESSED)
    assert file_contains_suppression(p, ("# noqa:",)) is True


def test_detection_core_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "c.py", _CLEAN)
    assert file_contains_suppression(p, ("# noqa:",)) is False


def test_empty_patterns_and_unreadable_sources_are_clean(tmp_path: Path) -> None:
    path = _seed(tmp_path, "empty.py", "value = 1\n")
    binary = tmp_path / "binary.py"
    binary.write_bytes(b"# noqa: BLE001\n\xff")

    assert file_contains_suppression(path, ()) is False
    assert file_contains_suppression(tmp_path / "missing.py", ("# noqa:",)) is False
    assert file_contains_suppression(binary, ("# noqa:",)) is False


def test_exempt_prefix_skips_file(tmp_path: Path) -> None:
    _seed(tmp_path, "src/app.py", _SUPPRESSED)
    _seed(tmp_path, "scripts/tool.py", _SUPPRESSED)
    rule = NoProductionSuppressions.from_config(
        {"roots": ["src", "scripts"], "exempt_prefixes": ["scripts/"]},
        repo_root=tmp_path,
    )
    assert {str(p) for p in rule.collect_violations()} == {"src/app.py"}


def test_test_file_basename_is_exempt(tmp_path: Path) -> None:
    _seed(tmp_path, "src/app.py", _SUPPRESSED)
    _seed(tmp_path, "src/test_app.py", _SUPPRESSED)
    rule = NoProductionSuppressions.from_config({"roots": ["src"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"src/app.py"}


def test_files_outside_python_extension_scope_are_not_production(tmp_path: Path) -> None:
    rule = build({"roots": ["src"]}, repo_root=tmp_path)

    assert rule.is_in_scope("src/app.txt") is False
    assert rule.is_in_scope("src/test_app.py") is False


def test_suppression_patterns_config_driven(tmp_path: Path) -> None:
    p = _seed(tmp_path, "src/app.ts", "const x = 1; // NOSONAR\n")
    rule = build(
        {"roots": ["src"], "extensions": [".ts"], "suppression_patterns": ["// NOSONAR"]},
        repo_root=tmp_path,
    )
    assert rule.file_has_violation(p) is True


def test_run_then_establish_grandfathers(tmp_path: Path) -> None:
    _seed(tmp_path, "src/app.py", _SUPPRESSED)
    rule = NoProductionSuppressions.from_config({"roots": ["src"]}, repo_root=tmp_path)
    assert rule.run() == 1
    rule.establish_baseline()
    assert rule.run() == 0


def test_main_establish_baseline_mode(tmp_path: Path) -> None:
    _seed(tmp_path, "app.py", _SUPPRESSED)
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / ".architecture" / "baseline" / "no-production-suppressions-files.txt").exists()


def test_no_repo_strings_in_executable_code() -> None:
    import tc_fitness.core_checks.no_production_suppressions as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(text)
    docstring_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            doc = ast.get_docstring(node, clean=False)
            if doc is not None and node.body:
                first = node.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                    docstring_ids.add(id(first.value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstring_ids:
            lowered = node.value.lower()
            for tok in ("kairix", "tc-agent-zone", "agent-zone", "kata"):
                assert tok not in lowered, f"repo identity leaked: {tok}"
