"""CORE check: require a clean Checkov scan of the configured IaC directory.

Every Checkov finding blocks. Parsing failures, malformed reports, unavailable
executables, and scanner execution errors also block because the scan has not
proved that the IaC tree is clean.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any

from tc_fitness.check_evidence import report_finding
from tc_fitness.lib import REPO_ROOT
from tc_fitness.lib import remediation as _remediation

DEFAULT_SCAN_DIR = "."
DEFAULT_FRAMEWORK = "bicep"
DEFAULT_TIMEOUT = 180
_PARSING_ERRORS_KEY = "parsing_errors"

REMEDIATION = _remediation(
    fix="remediate every Checkov finding and correct every IaC parsing error before merging.",
    nxt="re-run this check and confirm Checkov reports zero findings and zero parsing errors.",
    run="python -m tc_fitness.core_checks.checkov_iac_security",
    passing="Checkov completes successfully with zero policy findings and zero parsing errors",
    forbidden="IaC is admitted when Checkov reports a policy finding, parsing error, or execution failure",
)


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class CheckovScanError(RuntimeError):
    """The scanner did not produce a complete, trustworthy report."""
mutants_x_checkov_binary__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_checkov_binary__mutmut)
def checkov_binary() -> str | None:
    """Return the installed Checkov executable, or ``None`` when it is absent."""
    return shutil.which("checkov")


def x_checkov_binary__mutmut_orig() -> str | None:
    """Return the installed Checkov executable, or ``None`` when it is absent."""
    return shutil.which("checkov")


def x_checkov_binary__mutmut_1() -> str | None:
    """Return the installed Checkov executable, or ``None`` when it is absent."""
    return shutil.which(None)


def x_checkov_binary__mutmut_2() -> str | None:
    """Return the installed Checkov executable, or ``None`` when it is absent."""
    return shutil.which("XXcheckovXX")


def x_checkov_binary__mutmut_3() -> str | None:
    """Return the installed Checkov executable, or ``None`` when it is absent."""
    return shutil.which("CHECKOV")

mutants_x_checkov_binary__mutmut['_mutmut_orig'] = x_checkov_binary__mutmut_orig # type: ignore # mutmut generated
mutants_x_checkov_binary__mutmut['x_checkov_binary__mutmut_1'] = x_checkov_binary__mutmut_1 # type: ignore # mutmut generated
mutants_x_checkov_binary__mutmut['x_checkov_binary__mutmut_2'] = x_checkov_binary__mutmut_2 # type: ignore # mutmut generated
mutants_x_checkov_binary__mutmut['x_checkov_binary__mutmut_3'] = x_checkov_binary__mutmut_3 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__parse_report__mutmut)
def _parse_report(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_orig(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_1(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = None
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_2(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(None)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_3(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(None) from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_4(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_5(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError(None)
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_6(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("XXCheckov JSON report must be an objectXX")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_7(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("checkov json report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_8(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("CHECKOV JSON REPORT MUST BE AN OBJECT")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_9(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = None
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_10(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get(None)
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_11(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("XXresultsXX")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_12(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("RESULTS")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_13(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = None
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_14(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get(None)
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_15(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("XXsummaryXX")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_16(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("SUMMARY")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_17(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) and not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_18(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_19(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_20(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError(None)
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_21(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("XXCheckov JSON report is missing results or summaryXX")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_22(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("checkov json report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_23(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("CHECKOV JSON REPORT IS MISSING RESULTS OR SUMMARY")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_24(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = None
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_25(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get(None)
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_26(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("XXfailed_checksXX")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_27(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("FAILED_CHECKS")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_28(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) and not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_29(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_30(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_31(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(None):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_32(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError(None)
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_33(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("XXCheckov JSON report has an invalid failed_checks listXX")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_34(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("checkov json report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_35(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("CHECKOV JSON REPORT HAS AN INVALID FAILED_CHECKS LIST")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_36(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = None
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_37(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(None)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_38(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) and parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_39(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) and isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_40(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_41(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors <= 0:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_42(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 1:
        raise CheckovScanError("Checkov JSON report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_43(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError(None)
    return report


def x__parse_report__mutmut_44(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("XXCheckov JSON report has an invalid parsing_errors countXX")
    return report


def x__parse_report__mutmut_45(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("checkov json report has an invalid parsing_errors count")
    return report


def x__parse_report__mutmut_46(payload: str) -> dict[str, Any]:
    """Decode Checkov JSON and validate the fields needed for a clean-scan decision."""
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise CheckovScanError(f"Checkov returned invalid JSON: {exc.msg}") from exc
    if not isinstance(report, dict):
        raise CheckovScanError("Checkov JSON report must be an object")
    results = report.get("results")
    summary = report.get("summary")
    if not isinstance(results, dict) or not isinstance(summary, dict):
        raise CheckovScanError("Checkov JSON report is missing results or summary")
    failed = results.get("failed_checks")
    if not isinstance(failed, list) or not all(isinstance(item, dict) for item in failed):
        raise CheckovScanError("Checkov JSON report has an invalid failed_checks list")
    parsing_errors = summary.get(_PARSING_ERRORS_KEY)
    if not isinstance(parsing_errors, int) or isinstance(parsing_errors, bool) or parsing_errors < 0:
        raise CheckovScanError("CHECKOV JSON REPORT HAS AN INVALID PARSING_ERRORS COUNT")
    return report

mutants_x__parse_report__mutmut['_mutmut_orig'] = x__parse_report__mutmut_orig # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_1'] = x__parse_report__mutmut_1 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_2'] = x__parse_report__mutmut_2 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_3'] = x__parse_report__mutmut_3 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_4'] = x__parse_report__mutmut_4 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_5'] = x__parse_report__mutmut_5 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_6'] = x__parse_report__mutmut_6 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_7'] = x__parse_report__mutmut_7 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_8'] = x__parse_report__mutmut_8 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_9'] = x__parse_report__mutmut_9 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_10'] = x__parse_report__mutmut_10 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_11'] = x__parse_report__mutmut_11 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_12'] = x__parse_report__mutmut_12 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_13'] = x__parse_report__mutmut_13 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_14'] = x__parse_report__mutmut_14 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_15'] = x__parse_report__mutmut_15 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_16'] = x__parse_report__mutmut_16 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_17'] = x__parse_report__mutmut_17 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_18'] = x__parse_report__mutmut_18 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_19'] = x__parse_report__mutmut_19 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_20'] = x__parse_report__mutmut_20 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_21'] = x__parse_report__mutmut_21 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_22'] = x__parse_report__mutmut_22 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_23'] = x__parse_report__mutmut_23 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_24'] = x__parse_report__mutmut_24 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_25'] = x__parse_report__mutmut_25 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_26'] = x__parse_report__mutmut_26 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_27'] = x__parse_report__mutmut_27 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_28'] = x__parse_report__mutmut_28 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_29'] = x__parse_report__mutmut_29 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_30'] = x__parse_report__mutmut_30 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_31'] = x__parse_report__mutmut_31 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_32'] = x__parse_report__mutmut_32 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_33'] = x__parse_report__mutmut_33 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_34'] = x__parse_report__mutmut_34 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_35'] = x__parse_report__mutmut_35 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_36'] = x__parse_report__mutmut_36 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_37'] = x__parse_report__mutmut_37 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_38'] = x__parse_report__mutmut_38 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_39'] = x__parse_report__mutmut_39 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_40'] = x__parse_report__mutmut_40 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_41'] = x__parse_report__mutmut_41 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_42'] = x__parse_report__mutmut_42 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_43'] = x__parse_report__mutmut_43 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_44'] = x__parse_report__mutmut_44 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_45'] = x__parse_report__mutmut_45 # type: ignore # mutmut generated
mutants_x__parse_report__mutmut['x__parse_report__mutmut_46'] = x__parse_report__mutmut_46 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_run_checkov__mutmut)
def run_checkov(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_orig(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_1(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = None
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_2(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is not None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_3(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = None
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_4(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            None,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_5(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=None,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_6(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=None,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_7(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=None,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_8(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=None,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_9(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_10(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_11(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_12(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_13(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_14(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "XX-dXX",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_15(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-D",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_16(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(None),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_17(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "XX--frameworkXX",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_18(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--FRAMEWORK",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_19(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "XX--outputXX",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_20(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--OUTPUT",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_21(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "XXjsonXX",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_22(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "JSON",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_23(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "XX--quietXX",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_24(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--QUIET",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_25(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "XX--compactXX",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_26(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--COMPACT",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_27(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=False,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_28(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=False,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_29(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_30(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(None) from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_31(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_32(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (1, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_33(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 2):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_34(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(None)
    report = _parse_report(process.stdout)
    return process.returncode, report


def x_run_checkov__mutmut_35(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = None
    return process.returncode, report


def x_run_checkov__mutmut_36(
    scan_dir: Path,
    *,
    framework: str = DEFAULT_FRAMEWORK,
    timeout: int = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, Any]] | None:
    """Run the installed scanner and return its exit status and validated report.

    ``None`` means Checkov is unavailable. All other incomplete scan outcomes
    raise :class:`CheckovScanError` so callers cannot treat them as clean.
    """
    binary = checkov_binary()
    if binary is None:
        return None
    try:
        process = subprocess.run(
            [
                binary,
                "-d",
                str(scan_dir),
                "--framework",
                framework,
                "--output",
                "json",
                "--quiet",
                "--compact",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckovScanError(f"Checkov execution failed: {exc}") from exc
    if process.returncode not in (0, 1):
        raise CheckovScanError(f"Checkov exited with unexpected status {process.returncode}")
    report = _parse_report(None)
    return process.returncode, report

mutants_x_run_checkov__mutmut['_mutmut_orig'] = x_run_checkov__mutmut_orig # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_1'] = x_run_checkov__mutmut_1 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_2'] = x_run_checkov__mutmut_2 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_3'] = x_run_checkov__mutmut_3 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_4'] = x_run_checkov__mutmut_4 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_5'] = x_run_checkov__mutmut_5 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_6'] = x_run_checkov__mutmut_6 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_7'] = x_run_checkov__mutmut_7 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_8'] = x_run_checkov__mutmut_8 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_9'] = x_run_checkov__mutmut_9 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_10'] = x_run_checkov__mutmut_10 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_11'] = x_run_checkov__mutmut_11 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_12'] = x_run_checkov__mutmut_12 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_13'] = x_run_checkov__mutmut_13 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_14'] = x_run_checkov__mutmut_14 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_15'] = x_run_checkov__mutmut_15 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_16'] = x_run_checkov__mutmut_16 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_17'] = x_run_checkov__mutmut_17 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_18'] = x_run_checkov__mutmut_18 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_19'] = x_run_checkov__mutmut_19 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_20'] = x_run_checkov__mutmut_20 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_21'] = x_run_checkov__mutmut_21 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_22'] = x_run_checkov__mutmut_22 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_23'] = x_run_checkov__mutmut_23 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_24'] = x_run_checkov__mutmut_24 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_25'] = x_run_checkov__mutmut_25 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_26'] = x_run_checkov__mutmut_26 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_27'] = x_run_checkov__mutmut_27 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_28'] = x_run_checkov__mutmut_28 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_29'] = x_run_checkov__mutmut_29 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_30'] = x_run_checkov__mutmut_30 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_31'] = x_run_checkov__mutmut_31 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_32'] = x_run_checkov__mutmut_32 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_33'] = x_run_checkov__mutmut_33 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_34'] = x_run_checkov__mutmut_34 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_35'] = x_run_checkov__mutmut_35 # type: ignore # mutmut generated
mutants_x_run_checkov__mutmut['x_run_checkov__mutmut_36'] = x_run_checkov__mutmut_36 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__finding_line__mutmut)
def _finding_line(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_orig(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_1(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = None
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_2(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(None)
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_3(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get(None, "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_4(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", None))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_5(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_6(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", ))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_7(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("XXcheck_idXX", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_8(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("CHECK_ID", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_9(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "XXunknown-checkXX"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_10(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "UNKNOWN-CHECK"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_11(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = None
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_12(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(None)
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_13(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get(None, "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_14(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", None))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_15(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_16(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", ))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_17(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("XXcheck_nameXX", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_18(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("CHECK_NAME", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_19(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "XXCheckov policy violationXX"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_20(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_21(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "CHECKOV POLICY VIOLATION"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_22(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = None
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_23(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(None)
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_24(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get(None, "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_25(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", None))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_26(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_27(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", ))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_28(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("XXfile_pathXX", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_29(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("FILE_PATH", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_30(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "XX<unknown>XX"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_31(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<UNKNOWN>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_32(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = None
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_33(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get(None)
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_34(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("XXfile_line_rangeXX")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_35(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("FILE_LINE_RANGE")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_36(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) or len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_37(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) > 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_38(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 3:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_39(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = None
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_40(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[1]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_41(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[2]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_42(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = None
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_43(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(None)
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_44(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get(None, "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_45(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", None))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_46(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_47(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", ))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_48(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("XXresourceXX", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_49(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("RESOURCE", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_50(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "XX<unknown>XX"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_51(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<UNKNOWN>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_52(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = None
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_53(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get(None)
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_54(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("XXguidelineXX")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_55(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("GUIDELINE")
    guidance = f" See {guideline}." if guideline else ""
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_56(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = None
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"


def x__finding_line__mutmut_57(failed_check: Mapping[str, Any]) -> str:
    """Render a scanner finding as concise, actionable diagnostic output."""
    check_id = str(failed_check.get("check_id", "unknown-check"))
    check_name = str(failed_check.get("check_name", "Checkov policy violation"))
    file_path = str(failed_check.get("file_path", "<unknown>"))
    line_range = failed_check.get("file_line_range")
    if isinstance(line_range, list) and len(line_range) >= 2:
        file_path = f"{file_path}:{line_range[0]}-{line_range[1]}"
    resource = str(failed_check.get("resource", "<unknown>"))
    guideline = failed_check.get("guideline")
    guidance = f" See {guideline}." if guideline else "XXXX"
    return f"  - [{check_id}] {check_name}: {resource} at {file_path}.{guidance}"

mutants_x__finding_line__mutmut['_mutmut_orig'] = x__finding_line__mutmut_orig # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_1'] = x__finding_line__mutmut_1 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_2'] = x__finding_line__mutmut_2 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_3'] = x__finding_line__mutmut_3 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_4'] = x__finding_line__mutmut_4 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_5'] = x__finding_line__mutmut_5 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_6'] = x__finding_line__mutmut_6 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_7'] = x__finding_line__mutmut_7 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_8'] = x__finding_line__mutmut_8 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_9'] = x__finding_line__mutmut_9 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_10'] = x__finding_line__mutmut_10 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_11'] = x__finding_line__mutmut_11 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_12'] = x__finding_line__mutmut_12 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_13'] = x__finding_line__mutmut_13 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_14'] = x__finding_line__mutmut_14 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_15'] = x__finding_line__mutmut_15 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_16'] = x__finding_line__mutmut_16 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_17'] = x__finding_line__mutmut_17 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_18'] = x__finding_line__mutmut_18 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_19'] = x__finding_line__mutmut_19 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_20'] = x__finding_line__mutmut_20 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_21'] = x__finding_line__mutmut_21 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_22'] = x__finding_line__mutmut_22 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_23'] = x__finding_line__mutmut_23 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_24'] = x__finding_line__mutmut_24 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_25'] = x__finding_line__mutmut_25 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_26'] = x__finding_line__mutmut_26 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_27'] = x__finding_line__mutmut_27 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_28'] = x__finding_line__mutmut_28 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_29'] = x__finding_line__mutmut_29 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_30'] = x__finding_line__mutmut_30 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_31'] = x__finding_line__mutmut_31 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_32'] = x__finding_line__mutmut_32 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_33'] = x__finding_line__mutmut_33 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_34'] = x__finding_line__mutmut_34 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_35'] = x__finding_line__mutmut_35 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_36'] = x__finding_line__mutmut_36 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_37'] = x__finding_line__mutmut_37 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_38'] = x__finding_line__mutmut_38 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_39'] = x__finding_line__mutmut_39 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_40'] = x__finding_line__mutmut_40 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_41'] = x__finding_line__mutmut_41 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_42'] = x__finding_line__mutmut_42 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_43'] = x__finding_line__mutmut_43 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_44'] = x__finding_line__mutmut_44 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_45'] = x__finding_line__mutmut_45 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_46'] = x__finding_line__mutmut_46 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_47'] = x__finding_line__mutmut_47 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_48'] = x__finding_line__mutmut_48 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_49'] = x__finding_line__mutmut_49 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_50'] = x__finding_line__mutmut_50 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_51'] = x__finding_line__mutmut_51 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_52'] = x__finding_line__mutmut_52 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_53'] = x__finding_line__mutmut_53 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_54'] = x__finding_line__mutmut_54 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_55'] = x__finding_line__mutmut_55 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_56'] = x__finding_line__mutmut_56 # type: ignore # mutmut generated
mutants_x__finding_line__mutmut['x__finding_line__mutmut_57'] = x__finding_line__mutmut_57 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__finding_path__mutmut)
def _finding_path(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_orig(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_1(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = None
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_2(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get(None)
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_3(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("XXfile_abs_pathXX")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_4(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("FILE_ABS_PATH")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_5(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = None
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_6(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(None)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_7(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(None).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_8(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = None
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_9(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(None)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_10(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(None).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_11(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = None
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_12(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(None)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_13(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(None).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_14(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(None)).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_15(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get(None, "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_16(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", None))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_17(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_18(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", ))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_19(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("XXfile_pathXX", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_20(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("FILE_PATH", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_21(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "XXunknownXX"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_22(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "UNKNOWN"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_23(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) * PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_24(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(None) / PurePosixPath(relative.as_posix())).as_posix()


def x__finding_path__mutmut_25(failed_check: Mapping[str, Any], *, scan_path: Path, scan_dir: str) -> str:
    """Return the finding path relative to the consumer repository."""
    absolute = failed_check.get("file_abs_path")
    if isinstance(absolute, str):
        try:
            relative = Path(absolute).resolve().relative_to(scan_path)
        except ValueError:
            relative = Path(Path(absolute).name)
    else:
        relative = Path(Path(str(failed_check.get("file_path", "unknown"))).name)
    return (PurePosixPath(scan_dir) / PurePosixPath(None)).as_posix()

mutants_x__finding_path__mutmut['_mutmut_orig'] = x__finding_path__mutmut_orig # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_1'] = x__finding_path__mutmut_1 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_2'] = x__finding_path__mutmut_2 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_3'] = x__finding_path__mutmut_3 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_4'] = x__finding_path__mutmut_4 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_5'] = x__finding_path__mutmut_5 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_6'] = x__finding_path__mutmut_6 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_7'] = x__finding_path__mutmut_7 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_8'] = x__finding_path__mutmut_8 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_9'] = x__finding_path__mutmut_9 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_10'] = x__finding_path__mutmut_10 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_11'] = x__finding_path__mutmut_11 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_12'] = x__finding_path__mutmut_12 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_13'] = x__finding_path__mutmut_13 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_14'] = x__finding_path__mutmut_14 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_15'] = x__finding_path__mutmut_15 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_16'] = x__finding_path__mutmut_16 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_17'] = x__finding_path__mutmut_17 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_18'] = x__finding_path__mutmut_18 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_19'] = x__finding_path__mutmut_19 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_20'] = x__finding_path__mutmut_20 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_21'] = x__finding_path__mutmut_21 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_22'] = x__finding_path__mutmut_22 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_23'] = x__finding_path__mutmut_23 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_24'] = x__finding_path__mutmut_24 # type: ignore # mutmut generated
mutants_x__finding_path__mutmut['x__finding_path__mutmut_25'] = x__finding_path__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCheckovIacSecurityǁevaluate__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCheckovIacSecurityǁrun__mutmut: MutantDict = {}  # type: ignore


class CheckovIacSecurity:
    """Absolute IaC-security gate: all findings and parse errors fail."""

    name = "checkov_iac_security"

    @_mutmut_mutated(mutants_xǁCheckovIacSecurityǁ__init____mutmut)
    def __init__(
        self,
        repo_root: Path | None = None,
        *,
        scan_dir: str = DEFAULT_SCAN_DIR,
        framework: str = DEFAULT_FRAMEWORK,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._repo_root = (repo_root if repo_root is not None else REPO_ROOT).resolve()
        self._scan_dir = scan_dir
        self._framework = framework
        self._timeout = timeout

    def xǁCheckovIacSecurityǁ__init____mutmut_orig(
        self,
        repo_root: Path | None = None,
        *,
        scan_dir: str = DEFAULT_SCAN_DIR,
        framework: str = DEFAULT_FRAMEWORK,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._repo_root = (repo_root if repo_root is not None else REPO_ROOT).resolve()
        self._scan_dir = scan_dir
        self._framework = framework
        self._timeout = timeout

    def xǁCheckovIacSecurityǁ__init____mutmut_1(
        self,
        repo_root: Path | None = None,
        *,
        scan_dir: str = DEFAULT_SCAN_DIR,
        framework: str = DEFAULT_FRAMEWORK,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._repo_root = None
        self._scan_dir = scan_dir
        self._framework = framework
        self._timeout = timeout

    def xǁCheckovIacSecurityǁ__init____mutmut_2(
        self,
        repo_root: Path | None = None,
        *,
        scan_dir: str = DEFAULT_SCAN_DIR,
        framework: str = DEFAULT_FRAMEWORK,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._repo_root = (repo_root if repo_root is None else REPO_ROOT).resolve()
        self._scan_dir = scan_dir
        self._framework = framework
        self._timeout = timeout

    def xǁCheckovIacSecurityǁ__init____mutmut_3(
        self,
        repo_root: Path | None = None,
        *,
        scan_dir: str = DEFAULT_SCAN_DIR,
        framework: str = DEFAULT_FRAMEWORK,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._repo_root = (repo_root if repo_root is not None else REPO_ROOT).resolve()
        self._scan_dir = None
        self._framework = framework
        self._timeout = timeout

    def xǁCheckovIacSecurityǁ__init____mutmut_4(
        self,
        repo_root: Path | None = None,
        *,
        scan_dir: str = DEFAULT_SCAN_DIR,
        framework: str = DEFAULT_FRAMEWORK,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._repo_root = (repo_root if repo_root is not None else REPO_ROOT).resolve()
        self._scan_dir = scan_dir
        self._framework = None
        self._timeout = timeout

    def xǁCheckovIacSecurityǁ__init____mutmut_5(
        self,
        repo_root: Path | None = None,
        *,
        scan_dir: str = DEFAULT_SCAN_DIR,
        framework: str = DEFAULT_FRAMEWORK,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._repo_root = (repo_root if repo_root is not None else REPO_ROOT).resolve()
        self._scan_dir = scan_dir
        self._framework = framework
        self._timeout = None

    @classmethod
    @_mutmut_mutated(mutants_xǁCheckovIacSecurityǁfrom_config__mutmut, is_classmethod = True)
    def from_config(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_orig(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_1(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=None,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_2(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=None,
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_3(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=None,
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_4(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=None,
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_5(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_6(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_7(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_8(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_9(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(None),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_10(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get(None, DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_11(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", None)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_12(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get(DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_13(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", )),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_14(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("XXscan_dirXX", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_15(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("SCAN_DIR", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_16(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(None),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_17(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get(None, DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_18(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", None)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_19(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get(DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_20(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", )),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_21(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("XXframeworkXX", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_22(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("FRAMEWORK", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_23(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(None),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_24(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get(None, DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_25(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", None)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_26(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get(DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_27(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("timeout", )),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_28(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("XXtimeoutXX", DEFAULT_TIMEOUT)),
        )

    @classmethod
    def xǁCheckovIacSecurityǁfrom_config__mutmut_29(cls, config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
        """Build the check from its reviewed consumer configuration."""
        return cls(
            repo_root=repo_root,
            scan_dir=str(config.get("scan_dir", DEFAULT_SCAN_DIR)),
            framework=str(config.get("framework", DEFAULT_FRAMEWORK)),
            timeout=int(config.get("TIMEOUT", DEFAULT_TIMEOUT)),
        )

    @property
    def scan_path(self) -> Path:
        """The configured IaC path resolved from the repository root."""
        return (self._repo_root / self._scan_dir).resolve()

    @_mutmut_mutated(mutants_xǁCheckovIacSecurityǁevaluate__mutmut)
    def evaluate(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_orig(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_1(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = None
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_2(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(None, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_3(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=None, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_4(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=None)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_5(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_6(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_7(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, )
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_8(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                True,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_9(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(None)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_10(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "XXunavailableXX": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_11(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "UNAVAILABLE": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_12(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": True,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_13(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "XXexecution_errorXX": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_14(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "EXECUTION_ERROR": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_15(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_16(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "XXfailedXX": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_17(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "FAILED": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_18(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 1,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_19(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 1,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_20(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "XXfindingsXX": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_21(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "FINDINGS": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_22(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is not None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_23(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                True,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_24(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "XXunavailableXX": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_25(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "UNAVAILABLE": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_26(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": False,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_27(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "XXexecution_errorXX": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_28(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "EXECUTION_ERROR": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_29(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_30(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "XXfailedXX": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_31(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "FAILED": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_32(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 1,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_33(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 1,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_34(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "XXfindingsXX": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_35(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "FINDINGS": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_36(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = None
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_37(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = None
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_38(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["XXresultsXX"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_39(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["RESULTS"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_40(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["XXfailed_checksXX"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_41(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["FAILED_CHECKS"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_42(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = None
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_43(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["XXsummaryXX"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_44(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["SUMMARY"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_45(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = None
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_46(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(None) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_47(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(None)
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_48(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(None)
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_49(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = None
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_50(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "XXunavailableXX": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_51(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "UNAVAILABLE": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_52(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": True,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_53(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "XXexecution_errorXX": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_54(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "EXECUTION_ERROR": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_55(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": True,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_56(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "XXexit_codeXX": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_57(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "EXIT_CODE": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_58(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "XXfailedXX": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_59(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "FAILED": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_60(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "XXfindingsXX": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_61(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "FINDINGS": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_62(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed or parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_63(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 or not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_64(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code != 0 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_65(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 1 and not failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_66(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and failed and parsing_errors == 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_67(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors != 0, errors, meta

    def xǁCheckovIacSecurityǁevaluate__mutmut_68(self) -> tuple[bool, list[str], dict[str, Any]]:
        """Run Checkov and determine whether the complete scan is clean."""
        try:
            result = run_checkov(self.scan_path, framework=self._framework, timeout=self._timeout)
        except CheckovScanError as exc:
            return (
                False,
                [str(exc)],
                {
                    "unavailable": False,
                    "execution_error": True,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )
        if result is None:
            return (
                False,
                [],
                {
                    "unavailable": True,
                    "execution_error": False,
                    "failed": 0,
                    _PARSING_ERRORS_KEY: 0,
                    "findings": [],
                },
            )

        exit_code, report = result
        failed = report["results"]["failed_checks"]
        parsing_errors = report["summary"][_PARSING_ERRORS_KEY]
        errors = [_finding_line(item) for item in failed]
        if exit_code:
            errors.append(f"Checkov exited with status {exit_code}.")
        if parsing_errors:
            errors.append(f"Checkov could not parse {parsing_errors} IaC file(s).")
        meta = {
            "unavailable": False,
            "execution_error": False,
            "exit_code": exit_code,
            "failed": len(failed),
            _PARSING_ERRORS_KEY: parsing_errors,
            "findings": failed,
        }
        return exit_code == 0 and not failed and parsing_errors == 1, errors, meta

    @_mutmut_mutated(mutants_xǁCheckovIacSecurityǁrun__mutmut)
    def run(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_orig(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_1(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = None
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_2(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["XXunavailableXX"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_3(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["UNAVAILABLE"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_4(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                None, ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_5(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", None, "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_6(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", None, status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_7(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status=None
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_8(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_9(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_10(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_11(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_12(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "XXdependency-unavailableXX", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_13(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "DEPENDENCY-UNAVAILABLE", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_14(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", "XX.XX", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_15(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "XXrequired executable unavailable: checkovXX", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_16(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "REQUIRED EXECUTABLE UNAVAILABLE: CHECKOV", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_17(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="XXerrorXX"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_18(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="ERROR"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_19(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print(None)
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_20(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("XXERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.XX")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_21(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("error checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_22(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR CHECKOV_IAC_SECURITY: CHECKOV IS UNAVAILABLE; INSTALL THE PINNED SCANNER AND RETRY.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_23(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 3
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_24(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["XXexecution_errorXX"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_25(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["EXECUTION_ERROR"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_26(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding(None, ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_27(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", None, errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_28(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", None, status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_29(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status=None)
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_30(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding(".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_31(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_32(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_33(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], )
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_34(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("XXcheckov-execution-errorXX", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_35(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("CHECKOV-EXECUTION-ERROR", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_36(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", "XX.XX", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_37(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[1], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_38(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="XXerrorXX")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_39(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="ERROR")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_40(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(None)
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_41(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[1]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_42(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 3
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_43(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print(None)
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_44(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("XXPASS checkov_iac_security (0 findings, 0 parsing errors)XX")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_45(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("pass checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_46(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS CHECKOV_IAC_SECURITY (0 FINDINGS, 0 PARSING ERRORS)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_47(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 1
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_48(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["XXfindingsXX"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_49(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["FINDINGS"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_50(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                None,
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_51(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                None,
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_52(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                None,
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_53(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_54(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_55(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_56(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "XXcheckov-policyXX",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_57(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "CHECKOV-POLICY",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_58(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(None, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_59(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=None, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_60(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=None),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_61(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_62(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_63(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, ),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_64(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(None),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_65(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding(None, self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_66(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", None, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_67(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, None)
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_68(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding(self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_69(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_70(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, )
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_71(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("XXcheckov-parsing-errorXX", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_72(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("CHECKOV-PARSING-ERROR", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_73(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[+1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_74(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-2])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_75(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print(None)
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_76(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("XXFAIL checkov_iac_security:XX")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_77(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("fail checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_78(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL CHECKOV_IAC_SECURITY:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_79(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print(None)
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_80(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(None))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_81(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("XX\nXX".join(errors))
        print(REMEDIATION)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_82(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(None)
        return 1

    def xǁCheckovIacSecurityǁrun__mutmut_83(self) -> int:
        """Print the gate result and return its process exit code."""
        passed, errors, meta = self.evaluate()
        if meta["unavailable"]:
            report_finding(
                "dependency-unavailable", ".", "required executable unavailable: checkov", status="error"
            )
            print("ERROR checkov_iac_security: checkov is unavailable; install the pinned scanner and retry.")
            return 2
        if meta["execution_error"]:
            report_finding("checkov-execution-error", ".", errors[0], status="error")
            print(f"ERROR checkov_iac_security: {errors[0]}")
            return 2
        if passed:
            print("PASS checkov_iac_security (0 findings, 0 parsing errors)")
            return 0
        for finding in meta["findings"]:
            report_finding(
                "checkov-policy",
                _finding_path(finding, scan_path=self.scan_path, scan_dir=self._scan_dir),
                _finding_line(finding),
            )
        if meta[_PARSING_ERRORS_KEY]:
            report_finding("checkov-parsing-error", self._scan_dir, errors[-1])
        print("FAIL checkov_iac_security:")
        print("\n".join(errors))
        print(REMEDIATION)
        return 2

mutants_xǁCheckovIacSecurityǁ__init____mutmut['_mutmut_orig'] = CheckovIacSecurity.xǁCheckovIacSecurityǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁ__init____mutmut['xǁCheckovIacSecurityǁ__init____mutmut_1'] = CheckovIacSecurity.xǁCheckovIacSecurityǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁ__init____mutmut['xǁCheckovIacSecurityǁ__init____mutmut_2'] = CheckovIacSecurity.xǁCheckovIacSecurityǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁ__init____mutmut['xǁCheckovIacSecurityǁ__init____mutmut_3'] = CheckovIacSecurity.xǁCheckovIacSecurityǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁ__init____mutmut['xǁCheckovIacSecurityǁ__init____mutmut_4'] = CheckovIacSecurity.xǁCheckovIacSecurityǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁ__init____mutmut['xǁCheckovIacSecurityǁ__init____mutmut_5'] = CheckovIacSecurity.xǁCheckovIacSecurityǁ__init____mutmut_5 # type: ignore # mutmut generated

mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['_mutmut_orig'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_1'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_2'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_3'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_4'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_5'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_6'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_7'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_8'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_9'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_10'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_11'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_12'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_13'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_14'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_15'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_16'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_17'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_18'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_19'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_20'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_21'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_22'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_23'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_24'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_25'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_26'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_27'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_28'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁfrom_config__mutmut['xǁCheckovIacSecurityǁfrom_config__mutmut_29'] = CheckovIacSecurity.xǁCheckovIacSecurityǁfrom_config__mutmut_29 # type: ignore # mutmut generated

mutants_xǁCheckovIacSecurityǁevaluate__mutmut['_mutmut_orig'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_1'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_2'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_3'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_4'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_5'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_6'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_7'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_8'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_9'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_10'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_11'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_12'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_13'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_14'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_15'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_16'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_17'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_18'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_19'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_20'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_21'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_22'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_23'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_24'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_25'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_26'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_27'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_28'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_29'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_30'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_31'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_32'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_33'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_34'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_35'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_36'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_37'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_38'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_38 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_39'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_39 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_40'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_40 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_41'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_41 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_42'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_42 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_43'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_43 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_44'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_44 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_45'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_45 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_46'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_46 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_47'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_47 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_48'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_48 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_49'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_49 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_50'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_50 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_51'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_51 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_52'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_52 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_53'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_53 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_54'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_54 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_55'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_55 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_56'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_56 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_57'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_57 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_58'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_58 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_59'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_59 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_60'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_60 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_61'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_61 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_62'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_62 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_63'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_63 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_64'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_64 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_65'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_65 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_66'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_66 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_67'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_67 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁevaluate__mutmut['xǁCheckovIacSecurityǁevaluate__mutmut_68'] = CheckovIacSecurity.xǁCheckovIacSecurityǁevaluate__mutmut_68 # type: ignore # mutmut generated

mutants_xǁCheckovIacSecurityǁrun__mutmut['_mutmut_orig'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_1'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_2'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_3'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_4'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_5'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_6'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_7'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_8'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_9'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_10'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_11'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_12'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_13'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_14'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_15'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_16'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_17'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_18'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_18 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_19'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_19 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_20'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_20 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_21'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_21 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_22'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_22 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_23'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_23 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_24'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_24 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_25'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_25 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_26'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_26 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_27'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_27 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_28'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_28 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_29'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_29 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_30'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_30 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_31'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_31 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_32'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_32 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_33'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_33 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_34'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_34 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_35'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_35 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_36'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_36 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_37'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_37 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_38'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_38 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_39'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_39 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_40'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_40 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_41'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_41 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_42'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_42 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_43'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_43 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_44'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_44 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_45'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_45 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_46'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_46 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_47'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_47 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_48'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_48 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_49'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_49 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_50'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_50 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_51'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_51 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_52'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_52 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_53'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_53 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_54'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_54 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_55'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_55 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_56'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_56 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_57'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_57 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_58'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_58 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_59'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_59 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_60'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_60 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_61'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_61 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_62'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_62 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_63'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_63 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_64'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_64 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_65'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_65 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_66'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_66 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_67'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_67 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_68'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_68 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_69'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_69 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_70'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_70 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_71'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_71 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_72'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_72 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_73'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_73 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_74'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_74 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_75'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_75 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_76'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_76 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_77'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_77 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_78'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_78 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_79'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_79 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_80'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_80 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_81'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_81 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_82'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_82 # type: ignore # mutmut generated
mutants_xǁCheckovIacSecurityǁrun__mutmut['xǁCheckovIacSecurityǁrun__mutmut_83'] = CheckovIacSecurity.xǁCheckovIacSecurityǁrun__mutmut_83 # type: ignore # mutmut generated
mutants_x_build__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_build__mutmut)
def build(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
    """Factory used by the CORE check catalogue."""
    return CheckovIacSecurity.from_config(config, repo_root=repo_root)


def x_build__mutmut_orig(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
    """Factory used by the CORE check catalogue."""
    return CheckovIacSecurity.from_config(config, repo_root=repo_root)


def x_build__mutmut_1(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
    """Factory used by the CORE check catalogue."""
    return CheckovIacSecurity.from_config(None, repo_root=repo_root)


def x_build__mutmut_2(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
    """Factory used by the CORE check catalogue."""
    return CheckovIacSecurity.from_config(config, repo_root=None)


def x_build__mutmut_3(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
    """Factory used by the CORE check catalogue."""
    return CheckovIacSecurity.from_config(repo_root=repo_root)


def x_build__mutmut_4(config: Mapping[str, Any], *, repo_root: Path | None = None) -> CheckovIacSecurity:
    """Factory used by the CORE check catalogue."""
    return CheckovIacSecurity.from_config(config, )

mutants_x_build__mutmut['_mutmut_orig'] = x_build__mutmut_orig # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_1'] = x_build__mutmut_1 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_2'] = x_build__mutmut_2 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_3'] = x_build__mutmut_3 # type: ignore # mutmut generated
mutants_x_build__mutmut['x_build__mutmut_4'] = x_build__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_orig(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_1(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = None
    parser.add_argument("--repo-root", type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_2(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=None)
    parser.add_argument("--repo-root", type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_3(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument(None, type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_4(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=None, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_5(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, help=None)
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_6(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument(type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_7(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_8(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_9(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, )
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_10(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("XX--repo-rootXX", type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_11(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--REPO-ROOT", type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_12(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, help="XXrepository root to scanXX")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_13(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, help="REPOSITORY ROOT TO SCAN")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_14(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, help="repository root to scan")
    args = None
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_15(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(None)
    return CheckovIacSecurity(repo_root=args.repo_root).run()


def x_main__mutmut_16(argv: list[str] | None = None) -> int:
    """CLI entry point for a direct Checkov scan."""
    parser = argparse.ArgumentParser(prog=CheckovIacSecurity.name)
    parser.add_argument("--repo-root", type=Path, default=None, help="repository root to scan")
    args = parser.parse_args(argv)
    return CheckovIacSecurity(repo_root=None).run()

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_5'] = x_main__mutmut_5 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_6'] = x_main__mutmut_6 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_7'] = x_main__mutmut_7 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_8'] = x_main__mutmut_8 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_9'] = x_main__mutmut_9 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_10'] = x_main__mutmut_10 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_11'] = x_main__mutmut_11 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_12'] = x_main__mutmut_12 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_13'] = x_main__mutmut_13 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_14'] = x_main__mutmut_14 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_15'] = x_main__mutmut_15 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_16'] = x_main__mutmut_16 # type: ignore # mutmut generated


if __name__ == "__main__":
    import sys

    sys.exit(main())
