"""Tests for the CORE check checkov_iac_security (SGO-297).

The Checkov invocation is a dependency-injected ``runner`` seam, so these tests
drive the diff/baseline logic with canned Checkov JSON — no binary, no network,
no internal patching.
"""

from __future__ import annotations

from typing import Any

import pytest

from tc_fitness.core_checks.checkov_iac_security import (
    finding_key,
    net_new_findings,
    parse_failed,
    parsing_error_count,
)

pytestmark = pytest.mark.unit


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
