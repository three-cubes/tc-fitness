"""Context-local events preserve check outcomes without global capture state."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict

import pytest

from tc_fitness.check_evidence import capture_check_evidence, report_finding, report_result

pytestmark = pytest.mark.unit


def test_capture_restores_outer_context_even_when_inner_operation_raises() -> None:
    report_finding("ignored", ".", "no active capture")
    report_result("ignored", 0)
    with capture_check_evidence() as outer:
        report_finding("outer-before", ".", "before nested operation")
        with pytest.raises(ValueError), capture_check_evidence() as inner:
            report_finding("inner", ".", "inside nested operation")
            raise ValueError("operation failed")
        report_finding("outer-after", ".", "after nested operation")
    assert [finding.rule for finding in outer.findings] == ["outer-before", "outer-after"]
    assert [finding.rule for finding in inner.findings] == ["inner"]


def test_simultaneous_captures_do_not_mix_findings_or_terminal_results() -> None:
    def execute(check: str) -> tuple[str, str]:
        with capture_check_evidence() as evidence:
            report_finding(check, ".", "violation")
            report_result(check, 1)
        assert len(evidence.findings) == len(evidence.results) == 1
        return evidence.findings[0].rule, evidence.results[0].check

    with ThreadPoolExecutor(max_workers=2) as pool:
        result = list(pool.map(execute, ("first", "second")))
    assert result == [("first", "first"), ("second", "second")]


def test_error_from_one_check_does_not_poison_the_next_check_result() -> None:
    with capture_check_evidence() as evidence:
        report_finding("first", ".", "required dependency unavailable", status="error")
        report_result("first", 2)
        report_result("second", 0)
    assert [result.status for result in evidence.results] == ["error", "pass"]


def test_finding_preserves_the_complete_structured_failure() -> None:
    with capture_check_evidence() as evidence:
        report_finding("schema-check", "src/schema.json", "required field is missing")
    assert [asdict(finding) for finding in evidence.findings] == [
        {
            "rule": "schema-check",
            "path": "src/schema.json",
            "message": "required field is missing",
            "status": "fail",
        }
    ]


@pytest.mark.parametrize(
    ("exit_code", "crashed", "expected_status"),
    [
        (0, False, "pass"),
        (1, False, "fail"),
        (7, False, "fail"),
        (-9, False, "fail"),
        (0, True, "error"),
        (2, True, "error"),
    ],
)
def test_terminal_result_preserves_raw_exit_and_distinguishes_failure_from_crash(
    exit_code: int, crashed: bool, expected_status: str
) -> None:
    with capture_check_evidence() as evidence:
        report_result("schema-check", exit_code, crashed=crashed)
    assert [asdict(result) for result in evidence.results] == [
        {"check": "schema-check", "status": expected_status, "exit_code": exit_code}
    ]


def test_error_finding_overrides_zero_exit_without_contaminating_the_next_check() -> None:
    with capture_check_evidence() as evidence:
        report_finding("first", "dependency.json", "dependency unavailable", status="error")
        report_result("first", 0)
        report_finding("second", "input.json", "invalid input")
        report_result("second", 9)
    assert [asdict(result) for result in evidence.results] == [
        {"check": "first", "status": "error", "exit_code": 0},
        {"check": "second", "status": "fail", "exit_code": 9},
    ]
    assert evidence.findings[0].status == "error"
