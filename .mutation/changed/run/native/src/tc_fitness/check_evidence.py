"""Context-local structured events emitted by the real check execution path.

Events are optional and have no console side effects. Custom CORE checks emit
findings here at the same point they decide and display a violation or error.
The existing dispatcher records the terminal result, including check crashes.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str
    message: str
    status: str = "fail"


@dataclass(frozen=True)
class CheckResult:
    check: str
    status: str
    exit_code: int


@dataclass
class CheckEvidence:
    findings: list[Finding] = field(default_factory=list)
    results: list[CheckResult] = field(default_factory=list)
    _finding_offset: int = 0


_SINK: ContextVar[CheckEvidence | None] = ContextVar("check_evidence", default=None)


@contextmanager
def capture_check_evidence() -> Iterator[CheckEvidence]:
    """Capture only this context's events, restoring any enclosing capture."""
    evidence = CheckEvidence()
    token = _SINK.set(evidence)
    try:
        yield evidence
    finally:
        _SINK.reset(token)
mutants_x_report_finding__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_report_finding__mutmut)
def report_finding(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, path, message, status))


def x_report_finding__mutmut_orig(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, path, message, status))


def x_report_finding__mutmut_1(rule: str, path: str, message: str, *, status: str = "XXfailXX") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, path, message, status))


def x_report_finding__mutmut_2(rule: str, path: str, message: str, *, status: str = "FAIL") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, path, message, status))


def x_report_finding__mutmut_3(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = None
    if sink is not None:
        sink.findings.append(Finding(rule, path, message, status))


def x_report_finding__mutmut_4(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is None:
        sink.findings.append(Finding(rule, path, message, status))


def x_report_finding__mutmut_5(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(None)


def x_report_finding__mutmut_6(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(None, path, message, status))


def x_report_finding__mutmut_7(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, None, message, status))


def x_report_finding__mutmut_8(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, path, None, status))


def x_report_finding__mutmut_9(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, path, message, None))


def x_report_finding__mutmut_10(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(path, message, status))


def x_report_finding__mutmut_11(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, message, status))


def x_report_finding__mutmut_12(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, path, status))


def x_report_finding__mutmut_13(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, path, message, ))

mutants_x_report_finding__mutmut['_mutmut_orig'] = x_report_finding__mutmut_orig # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_1'] = x_report_finding__mutmut_1 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_2'] = x_report_finding__mutmut_2 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_3'] = x_report_finding__mutmut_3 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_4'] = x_report_finding__mutmut_4 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_5'] = x_report_finding__mutmut_5 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_6'] = x_report_finding__mutmut_6 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_7'] = x_report_finding__mutmut_7 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_8'] = x_report_finding__mutmut_8 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_9'] = x_report_finding__mutmut_9 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_10'] = x_report_finding__mutmut_10 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_11'] = x_report_finding__mutmut_11 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_12'] = x_report_finding__mutmut_12 # type: ignore # mutmut generated
mutants_x_report_finding__mutmut['x_report_finding__mutmut_13'] = x_report_finding__mutmut_13 # type: ignore # mutmut generated
mutants_x_report_result__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_report_result__mutmut)
def report_result(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_orig(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_1(check: str, exit_code: int, *, crashed: bool = True) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_2(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = None
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_3(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_4(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = None
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_5(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed and any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_6(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(None)
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_7(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status != "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_8(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "XXerrorXX" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_9(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "ERROR" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_10(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = None
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_11(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "XXerrorXX" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_12(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "ERROR" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_13(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "XXpassXX" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_14(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "PASS" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_15(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code != 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_16(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 1 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_17(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "XXfailXX"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_18(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "FAIL"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_19(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(None)
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_20(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(None, status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_21(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, None, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_22(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, None))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_23(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(status, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_24(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, exit_code))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_25(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, ))
        sink._finding_offset = len(sink.findings)


def x_report_result__mutmut_26(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = None

mutants_x_report_result__mutmut['_mutmut_orig'] = x_report_result__mutmut_orig # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_1'] = x_report_result__mutmut_1 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_2'] = x_report_result__mutmut_2 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_3'] = x_report_result__mutmut_3 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_4'] = x_report_result__mutmut_4 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_5'] = x_report_result__mutmut_5 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_6'] = x_report_result__mutmut_6 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_7'] = x_report_result__mutmut_7 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_8'] = x_report_result__mutmut_8 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_9'] = x_report_result__mutmut_9 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_10'] = x_report_result__mutmut_10 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_11'] = x_report_result__mutmut_11 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_12'] = x_report_result__mutmut_12 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_13'] = x_report_result__mutmut_13 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_14'] = x_report_result__mutmut_14 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_15'] = x_report_result__mutmut_15 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_16'] = x_report_result__mutmut_16 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_17'] = x_report_result__mutmut_17 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_18'] = x_report_result__mutmut_18 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_19'] = x_report_result__mutmut_19 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_20'] = x_report_result__mutmut_20 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_21'] = x_report_result__mutmut_21 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_22'] = x_report_result__mutmut_22 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_23'] = x_report_result__mutmut_23 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_24'] = x_report_result__mutmut_24 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_25'] = x_report_result__mutmut_25 # type: ignore # mutmut generated
mutants_x_report_result__mutmut['x_report_result__mutmut_26'] = x_report_result__mutmut_26 # type: ignore # mutmut generated
