"""Tests for the CORE check checkov_iac_security (SGO-297).

The Checkov invocation is a dependency-injected ``runner`` seam, so these tests
drive the diff/baseline logic with canned Checkov JSON — no binary, no network,
no internal patching.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from tc_fitness.core_checks.checkov_iac_security import (
    CheckovIacSecurity,
    build,
    finding_key,
    main,
    net_new_findings,
    parse_failed,
    parsing_error_count,
)


def _report(*failed: dict[str, Any], parsing_errors: int = 0) -> dict[str, Any]:
    return {
        "results": {"failed_checks": list(failed)},
        "summary": {"parsing_errors": parsing_errors},
    }


_FAIL_A = {
    "check_id": "CKV_AZURE_1",
    "check_name": "Ensure storage account uses HTTPS only",
    "file_path": "/store.bicep",
    "resource": "Microsoft.Storage/storageAccounts.store",
    "file_line_range": [1, 12],
    "guideline": "https://docs.example/CKV_AZURE_1",
    "framework": "bicep",
}
_FAIL_B = {
    "check_id": "CKV_AZURE_2",
    "check_name": "Ensure storage account blocks public access",
    "file_path": "/store.bicep",
    "resource": "Microsoft.Storage/storageAccounts.store",
    "file_line_range": [1, 12],
    "framework": "bicep",
}


def test_parse_failed_and_finding_key() -> None:
    failed = parse_failed(_report(_FAIL_A, _FAIL_B))
    assert len(failed) == 2
    assert finding_key(_FAIL_A) == "CKV_AZURE_1|/store.bicep|Microsoft.Storage/storageAccounts.store"


def test_parse_failed_handles_list_of_reports() -> None:
    # Checkov may emit a LIST of reports (multi-framework) — both are flattened.
    data = [_report(_FAIL_A), _report(_FAIL_B)]
    assert len(parse_failed(data)) == 2


def test_parsing_error_count_surfaced() -> None:
    assert parsing_error_count(_report(_FAIL_A, parsing_errors=3)) == 3


def test_net_new_findings_excludes_baselined() -> None:
    failed = parse_failed(_report(_FAIL_A, _FAIL_B))
    baseline = {finding_key(_FAIL_A)}
    net_new = net_new_findings(failed, baseline)
    assert [finding_key(fc) for fc in net_new] == [finding_key(_FAIL_B)]


def test_evaluate_flags_net_new_with_injected_runner(tmp_path: Path) -> None:
    rule = CheckovIacSecurity(
        tmp_path,
        scan_dir="infra",
        runner=lambda _sd: _report(_FAIL_A),
    )
    passed, errors, meta = rule.evaluate()
    assert not passed
    assert meta["net_new"] == 1
    assert "CKV_AZURE_1" in errors[0]


def test_evaluate_soft_skips_when_runner_returns_none(tmp_path: Path) -> None:
    rule = CheckovIacSecurity(tmp_path, runner=lambda _sd: None)
    passed, errors, meta = rule.evaluate()
    assert passed
    assert errors == []
    assert meta["skipped"] is True


def test_run_soft_skip_returns_zero(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    rule = CheckovIacSecurity(tmp_path, runner=lambda _sd: None)
    assert rule.run() == 0
    assert "soft-skip" in capsys.readouterr().out


def test_run_fails_then_establish_grandfathers(tmp_path: Path) -> None:
    rule = CheckovIacSecurity(tmp_path, scan_dir="infra", runner=lambda _sd: _report(_FAIL_A))
    assert rule.run() == 1
    path = rule.establish_baseline()
    assert path.exists()
    assert finding_key(_FAIL_A) in path.read_text(encoding="utf-8")
    # After grandfathering, the same finding is tolerated — only net-new gates.
    assert rule.run() == 0


def test_net_new_after_baseline_fails(tmp_path: Path) -> None:
    rule = CheckovIacSecurity(tmp_path, scan_dir="infra", runner=lambda _sd: _report(_FAIL_A))
    rule.establish_baseline()
    assert rule.run() == 0
    # A SECOND finding appears — grandfathered A tolerated, net-new B gates.
    rule2 = CheckovIacSecurity(tmp_path, scan_dir="infra", runner=lambda _sd: _report(_FAIL_A, _FAIL_B))
    assert rule2.run() == 1


def test_from_config_and_baseline_name(tmp_path: Path) -> None:
    rule = CheckovIacSecurity.from_config(
        {"scan_dir": "infra", "name": "checkov_iac_security", "framework": "bicep"},
        repo_root=tmp_path,
    )
    assert rule.baseline_path.name == "checkov_iac_security-findings.txt"
    assert rule.scan_path == (tmp_path / "infra").resolve()


def test_build_factory_returns_instance(tmp_path: Path) -> None:
    rule = build({"scan_dir": "infra"}, repo_root=tmp_path)
    assert isinstance(rule, CheckovIacSecurity)


def test_main_gate_and_establish_are_deterministic_without_binary(tmp_path: Path) -> None:
    # main() uses the real checkov binary (runner=None). tc-fitness ships zero
    # runtime deps, so on CI checkov is absent → soft-skip (rc 0); establish then
    # writes an empty key baseline. An empty scan tree keeps the verdict stable
    # even where checkov IS installed (no resources → no findings).
    (tmp_path / "infra").mkdir()
    assert main(["--repo-root", str(tmp_path)]) == 0
    assert main(["--establish-baseline", "--repo-root", str(tmp_path)]) == 0
    assert (tmp_path / ".architecture" / "baseline" / "checkov-iac-security-findings.txt").exists()


def test_no_repo_strings_in_executable_code() -> None:
    # DESIGN LAW: a CORE module's LOGIC carries no repo identity.
    import tc_fitness.core_checks.checkov_iac_security as mod

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
