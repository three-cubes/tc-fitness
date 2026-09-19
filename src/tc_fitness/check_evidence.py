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


def report_finding(rule: str, path: str, message: str, *, status: str = "fail") -> None:
    """Emit a finding from the decision that produced it, never from log text."""
    sink = _SINK.get()
    if sink is not None:
        sink.findings.append(Finding(rule, path, message, status))


def report_result(check: str, exit_code: int, *, crashed: bool = False) -> None:
    """Record the dispatched check's raw exit and terminal classification."""
    sink = _SINK.get()
    if sink is not None:
        error = crashed or any(finding.status == "error" for finding in sink.findings[sink._finding_offset :])
        status = "error" if error else "pass" if exit_code == 0 else "fail"
        sink.results.append(CheckResult(check, status, exit_code))
        sink._finding_offset = len(sink.findings)
