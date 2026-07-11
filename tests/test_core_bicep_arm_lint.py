"""Tests for the CORE check bicep_arm_lint (SGO-297)."""

from __future__ import annotations

import ast
from pathlib import Path

from tc_fitness.core_checks.bicep_arm_lint import (
    BicepArmLint,
    bicep_findings,
    build,
    main,
)

# A resource with `tags` declared BEFORE `sku` — out of the canonical order
# (S6975) — plus an empty-literal `properties: {}` (S6954).
_DIRTY = """resource store 'Microsoft.Storage/storageAccounts@2021-01-01' = {
  name: 'store'
  location: 'eastus'
  tags: {
    env: 'prod'
  }
  sku: {
    name: 'Standard_LRS'
  }
  properties: {}
}
"""

# The same resource with the properties filled and `sku` ahead of `tags`.
_CLEAN = """resource store 'Microsoft.Storage/storageAccounts@2021-01-01' = {
  name: 'store'
  location: 'eastus'
  sku: {
    name: 'Standard_LRS'
  }
  tags: {
    env: 'prod'
  }
  properties: {
    accessTier: 'Hot'
  }
}
"""


def _seed(tmp_path: Path, rel: str, body: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_detection_core_flags_empty_literal(tmp_path: Path) -> None:
    p = _seed(tmp_path, "empty.bicep", _DIRTY)
    rules = {rule for _line, rule, _msg in bicep_findings(p)}
    assert "S6954" in rules  # properties: {}


def test_detection_core_flags_property_order(tmp_path: Path) -> None:
    p = _seed(tmp_path, "order.bicep", _DIRTY)
    findings = bicep_findings(p)
    # The `sku` that follows `tags` is out of canonical order.
    order = [(line, msg) for line, rule, msg in findings if rule == "S6975"]
    assert order, "tags-before-sku must raise an S6975 property-order finding"
    assert any("sku" in msg for _line, msg in order)


def test_detection_core_clean(tmp_path: Path) -> None:
    p = _seed(tmp_path, "clean.bicep", _CLEAN)
    assert bicep_findings(p) == []


def test_non_bicep_and_unreadable_are_ignored(tmp_path: Path) -> None:
    # A .bicep that is not valid UTF-8 yields no findings (another concern owns
    # unreadable files); a missing file likewise.
    p = tmp_path / "binary.bicep"
    p.write_bytes(b"\xff\xfe\x00resource")
    assert bicep_findings(p) == []
    assert bicep_findings(tmp_path / "absent.bicep") == []


def test_rule_from_config_scopes_roots(tmp_path: Path) -> None:
    _seed(tmp_path, "infra/dirty.bicep", _DIRTY)
    _seed(tmp_path, "vendor/dirty.bicep", _DIRTY)
    rule = BicepArmLint.from_config({"roots": ["infra"]}, repo_root=tmp_path)
    assert {str(p) for p in rule.collect_violations()} == {"infra/dirty.bicep"}


def test_extension_default_ignores_non_bicep(tmp_path: Path) -> None:
    # A .txt with bicep-shaped content is out of scope (extension gate).
    _seed(tmp_path, "infra/notbicep.txt", _DIRTY)
    rule = BicepArmLint.from_config({"roots": ["infra"]}, repo_root=tmp_path)
    assert rule.collect_violations() == set()


def test_run_fails_on_new_then_establish_grandfathers(tmp_path: Path) -> None:
    _seed(tmp_path, "infra/dirty.bicep", _DIRTY)
    rule = BicepArmLint.from_config({"roots": ["infra"]}, repo_root=tmp_path)
    assert rule.run() == 1
    rule.establish_baseline()
    assert rule.run() == 0


def test_net_new_offender_fails_after_baseline(tmp_path: Path) -> None:
    _seed(tmp_path, "infra/dirty.bicep", _DIRTY)
    rule = BicepArmLint.from_config({"roots": ["infra"]}, repo_root=tmp_path)
    rule.establish_baseline()
    assert rule.run() == 0
    _seed(tmp_path, "infra/dirty2.bicep", _DIRTY)
    assert rule.run() == 1, "a net-new offending .bicep must gate"


def test_build_factory_returns_configured_rule(tmp_path: Path) -> None:
    rule = build({"roots": ["infra"], "extensions": [".bicep"]}, repo_root=tmp_path)
    assert isinstance(rule, BicepArmLint)


def test_main_establish_baseline_mode(tmp_path: Path) -> None:
    _seed(tmp_path, "dirty.bicep", _DIRTY)
    rc = main(["--establish-baseline", "--repo-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / ".architecture" / "baseline" / "bicep-arm-lint-files.txt").exists()


def test_no_repo_strings_in_executable_code() -> None:
    # DESIGN LAW: a CORE module's LOGIC carries no repo identity. Provenance
    # docstrings may name the donor repo, so strip docstrings via AST and scan
    # only the executable string literals.
    import tc_fitness.core_checks.bicep_arm_lint as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")  # type: ignore[arg-type]
    tree = ast.parse(text)
    docstring_ids: set[int] = set()
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
